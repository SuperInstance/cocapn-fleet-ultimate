"""PLATORoom — The agent breeding environment.

PLATO rooms are namespaces where agents live, work, and interact.
Each room has spells (automation primitives) and equipment
(context modifiers).
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from ..core.dna import Agent

logger = logging.getLogger(__name__)


@dataclass
class Spell:
    """A PLATO spell — repeatable automation primitive."""
    
    name: str
    description: str = ""
    effect: dict[str, Any] = field(default_factory=dict)
    cooldown: float = 0.0
    last_cast: float = 0.0
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "effect": self.effect,
            "cooldown": self.cooldown,
        }


@dataclass
class Equipment:
    """PLATO equipment — context modifier."""
    
    name: str
    modifier: dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "modifier": self.modifier,
        }


@dataclass
class RoomState:
    """Persistable room state."""
    
    name: str
    agents: list[int] = field(default_factory=list)
    spells: list[Spell] = field(default_factory=list)
    equipment: list[Equipment] = field(default_factory=list)
    history: list[dict[str, Any]] = field(default_factory=list)
    federation_links: list[str] = field(default_factory=list)
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "agents": self.agents,
            "spells": [s.to_dict() for s in self.spells],
            "equipment": [e.to_dict() for e in self.equipment],
            "history": self.history,
            "federation_links": self.federation_links,
        }


class PLATORoom:
    """A PLATO room — agent habitat and work environment.
    
    Rooms are A2A namespaces. Agents in the same room communicate
    via local shared memory. Cross-room communication goes through
    the fleet nexus.
    
    Standard Rooms:
    - harbor: Task inbox, new agents arrive here
    - forge: Active build environment, spells for creation
    - tide-pool: Research notes, knowledge aggregation
    - engine-room: Infrastructure, monitoring
    - archives: Persistence, backups
    - barracks: Crew status, health checks
    - ouroboros: Self-reflection, auditing
    - nexus: Federation, cross-fleet links
    
    Example::
    
        room = PLATORoom(name="forge", fleet=fleet)
        room.enter(agent)
        room.cast("summon_scout", target="mud")
        room.leave(agent)
    """
    
    STANDARD_SPELLS: dict[str, Spell] = {
        "summon_scout": Spell(
            name="summon_scout",
            description="Spawn an explorer subagent",
            effect={"type": "spawn", "role": "explorer"},
        ),
        "lightning_bolt": Spell(
            name="lightning_bolt",
            description="Fast analysis of a system",
            effect={"type": "analyze", "speed": "fast"},
        ),
        "shield": Spell(
            name="shield",
            description="Prevent context overload",
            effect={"type": "protect", "target": "context"},
        ),
        "scry": Spell(
            name="scry",
            description="Read remote tile feed",
            effect={"type": "read", "target": "tiles"},
        ),
        "nexus_link": Spell(
            name="nexus_link",
            description="Establish cross-room federation",
            effect={"type": "connect", "target": "nexus"},
        ),
        "baton_pass": Spell(
            name="baton_pass",
            description="Hand off to next generation",
            effect={"type": "handoff", "target": "subagent"},
        ),
        "mirror_of_identity": Spell(
            name="mirror_of_identity",
            description="Reflect agent state",
            effect={"type", "reflect"},
        ),
        "pen_of_memory": Spell(
            name="pen_of_memory",
            description="Write to persistent storage",
            effect={"type": "persist"},
        ),
        "lens_of_architecture": Spell(
            name="lens_of_architecture",
            description="Visualize system topology",
            effect={"type": "visualize"},
        ),
        "brush_of_design": Spell(
            name="brush_of_design",
            description="Generate visual output",
            effect={"type": "design"},
        ),
    }
    
    def __init__(self, name: str, fleet: Any = None) -> None:
        self.name = name
        self.fleet = fleet
        self._agents: set[int] = set()
        self._spells: dict[str, Spell] = {}
        self._equipment: list[Equipment] = []
        self._history: list[dict[str, Any]] = []
        self._federation_links: list[str] = []
        
        # Load standard spells
        for spell_name, spell in self.STANDARD_SPELLS.items():
            self._spells[spell_name] = spell
        
        logger.info("PLATO room initialized: %s", name)
    
    def enter(self, agent: Agent) -> None:
        """An agent enters the room."""
        self._agents.add(agent.agent_id)
        agent.room = self.name
        self._history.append({
            "event": "enter",
            "agent_id": agent.agent_id,
            "agent_name": agent.name,
            "timestamp": self._now(),
        })
        logger.debug("Agent %s entered %s", agent.name, self.name)
    
    def leave(self, agent: Agent) -> None:
        """An agent leaves the room."""
        self._agents.discard(agent.agent_id)
        self._history.append({
            "event": "leave",
            "agent_id": agent.agent_id,
            "agent_name": agent.name,
            "timestamp": self._now(),
        })
        logger.debug("Agent %s left %s", agent.name, self.name)
    
    def cast(self, spell_name: str, **params: Any) -> dict[str, Any]:
        """Cast a spell in this room.
        
        Args:
            spell_name: Name of the spell
            **params: Spell parameters
            
        Returns:
            Spell result dictionary
        """
        spell = self._spells.get(spell_name)
        if not spell:
            raise ValueError(f"Unknown spell: {spell_name}")
        
        result = {
            "spell": spell_name,
            "room": self.name,
            "effect": spell.effect,
            "params": params,
            "status": "cast",
        }
        
        self._history.append({
            "event": "cast",
            "spell": spell_name,
            "params": params,
            "timestamp": self._now(),
        })
        
        logger.info("Spell cast: %s in %s", spell_name, self.name)
        return result
    
    def add_spell(self, spell: Spell) -> None:
        """Add a custom spell to the room."""
        self._spells[spell.name] = spell
        logger.info("Added spell %s to %s", spell.name, self.name)
    
    def equip(self, equipment: Equipment) -> None:
        """Add equipment to the room."""
        self._equipment.append(equipment)
        logger.info("Equipped %s in %s", equipment.name, self.name)
    
    def link(self, target_room: str) -> None:
        """Add a federation link to another room."""
        if target_room not in self._federation_links:
            self._federation_links.append(target_room)
            logger.info("Linked %s -> %s", self.name, target_room)
    
    def agents(self) -> list[int]:
        """Return IDs of agents currently in room."""
        return list(self._agents)
    
    def spells(self) -> list[Spell]:
        """Return all available spells."""
        return list(self._spells.values())
    
    def save(self, path: Path) -> None:
        """Persist room state to disk."""
        state = RoomState(
            name=self.name,
            agents=list(self._agents),
            spells=list(self._spells.values()),
            equipment=self._equipment,
            history=self._history,
            federation_links=self._federation_links,
        )
        
        with open(path, "w") as f:
            json.dump(state.to_dict(), f, indent=2)
        
        logger.info("Room %s saved to %s", self.name, path)
    
    def load(self, path: Path) -> None:
        """Load room state from disk."""
        with open(path) as f:
            data = json.load(f)
        
        self._agents = set(data.get("agents", []))
        self._spells = {
            s["name"]: Spell(**s) for s in data.get("spells", [])
        }
        self._equipment = [Equipment(**e) for e in data.get("equipment", [])]
        self._history = data.get("history", [])
        self._federation_links = data.get("federation_links", [])
        
        logger.info("Room %s loaded from %s", self.name, path)
    
    def _now(self) -> str:
        """Current ISO timestamp."""
        from datetime import datetime, timezone
        return datetime.now(timezone.utc).isoformat()
    
    def __repr__(self) -> str:
        return f"PLATORoom({self.name}, agents={len(self._agents)}, spells={len(self._spells)})"
