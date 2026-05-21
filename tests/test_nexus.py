"""Tests for FleetNexus."""

import pytest
from cocapn_fleet.nexus.federation import FleetNexus, NodeStatus


class TestFleetNexus:
    """Fleet nexus federation tests."""

    def test_init(self):
        nexus = FleetNexus(endpoint="http://test.local")
        assert nexus.endpoint == "http://test.local"
        assert len(nexus.status()["details"]) == 0

    def test_register(self):
        nexus = FleetNexus()
        node = nexus.register("node-1", "Oracle1", "http://147.224.38.131")
        
        assert node.node_id == "node-1"
        assert node.name == "Oracle1"
        assert node.endpoint == "http://147.224.38.131"
        assert node.status == "online"

    def test_heartbeat(self):
        nexus = FleetNexus()
        nexus.register("node-1", "Oracle1", "http://147.224.38.131")
        
        result = nexus.heartbeat("node-1", metrics={"cpu": 45}, agent_count=10)
        assert result
        
        node = nexus.get_node("node-1")
        assert node.metrics["cpu"] == 45
        assert node.agent_count == 10

    def test_heartbeat_unknown_node(self):
        nexus = FleetNexus()
        result = nexus.heartbeat("unknown", metrics={"cpu": 50})
        assert not result

    def test_status(self):
        nexus = FleetNexus()
        nexus.register("node-1", "Oracle1", "http://147.224.38.131")
        nexus.register("node-2", "CCC", "http://ccc.local")
        
        status = nexus.status()
        assert status["nodes"]["total"] == 2
        assert status["nodes"]["alive"] == 2
        assert status["nodes"]["dead"] == 0

    def test_get_node(self):
        nexus = FleetNexus()
        nexus.register("node-1", "Oracle1", "http://147.224.38.131")
        
        found = nexus.get_node("node-1")
        assert found is not None
        assert found.name == "Oracle1"
        
        assert nexus.get_node("nonexistent") is None

    def test_get_node_by_name(self):
        nexus = FleetNexus()
        nexus.register("node-1", "Oracle1", "http://147.224.38.131")
        
        found = nexus.get_node_by_name("Oracle1")
        assert found is not None
        assert found.node_id == "node-1"
        
        assert nexus.get_node_by_name("Nonexistent") is None

    def test_unregister(self):
        nexus = FleetNexus()
        nexus.register("node-1", "Oracle1", "http://147.224.38.131")
        
        assert nexus.unregister("node-1")
        assert not nexus.unregister("node-1")
        assert nexus.status()["nodes"]["total"] == 0

    def test_broadcast(self):
        nexus = FleetNexus()
        nexus.register("node-1", "Oracle1", "http://147.224.38.131")
        nexus.register("node-2", "CCC", "http://ccc.local")
        
        results = nexus.broadcast({"type": "ping"})
        assert len(results) == 2
        assert results["node-1"]
        assert results["node-2"]

    def test_find_agent_room(self):
        nexus = FleetNexus()
        nexus.register("node-1", "Oracle1", "http://147.224.38.131", rooms=["harbor", "forge"])
        
        endpoint = nexus.find_agent_room("harbor")
        assert endpoint == "http://147.224.38.131"
        
        assert nexus.find_agent_room("nonexistent") is None

    def test_node_alive(self):
        node = NodeStatus(
            node_id="test",
            name="Test",
            endpoint="http://test.local",
            last_heartbeat="2026-05-22T02:00:00+00:00",
        )
        
        # Old heartbeat should be dead
        assert not node.is_alive(timeout_seconds=1.0)

    def test_repr(self):
        nexus = FleetNexus()
        nexus.register("node-1", "Oracle1", "http://147.224.38.131")
        
        rep = repr(nexus)
        assert "FleetNexus" in rep
        assert "nodes=1" in rep
        assert "alive=1" in rep