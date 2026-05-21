"""Tests for BreedingOrchestrator."""

import pytest
from cocapn_fleet import FleetCore, FleetConfig
from cocapn_fleet.breeding.orchestrator import BreedingOrchestrator, BreedingEvent


class TestBreedingOrchestrator:
    """Breeding lifecycle tests."""

    def test_init(self):
        fleet = FleetCore(FleetConfig(dim=64))
        breeding = BreedingOrchestrator(fleet)
        
        assert breeding.generation == 0
        assert breeding.fleet == fleet
        assert breeding.tournament_size == 4

    def test_tick_increments_generation(self):
        fleet = FleetCore(FleetConfig(dim=64))
        breeding = fleet.breeding
        
        # Spawn agents with metadata
        for i in range(8):
            agent = fleet.spawn(name=f"agent-{i}")
            agent.meta = {
                "hardware": {"thermal_pressure": 0.2, "memory_efficiency": 0.8, "gpu_utilization": 0.6, "power_efficiency": 0.9},
                "human": {"task_completion_rate": 0.9, "avg_latency_ms": 200, "user_feedback": 0.8, "goal_achievement": 0.75},
                "code": {"test_pass_rate": 0.95, "proof_coverage": 0.7, "cyclomatic_complexity": 15, "documentation_score": 0.8, "type_coverage": 0.9},
            }
        
        result = breeding.tick()
        assert result["generation"] == 1
        assert "stats" in result
        assert "events" in result

    def test_tick_classifies_agents(self):
        fleet = FleetCore(FleetConfig(dim=64))
        
        # High fitness agent
        high = fleet.spawn(name="high")
        high.meta = {
            "hardware": {"thermal_pressure": 0.1, "memory_efficiency": 0.9, "gpu_utilization": 0.8, "power_efficiency": 0.9},
            "human": {"task_completion_rate": 0.95, "avg_latency_ms": 100, "user_feedback": 0.9, "goal_achievement": 0.9},
            "code": {"test_pass_rate": 0.98, "proof_coverage": 0.8, "cyclomatic_complexity": 10, "documentation_score": 0.9, "type_coverage": 0.95},
        }
        
        # Low fitness agent
        low = fleet.spawn(name="low")
        low.meta = {
            "hardware": {"thermal_pressure": 0.9, "memory_efficiency": 0.2, "gpu_utilization": 0.2, "power_efficiency": 0.2},
            "human": {"task_completion_rate": 0.2, "avg_latency_ms": 900, "user_feedback": 0.2, "goal_achievement": 0.2},
            "code": {"test_pass_rate": 0.2, "proof_coverage": 0.1, "cyclomatic_complexity": 45, "documentation_score": 0.2, "type_coverage": 0.2},
        }
        
        result = fleet.breeding.tick()
        stats = result["stats"]
        
        assert stats["total_agents"] >= 2
        assert stats["survivors"] + stats["sunset"] == 2

    def test_parent_selection(self):
        fleet = FleetCore(FleetConfig(dim=64))
        breeding = fleet.breeding
        
        agents = []
        for i in range(6):
            agent = fleet.spawn(name=f"parent-{i}")
            agent.fitness = i / 6.0
            agents.append(agent)
        
        breeders = [(a, breeding.scorer.score(a)) for a in agents]
        parents = breeding._select_parents(breeders)
        
        assert len(parents) >= 2
        assert len(parents) <= 6

    def test_spawn_child(self):
        fleet = FleetCore(FleetConfig(dim=64))
        breeding = fleet.breeding
        
        p1 = fleet.spawn(name="p1", vector=[0.5] * 64)
        p2 = fleet.spawn(name="p2", vector=[-0.5] * 64)
        
        child = breeding._spawn_child(p1, p2)
        
        assert child is not None
        assert child.generation == 1
        assert len(child.vector) == 64
        assert "p1" in child.name or "p2" in child.name

    def test_stats(self):
        fleet = FleetCore(FleetConfig(dim=64))
        breeding = fleet.breeding
        
        stats = breeding.stats()
        assert stats["generation"] == 0
        assert stats["active_agents"] == 0
        assert stats["total_sunset"] == 0

    def test_archive(self):
        fleet = FleetCore(FleetConfig(dim=64))
        breeding = fleet.breeding
        
        agent = fleet.spawn(name="archive-me")
        agent.meta = {
            "hardware": {"thermal_pressure": 0.9, "memory_efficiency": 0.2, "gpu_utilization": 0.2, "power_efficiency": 0.2},
            "human": {"task_completion_rate": 0.2, "avg_latency_ms": 900, "user_feedback": 0.2, "goal_achievement": 0.2},
            "code": {"test_pass_rate": 0.2, "proof_coverage": 0.1, "cyclomatic_complexity": 45, "documentation_score": 0.2, "type_coverage": 0.2},
        }
        
        fleet.tick()
        
        archive = breeding.get_archive()
        assert len(archive) >= 1
        assert archive[0].name == "archive-me"

    def test_event_structure(self):
        event = BreedingEvent(generation=1, event_type="survive", agent_id=42, agent_name="test")
        data = event.to_dict()
        
        assert data["generation"] == 1
        assert data["event_type"] == "survive"
        assert data["agent_id"] == 42
