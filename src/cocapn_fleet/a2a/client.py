"""A2A Client — Agent-to-Agent Protocol Client.

Implements the A2A protocol for task delegation between agents.
All communication is JSON-native and machine-parseable.
"""

from __future__ import annotations

import json
import logging
import uuid
from dataclasses import dataclass, field
from typing import Any, AsyncIterator

logger = logging.getLogger(__name__)


@dataclass
class AgentCard:
    """A2A Agent Card — published at /.well-known/agent.json"""
    
    name: str
    version: str
    capabilities: dict[str, dict[str, Any]] = field(default_factory=dict)
    endpoint: str = ""
    authentication: dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "version": self.version,
            "capabilities": self.capabilities,
            "endpoint": self.endpoint,
            "authentication": self.authentication,
        }
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "AgentCard":
        return cls(**{k: data.get(k, default) for k, default in {
            "name": "", "version": "", "capabilities": {},
            "endpoint": "", "authentication": {},
        }.items()})


@dataclass
class Task:
    """A2A Task — the unit of delegation."""
    
    task_id: str = ""
    type: str = ""
    input: dict[str, Any] = field(default_factory=dict)
    status: str = "pending"
    artefacts: list[dict[str, Any]] = field(default_factory=list)
    created_at: str = ""
    
    def __post_init__(self) -> None:
        if not self.task_id:
            self.task_id = str(uuid.uuid4())
        if not self.created_at:
            from datetime import datetime, timezone
            self.created_at = datetime.now(timezone.utc).isoformat()
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "task_id": self.task_id,
            "type": self.type,
            "input": self.input,
            "status": self.status,
            "artefacts": self.artefacts,
            "created_at": self.created_at,
        }


@dataclass
class A2AMessage:
    """A2A Message — typed communication between agents."""
    
    sender: str = ""
    recipient: str = ""
    message_type: str = "task"  # task, status, artefact, error
    payload: dict[str, Any] = field(default_factory=dict)
    timestamp: str = ""
    
    def __post_init__(self) -> None:
        if not self.timestamp:
            from datetime import datetime, timezone
            self.timestamp = datetime.now(timezone.utc).isoformat()
    
    def to_json(self) -> str:
        return json.dumps({
            "sender": self.sender,
            "recipient": self.recipient,
            "type": self.message_type,
            "payload": self.payload,
            "timestamp": self.timestamp,
        })
    
    @classmethod
    def from_json(cls, data: str) -> "A2AMessage":
        d = json.loads(data)
        return cls(
            sender=d.get("sender", ""),
            recipient=d.get("recipient", ""),
            message_type=d.get("type", "task"),
            payload=d.get("payload", {}),
            timestamp=d.get("timestamp", ""),
        )


class A2AClient:
    """A2A Protocol Client.
    
    Sends tasks to other agents and receives results.
    All communication is JSON-native.
    
    Example::
    
        client = A2AClient(agent_name="explorer")
        
        # Discover another agent
        card = await client.discover("http://flux.local/.well-known/agent.json")
        
        # Send a task
        result = await client.send_task(card, {
            "type": "check",
            "input": {"constraint": "temp < 300", "reading": 295}
        })
    """
    
    def __init__(self, agent_name: str, endpoint: str = "") -> None:
        self.agent_name = agent_name
        self.endpoint = endpoint
        self._registry: dict[str, AgentCard] = {}
        self._pending: dict[str, Task] = {}
        self._history: list[A2AMessage] = []
    
    async def discover(self, url: str) -> AgentCard:
        """Fetch an Agent Card from a well-known endpoint."""
        try:
            import httpx
            async with httpx.AsyncClient() as client:
                resp = await client.get(url, timeout=10.0)
                resp.raise_for_status()
                data = resp.json()
                card = AgentCard.from_dict(data)
                self._registry[card.name] = card
                logger.info("Discovered agent: %s at %s", card.name, card.endpoint)
                return card
        except Exception as e:
            logger.error("Discovery failed for %s: %s", url, e)
            raise
    
    async def send_task(self, card: AgentCard, task_data: dict[str, Any],
                        streaming: bool = False) -> Task | AsyncIterator[Task]:
        """Send a task to another agent.
        
        Args:
            card: Target agent's AgentCard
            task_data: Task specification
            streaming: If True, yields progress updates
            
        Returns:
            Completed Task or AsyncIterator of updates
        """
        task = Task(type=task_data.get("type", "generic"), input=task_data.get("input", {}))
        self._pending[task.task_id] = task
        
        message = A2AMessage(
            sender=self.agent_name,
            recipient=card.name,
            message_type="task",
            payload=task.to_dict(),
        )
        self._history.append(message)
        
        try:
            import httpx
            async with httpx.AsyncClient() as client:
                resp = await client.post(
                    f"{card.endpoint}/tasks/send",
                    json=task.to_dict(),
                    timeout=60.0,
                )
                resp.raise_for_status()
                result_data = resp.json()
                
                task.status = result_data.get("status", "completed")
                task.artefacts = result_data.get("artefacts", [])
                
                del self._pending[task.task_id]
                logger.info("Task %s completed by %s", task.task_id, card.name)
                return task
                
        except Exception as e:
            task.status = "failed"
            logger.error("Task %s failed: %s", task.task_id, e)
            del self._pending[task.task_id]
            raise
    
    async def send_task_sync(self, card: AgentCard, task_data: dict[str, Any]) -> Task:
        """Synchronous wrapper for send_task."""
        import asyncio
        return await self.send_task(card, task_data, streaming=False)
    
    def register_local(self, card: AgentCard) -> None:
        """Register a local agent (no network needed)."""
        self._registry[card.name] = card
        logger.info("Registered local agent: %s", card.name)
    
    def get_card(self, name: str) -> AgentCard | None:
        """Get a registered agent's card."""
        return self._registry.get(name)
    
    def history(self) -> list[A2AMessage]:
        """Return message history."""
        return self._history.copy()
    
    def pending(self) -> list[Task]:
        """Return pending tasks."""
        return list(self._pending.values())
