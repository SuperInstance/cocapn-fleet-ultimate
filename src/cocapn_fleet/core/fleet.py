"""FleetCore — The unified entrypoint for the Cocapn Fleet.

FleetCore is the orchestrator that binds every subsystem into a single,
coherent whole. It is the A2A-first application kernel.
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .dna import AgentDNA
from .trinity.scorer import TrinityScore
from .a2a.client import A2AClient
from .plato.room import PLATORoom
from .flux.checker import FLUXChecker
from .breeding.orchestrator import BreedingOrchestrator
from .grammar.engine import GrammarEngine
from .nexus.federation import FleetNexus

logger = logging.getLogger(__name__)


@dataclass
class FleetConfig:
    """Configuration for FleetCore initialization."""
    
    name: str = "cocapn-fleet"
    dim: int = 256
    bit_width: int = 4
    rooms: list[str] = field(default_factory=lambda: [
        "harbor", "forge", "tide-pool", "engine-room", 
        "archives", "barracks", "ouroboros", "nexus"
    ])
    enable_flux: bool = True
    enable_breeding: bool = True
    enable_grammar: bool = True
    enable_nexus: bool = True
    nexus_endpoint: str | None = None
    data_dir: Path = field(default_factory=lambda: Path("./fleet-data"))


class FleetCore:
    """The unified fleet orchestrator.
    
    FleetCore is the A2A-first application kernel. It manages:
    - Agent DNA memory (turbovec-backed)
    - PLATO room system
    - FLUX constraint checking
    - Trinity fitness scoring
    - Breeding lifecycle
    - Grammar rule engine
    - Fleet nexus federation
    
    Example::
    
        fleet = FleetCore(FleetConfig(name="my-fleet"))
        fleet.welcome()
        
        # Spawn an agent
        agent = fleet.spawn(name="explorer", room="harbor")
        
        # Check constraints
        result = fleet.flux.check("temperature < 300", reading=295.4)
        
        # Search DNA
        neighbors = fleet.dna.search(agent.vector, k=5)
        
        # Breed next generation
        fleet.breeding.tick()
    """
    
    def __init__(self, config: FleetConfig | None = None) -> None:
        self.config = config or FleetConfig()
        self.config.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize subsystems
        self.dna = AgentDNA(dim=self.config.dim, bit_width=self.config.bit_width)
        self.trinity = TrinityScore()
        self.a2a = A2AClient(agent_name=self.config.name)
        self.rooms: dict[str, PLATORoom] = {}
        self.flux = FLUXChecker() if self.config.enable_flux else None
        self.breeding = BreedingOrchestrator(self) if self.config.enable_breeding else None
        self.grammar = GrammarEngine() if self.config.enable_grammar else None
        self.nexus = FleetNexus(endpoint=self.config.nexus_endpoint) if self.config.enable_nexus else None
        
        # Initialize PLATO rooms
        for room_name in self.config.rooms:
            self.rooms[room_name] = PLATORoom(name=room_name, fleet=self)
        
        logger.info("FleetCore initialized: %s (dim=%d, rooms=%d)", 
                   self.config.name, self.config.dim, len(self.rooms))
    
    def welcome(self) -> str:
        """Return a welcome message with fleet status."""
        status = {
            "fleet": self.config.name,
            "version": "0.1.0",
            "agents": len(self.dna),
            "rooms": list(self.rooms.keys()),
            "subsystems": {
                "flux": self.flux is not None,
                "breeding": self.breeding is not None,
                "grammar": self.grammar is not None,
                "nexus": self.nexus is not None,
            },
            "dna": {
                "dim": self.config.dim,
                "bit_width": self.config.bit_width,
                "compression": f"{self.config.bit_width}-bit",
            }
        }
        return json.dumps(status, indent=2)
    
    def spawn(self, name: str, room: str = "harbor", 
              vector: list[float] | None = None,
              **meta: Any) -> AgentDNA:
        """Spawn a new agent into the fleet.
        
        Args:
            name: Human-readable agent name
            room: PLATO room to place the agent in
            vector: Optional DNA vector (auto-generated if None)
            **meta: Additional agent metadata
            
        Returns:
            The spawned AgentDNA instance
        """
        import numpy as np
        
        if vector is None:
            rng = np.random.default_rng()
            v = rng.standard_normal(self.config.dim).astype(np.float32)
            v /= np.linalg.norm(v) + 1e-8
            vector = v.tolist()
        
        agent = self.dna.add(name=name, vector=vector, room=room, **meta)
        
        # Enter PLATO room
        if room in self.rooms:
            self.rooms[room].enter(agent)
        
        logger.info("Spawned agent %s in room %s (id=%d)", name, room, agent.agent_id)
        return agent
    
    def tick(self) -> dict[str, Any]:
        """Run one fleet tick — breeding, scoring, constraints.
        
        Returns:
            Tick summary with statistics
        """
        results: dict[str, Any] = {"generation": 0, "events": []}
        
        # Run breeding if enabled
        if self.breeding:
            breed_result = self.breeding.tick()
            results["generation"] = breed_result.get("generation", 0)
            results["events"].extend(breed_result.get("events", []))
        
        # Score all agents
        for agent in self.dna.all():
            score = self.trinity.score(agent)
            agent.fitness = score.product
        
        # Check constraints
        if self.flux:
            violations = self.flux.audit(self.dna.all())
            results["violations"] = len(violations)
            results["events"].extend([v.to_dict() for v in violations])
        
        logger.info("Tick complete: gen=%d, agents=%d, events=%d",
                   results["generation"], len(self.dna), len(results["events"]))
        return results
    
    def save(self, path: Path | None = None) -> Path:
        """Persist fleet state to disk.
        
        Returns:
            Path to saved state directory
        """
        path = path or self.config.data_dir / "fleet-state"
        path.mkdir(parents=True, exist_ok=True)
        
        # Save DNA index
        self.dna.write(path / "dna.tvim")
        
        # Save room states
        for name, room in self.rooms.items():
            room.save(path / f"room-{name}.json")
        
        # Save config
        with open(path / "config.json", "w") as f:
            json.dump({
                "name": self.config.name,
                "dim": self.config.dim,
                "bit_width": self.config.bit_width,
                "rooms": self.config.rooms,
            }, f, indent=2)
        
        logger.info("Fleet state saved to %s", path)
        return path
    
    @classmethod
    def load(cls, path: Path) -> "FleetCore":
        """Load fleet state from disk."""
        with open(path / "config.json") as f:
            config_dict = json.load(f)
        
        config = FleetConfig(**config_dict)
        instance = cls(config)
        
        # Load DNA
        instance.dna = AgentDNA.load(path / "dna.tvim", dim=config.dim)
        
        # Load rooms
        for name in config.rooms:
            room_path = path / f"room-{name}.json"
            if room_path.exists():
                instance.rooms[name].load(room_path)
        
        logger.info("Fleet state loaded from %s", path)
        return instance
    
    def __repr__(self) -> str:
        return f"FleetCore({self.config.name}, agents={len(self.dna)}, rooms={len(self.rooms)})"
