"""BreedingOrchestrator — Agent lifecycle and evolution.

Manages the complete agent lifecycle:
INCUBATE → COMPETE → (SURVIVE → BREED) or (SUNSET → ARCHIVE)

Each tick advances the generation, runs tournaments,
selects parents, spawns children, and archives losers.
"""

from __future__ import annotations

import json
import logging
import random
from dataclasses import dataclass, field
from typing import Any

from ..core.dna import Agent
from ..trinity.scorer import TrinityScore

logger = logging.getLogger(__name__)


@dataclass
class BreedingEvent:
    """A single breeding lifecycle event."""
    
    generation: int
    event_type: str  # incubate, compete, survive, breed, sunset, archive
    agent_id: int | None = None
    agent_name: str = ""
    details: dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "generation": self.generation,
            "event_type": self.event_type,
            "agent_id": self.agent_id,
            "agent_name": self.agent_name,
            "details": self.details,
        }


class BreedingOrchestrator:
    """Breeding daemon — manages agent evolution.
    
    The lifecycle is a state machine:
    
    INCUBATE: Spawn new agents from seed or mutation
    COMPETE: Run tournament rounds
    SURVIVE: Agents above threshold continue
    BREED: Top agents produce children
    SUNSET: Below-threshold agents marked for removal
    ARCHIVE: Sunset agents written to epilogue
    
    Example::
    
        breeding = BreedingOrchestrator(fleet)
        
        # Run one generation
        result = breeding.tick()
        
        # Access generation history
        print(f"Generation {result['generation']}: {len(result['events'])} events")
    """
    
    def __init__(self, fleet: Any) -> None:
        self.fleet = fleet
        self.generation = 0
        self.scorer = TrinityScore()
        self._history: list[BreedingEvent] = []
        self._sunset_agents: list[Agent] = []
        self._archive_path: Any = None
        
        # Configuration
        self.tournament_size = 4
        self.survival_threshold = TrinityScore.SURVIVE_THRESHOLD
        self.breed_threshold = TrinityScore.BREED_THRESHOLD
        self.max_population = 100
        self.diversity_pressure = 0.3  # Weight for diversity in parent selection
    
    def tick(self) -> dict[str, Any]:
        """Run one complete breeding cycle.
        
        Returns:
            Dict with generation number, events, and statistics
        """
        self.generation += 1
        events: list[BreedingEvent] = []
        
        # Get all current agents
        agents = self.fleet.dna.all()
        
        # Phase 1: Score all agents
        scored = [(a, self.scorer.score(a)) for a in agents]
        
        # Phase 2: Run tournaments for selection pressure
        if len(agents) >= self.tournament_size:
            winners = self.scorer.tournament(agents, self.tournament_size)
            winner_ids = {a.agent_id for a, _ in winners}
        else:
            winner_ids = {a.agent_id for a in agents}
        
        # Phase 3: Classify agents
        survivors: list[Agent] = []
        breeders: list[tuple[Agent, Any]] = []
        sunset: list[Agent] = []
        
        for agent, score in scored:
            if score.product >= self.breed_threshold and agent.agent_id in winner_ids:
                breeders.append((agent, score))
                events.append(BreedingEvent(
                    generation=self.generation,
                    event_type="breed",
                    agent_id=agent.agent_id,
                    agent_name=agent.name,
                    details={"fitness": score.product},
                ))
            elif score.product >= self.survival_threshold:
                survivors.append(agent)
                events.append(BreedingEvent(
                    generation=self.generation,
                    event_type="survive",
                    agent_id=agent.agent_id,
                    agent_name=agent.name,
                    details={"fitness": score.product},
                ))
            else:
                sunset.append(agent)
                events.append(BreedingEvent(
                    generation=self.generation,
                    event_type="sunset",
                    agent_id=agent.agent_id,
                    agent_name=agent.name,
                    details={"fitness": score.product},
                ))
        
        # Phase 4: Breed new agents
        children: list[Agent] = []
        if len(breeders) >= 2 and len(agents) < self.max_population:
            # Select diverse parents
            parents = self._select_parents(breeders)
            
            for i in range(min(len(parents) // 2, self.max_population - len(agents))):
                p1, p2 = parents[i], parents[i + 1] if i + 1 < len(parents) else parents[0]
                child = self._spawn_child(p1, p2)
                children.append(child)
                
                events.append(BreedingEvent(
                    generation=self.generation,
                    event_type="incubate",
                    agent_id=child.agent_id,
                    agent_name=child.name,
                    details={
                        "parents": [p1.agent_id, p2.agent_id],
                        "parent_names": [p1.name, p2.name],
                    },
                ))
        
        # Phase 5: Archive sunset agents
        for agent in sunset:
            self._sunset_agents.append(agent)
            self.fleet.dna.remove(agent.agent_id)
            
            events.append(BreedingEvent(
                generation=self.generation,
                event_type="archive",
                agent_id=agent.agent_id,
                agent_name=agent.name,
                details={"archive_size": len(self._sunset_agents)},
            ))
        
        self._history.extend(events)
        
        result = {
            "generation": self.generation,
            "events": [e.to_dict() for e in events],
            "stats": {
                "total_agents": len(self.fleet.dna),
                "survivors": len(survivors),
                "breeders": len(breeders),
                "sunset": len(sunset),
                "children": len(children),
                "archive_size": len(self._sunset_agents),
            },
        }
        
        logger.info("Generation %d: %s", self.generation, result["stats"])
        return result
    
    def _select_parents(self, breeders: list[tuple[Agent, Any]]) -> list[Agent]:
        """Select diverse parents for breeding.
        
        Uses a diversity-seeking selection that penalizes
        similarity to already-selected parents.
        """
        import numpy as np
        
        selected: list[Agent] = []
        candidates = [a for a, _ in breeders]
        
        # Sort by fitness
        candidates.sort(key=lambda a: a.fitness, reverse=True)
        
        for _ in range(min(len(candidates), 6)):
            if not candidates:
                break
            
            # Score candidates by fitness + diversity
            best_score = -1.0
            best_idx = 0
            
            for i, candidate in enumerate(candidates):
                fitness_score = candidate.fitness
                
                # Diversity penalty: distance from already selected
                if selected:
                    v = np.array(candidate.vector)
                    diversities = []
                    for s in selected:
                        sv = np.array(s.vector)
                        sim = np.dot(v, sv) / (np.linalg.norm(v) * np.linalg.norm(sv) + 1e-8)
                        diversities.append(1.0 - sim)  # Higher = more diverse
                    diversity = np.mean(diversities)
                else:
                    diversity = 1.0
                
                score = (1.0 - self.diversity_pressure) * fitness_score + self.diversity_pressure * diversity
                
                if score > best_score:
                    best_score = score
                    best_idx = i
            
            selected.append(candidates.pop(best_idx))
        
        return selected
    
    def _spawn_child(self, parent1: Agent, parent2: Agent) -> Agent:
        """Spawn a child agent from two parents.
        
        Uses vector interpolation with random mutation.
        """
        import numpy as np
        
        # Interpolate vectors
        v1 = np.array(parent1.vector, dtype=np.float32)
        v2 = np.array(parent2.vector, dtype=np.float32)
        
        # Random interpolation factor
        alpha = np.random.random()
        child_vector = alpha * v1 + (1 - alpha) * v2
        
        # Add mutation
        mutation_rate = 0.1
        mutation = np.random.standard_normal(self.fleet.config.dim).astype(np.float32) * mutation_rate
        child_vector += mutation
        
        # Normalize
        child_vector /= np.linalg.norm(child_vector) + 1e-8
        
        # Create child
        child = self.fleet.spawn(
            name=f"gen{self.generation}-{parent1.name[:4]}{parent2.name[:4]}",
            room="harbor",
            vector=child_vector.tolist(),
            generation=self.generation,
            parents=[parent1.agent_id, parent2.agent_id],
        )
        
        return child
    
    def history(self) -> list[BreedingEvent]:
        """Return complete breeding history."""
        return self._history.copy()
    
    def get_archive(self) -> list[Agent]:
        """Return sunset agents."""
        return self._sunset_agents.copy()
    
    def stats(self) -> dict[str, Any]:
        """Return breeding statistics."""
        return {
            "generation": self.generation,
            "active_agents": len(self.fleet.dna),
            "total_sunset": len(self._sunset_agents),
            "total_events": len(self._history),
            "tournament_size": self.tournament_size,
            "survival_threshold": self.survival_threshold,
            "breed_threshold": self.breed_threshold,
            "max_population": self.max_population,
        }
