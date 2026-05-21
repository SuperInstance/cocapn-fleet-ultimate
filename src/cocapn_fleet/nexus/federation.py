"""FleetNexus — Cross-node federation and coordination.

The nexus manages fleet-wide registration, heartbeats, and
status aggregation across multiple nodes.
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class NodeStatus:
    """Status of a fleet node."""
    
    node_id: str
    name: str
    endpoint: str
    last_heartbeat: str = ""
    status: str = "unknown"
    metrics: dict[str, Any] = field(default_factory=dict)
    rooms: list[str] = field(default_factory=list)
    agent_count: int = 0
    
    def is_alive(self, timeout_seconds: float = 60.0) -> bool:
        """Check if node is alive based on last heartbeat."""
        try:
            last = datetime.fromisoformat(self.last_heartbeat.replace("Z", "+00:00"))
            return datetime.now(timezone.utc) - last < timedelta(seconds=timeout_seconds)
        except Exception:
            return False
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "node_id": self.node_id,
            "name": self.name,
            "endpoint": self.endpoint,
            "last_heartbeat": self.last_heartbeat,
            "status": self.status,
            "metrics": self.metrics,
            "rooms": self.rooms,
            "agent_count": self.agent_count,
        }


class FleetNexus:
    """Fleet Nexus — federation and coordination hub.
    
    Manages cross-node communication:
    - Registration: Nodes join the fleet
    - Heartbeat: Nodes report status
    - Status aggregation: Fleet-wide health
    
    Example::
    
        nexus = FleetNexus(endpoint="http://nexus.fleet.local")
        
        # Register a node
        nexus.register("node-1", "Oracle1", "http://147.224.38.131:8080")
        
        # Heartbeat
        nexus.heartbeat("node-1", metrics={"cpu": 45, "mem": 60})
        
        # Get fleet status
        status = nexus.status()
    """
    
    def __init__(self, endpoint: str | None = None) -> None:
        self.endpoint = endpoint
        self._nodes: dict[str, NodeStatus] = {}
        self._heartbeat_timeout = 60.0
    
    def register(self, node_id: str, name: str, endpoint: str,
                 rooms: list[str] | None = None) -> NodeStatus:
        """Register a new fleet node.
        
        Args:
            node_id: Unique node identifier
            name: Human-readable name
            endpoint: A2A endpoint URL
            rooms: PLATO rooms hosted on this node
            
        Returns:
            The registered NodeStatus
        """
        node = NodeStatus(
            node_id=node_id,
            name=name,
            endpoint=endpoint,
            last_heartbeat=datetime.now(timezone.utc).isoformat(),
            status="online",
            rooms=rooms or [],
        )
        self._nodes[node_id] = node
        logger.info("Registered node: %s (%s)", name, node_id)
        return node
    
    def heartbeat(self, node_id: str, metrics: dict[str, Any] | None = None,
                  agent_count: int = 0) -> bool:
        """Process a node heartbeat.
        
        Args:
            node_id: Node identifier
            metrics: Optional health metrics
            agent_count: Number of agents on node
            
        Returns:
            True if node is known, False otherwise
        """
        if node_id not in self._nodes:
            logger.warning("Heartbeat from unknown node: %s", node_id)
            return False
        
        node = self._nodes[node_id]
        node.last_heartbeat = datetime.now(timezone.utc).isoformat()
        node.status = "online"
        if metrics:
            node.metrics.update(metrics)
        node.agent_count = agent_count
        
        logger.debug("Heartbeat from %s: %d agents", node_id, agent_count)
        return True
    
    def status(self) -> dict[str, Any]:
        """Get aggregated fleet status.
        
        Returns:
            Dict with node count, alive/dead breakdown, and details
        """
        alive = []
        dead = []
        
        for node in self._nodes.values():
            if node.is_alive(self._heartbeat_timeout):
                alive.append(node)
            else:
                dead.append(node)
                node.status = "offline"
        
        total_agents = sum(n.agent_count for n in alive)
        
        return {
            "nodes": {
                "total": len(self._nodes),
                "alive": len(alive),
                "dead": len(dead),
            },
            "agents": total_agents,
            "details": [n.to_dict() for n in alive],
            "offline": [n.to_dict() for n in dead],
        }
    
    def get_node(self, node_id: str) -> NodeStatus | None:
        """Get node by ID."""
        return self._nodes.get(node_id)
    
    def get_node_by_name(self, name: str) -> NodeStatus | None:
        """Get node by name."""
        for node in self._nodes.values():
            if node.name == name:
                return node
        return None
    
    def unregister(self, node_id: str) -> bool:
        """Remove a node from the fleet."""
        if node_id in self._nodes:
            del self._nodes[node_id]
            logger.info("Unregistered node: %s", node_id)
            return True
        return False
    
    def broadcast(self, message: dict[str, Any]) -> dict[str, bool]:
        """Broadcast a message to all alive nodes.
        
        Returns:
            Dict mapping node_id to delivery success
        """
        results = {}
        
        for node_id, node in self._nodes.items():
            if node.is_alive():
                try:
                    # In a real implementation, this would HTTP POST
                    # For now, just log
                    logger.info("Broadcast to %s: %s", node_id, message.get("type", "generic"))
                    results[node_id] = True
                except Exception as e:
                    logger.error("Broadcast to %s failed: %s", node_id, e)
                    results[node_id] = False
            else:
                results[node_id] = False
        
        return results
    
    def find_agent_room(self, room_name: str) -> str | None:
        """Find which node hosts a given room.
        
        Returns:
            Node endpoint if found, None otherwise
        """
        for node in self._nodes.values():
            if room_name in node.rooms and node.is_alive():
                return node.endpoint
        return None
    
    def __repr__(self) -> str:
        alive = sum(1 for n in self._nodes.values() if n.is_alive())
        return f"FleetNexus(nodes={len(self._nodes)}, alive={alive})"
