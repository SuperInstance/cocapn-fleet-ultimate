"""AgentDNA — Hardware-accelerated agent memory with turbovec.

Each agent has a compressed DNA vector that captures its behavioral
and architectural signature. Turbovec provides 4-bit quantized
storage with sub-millisecond search.
"""

from __future__ import annotations

import json
import logging
import struct
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class Agent:
    """A single agent in the fleet."""
    
    agent_id: int
    name: str
    vector: list[float]
    fitness: float = 0.0
    room: str = "harbor"
    generation: int = 0
    meta: dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "vector": self.vector,
            "fitness": self.fitness,
            "room": self.room,
            "generation": self.generation,
            "meta": self.meta,
        }
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Agent":
        return cls(**data)


class AgentDNA:
    """Hardware-accelerated DNA index for the fleet.
    
    Wraps turbovec for compressed vector storage. Falls back to
    numpy brute-force search if turbovec is unavailable.
    
    Example::
    
        dna = AgentDNA(dim=256, bit_width=4)
        agent = dna.add(name="explorer", vector=[0.1, -0.2, ...])
        neighbors = dna.search(agent.vector, k=5)
    """
    
    def __init__(self, dim: int = 256, bit_width: int = 4) -> None:
        self.dim = dim
        self.bit_width = bit_width
        self._agents: dict[int, Agent] = {}
        self._next_id = 1
        self._index: Any = None
        self._fallback: bool = False
        
        # Try turbovec first
        try:
            import turbovec as tv
            self._index = tv.Indexer(dim=dim, bit_width=bit_width)
            logger.info("Turbovec indexer loaded (dim=%d, bits=%d)", dim, bit_width)
        except Exception as e:
            logger.warning("Turbovec unavailable, using numpy fallback: %s", e)
            self._fallback = True
            import numpy as np
            self._vectors: np.ndarray = np.zeros((0, dim), dtype=np.float32)
            self._ids: list[int] = []
    
    def add(self, name: str, vector: list[float], room: str = "harbor",
            generation: int = 0, **meta: Any) -> Agent:
        """Add a new agent to the DNA index.
        
        Args:
            name: Human-readable agent name
            vector: DNA vector (length must match dim)
            room: PLATO room assignment
            generation: Breeding generation number
            **meta: Additional metadata
            
        Returns:
            The created Agent instance
        """
        import numpy as np
        
        agent_id = self._next_id
        self._next_id += 1
        
        agent = Agent(
            agent_id=agent_id,
            name=name,
            vector=vector,
            room=room,
            generation=generation,
            meta=meta,
        )
        self._agents[agent_id] = agent
        
        v = np.array(vector, dtype=np.float32)
        if v.shape != (self.dim,):
            raise ValueError(f"Vector dim {v.shape} != index dim {self.dim}")
        
        if not self._fallback:
            import turbovec as tv
            ids = np.array([agent_id], dtype=np.uint64)
            vectors = v.reshape(1, -1)
            try:
                self._index.add_with_ids(vectors, ids)
            except TypeError:
                # Handle API variations
                self._index.add_with_ids(ids, vectors)
        else:
            if len(self._vectors) == 0:
                self._vectors = v.reshape(1, -1)
            else:
                self._vectors = np.vstack([self._vectors, v.reshape(1, -1)])
            self._ids.append(agent_id)
        
        logger.debug("Added agent %s (id=%d)", name, agent_id)
        return agent
    
    def search(self, vector: list[float], k: int = 5,
               allowlist: list[int] | None = None) -> list[tuple[Agent, float]]:
        """Find k nearest neighbors by DNA similarity.
        
        Args:
            vector: Query vector
            k: Number of neighbors to return
            allowlist: Optional agent IDs to restrict search to
            
        Returns:
            List of (Agent, score) tuples, sorted by score ascending
        """
        import numpy as np
        
        v = np.array(vector, dtype=np.float32).reshape(1, -1)
        
        if not self._fallback:
            try:
                scores, ids = self._index.search(v, k)
            except Exception:
                # Handle API variations
                result = self._index.search(v, k)
                if isinstance(result, tuple):
                    scores, ids = result
                else:
                    scores = result
                    ids = np.arange(len(result))
            
            results = []
            for idx, agent_id in enumerate(ids[0] if len(ids.shape) > 1 else ids):
                agent_id = int(agent_id)
                if agent_id in self._agents:
                    score = float(scores[0][idx] if len(scores.shape) > 1 else scores[idx])
                    results.append((self._agents[agent_id], score))
            return results
        else:
            # Numpy fallback
            if len(self._vectors) == 0:
                return []
            
            # Compute cosine distances
            v_norm = v / (np.linalg.norm(v) + 1e-8)
            vecs_norm = self._vectors / (np.linalg.norm(self._vectors, axis=1, keepdims=True) + 1e-8)
            similarities = np.dot(vecs_norm, v_norm.T).flatten()
            
            # Get top k
            top_k = np.argsort(-similarities)[:k]
            return [(self._agents[self._ids[i]], float(1.0 - similarities[i])) for i in top_k]
    
    def remove(self, agent_id: int) -> bool:
        """Remove an agent from the index.
        
        Note: turbovec indices don't support true deletion.
        The agent is removed from the agent map but remains in the index.
        """
        if agent_id in self._agents:
            del self._agents[agent_id]
            logger.debug("Removed agent id=%d", agent_id)
            return True
        return False
    
    def all(self) -> list[Agent]:
        """Return all active agents."""
        return list(self._agents.values())
    
    def get(self, agent_id: int) -> Agent | None:
        """Get agent by ID."""
        return self._agents.get(agent_id)
    
    def __len__(self) -> int:
        return len(self._agents)
    
    def write(self, path: Path) -> None:
        """Save DNA state to disk."""
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        # Save agent metadata
        meta_path = path.with_suffix(".json")
        with open(meta_path, "w") as f:
            json.dump({
                "dim": self.dim,
                "bit_width": self.bit_width,
                "next_id": self._next_id,
                "agents": [a.to_dict() for a in self._agents.values()],
            }, f, indent=2)
        
        # Save turbovec index if available
        if not self._fallback and hasattr(self._index, "write"):
            self._index.write(str(path))
        
        logger.info("DNA saved to %s (%d agents)", path, len(self._agents))
    
    @classmethod
    def load(cls, path: Path, dim: int = 256) -> "AgentDNA":
        """Load DNA state from disk."""
        path = Path(path)
        meta_path = path.with_suffix(".json")
        
        instance = cls(dim=dim)
        
        if meta_path.exists():
            with open(meta_path) as f:
                data = json.load(f)
            
            instance.dim = data.get("dim", dim)
            instance.bit_width = data.get("bit_width", 4)
            instance._next_id = data.get("next_id", 1)
            
            for agent_data in data.get("agents", []):
                agent = Agent.from_dict(agent_data)
                instance._agents[agent.agent_id] = agent
                
                # Re-add to index
                if not instance._fallback:
                    import numpy as np
                    v = np.array(agent.vector, dtype=np.float32).reshape(1, -1)
                    ids = np.array([agent.agent_id], dtype=np.uint64)
                    try:
                        instance._index.add_with_ids(v, ids)
                    except TypeError:
                        instance._index.add_with_ids(ids, v)
                else:
                    import numpy as np
                    v = np.array(agent.vector, dtype=np.float32).reshape(1, -1)
                    if len(instance._vectors) == 0:
                        instance._vectors = v
                    else:
                        instance._vectors = np.vstack([instance._vectors, v])
                    instance._ids.append(agent.agent_id)
        
        # Load turbovec index if available
        if not instance._fallback and path.exists() and hasattr(instance._index, "load"):
            instance._index.load(str(path))
        
        logger.info("DNA loaded from %s (%d agents)", path, len(instance._agents))
        return instance
    
    def stats(self) -> dict[str, Any]:
        """Return index statistics."""
        return {
            "agents": len(self._agents),
            "dim": self.dim,
            "bit_width": self.bit_width,
            "compression": f"{self.bit_width}-bit",
            "backend": "turbovec" if not self._fallback else "numpy",
            "memory_estimate_mb": len(self._agents) * self.dim * self.bit_width / 8 / 1024 / 1024,
        }
