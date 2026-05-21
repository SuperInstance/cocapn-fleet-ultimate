"""Tests for TrinityScore."""

import pytest
from cocapn_fleet.core.dna import Agent
from cocapn_fleet.trinity.scorer import TrinityScore, EthosScorer, PathosScorer, LogosScorer


class TestTrinityScore:
    """Trinity scoring tests."""

    def test_ethos_scorer(self):
        scorer = EthosScorer()
        agent = Agent(agent_id=1, name="test", vector=[0.1])
        agent.meta = {"hardware": {
            "thermal_pressure": 0.2,
            "memory_efficiency": 0.8,
            "gpu_utilization": 0.6,
            "power_efficiency": 0.9,
        }}
        
        result = scorer.score(agent)
        assert 0.0 <= result.raw <= 1.0
        assert 0.0 <= result.normalized <= 1.0
        assert "thermal" in result.details

    def test_pathos_scorer(self):
        scorer = PathosScorer()
        agent = Agent(agent_id=1, name="test", vector=[0.1])
        agent.meta = {"human": {
            "task_completion_rate": 0.9,
            "avg_latency_ms": 200,
            "user_feedback": 0.8,
            "goal_achievement": 0.75,
        }}
        
        result = scorer.score(agent)
        assert 0.0 <= result.raw <= 1.0
        assert result.details["latency"] <= 1.0

    def test_logos_scorer(self):
        scorer = LogosScorer()
        agent = Agent(agent_id=1, name="test", vector=[0.1])
        agent.meta = {"code": {
            "test_pass_rate": 0.95,
            "proof_coverage": 0.7,
            "cyclomatic_complexity": 15,
            "documentation_score": 0.8,
            "type_coverage": 0.9,
        }}
        
        result = scorer.score(agent)
        assert 0.0 <= result.raw <= 1.0
        assert result.details["proofs"] == 0.7

    def test_trinity_score(self):
        scorer = TrinityScore()
        agent = Agent(agent_id=1, name="test", vector=[0.1])
        agent.meta = {
            "hardware": {"thermal_pressure": 0.2, "memory_efficiency": 0.8, "gpu_utilization": 0.6, "power_efficiency": 0.9},
            "human": {"task_completion_rate": 0.9, "avg_latency_ms": 200, "user_feedback": 0.8, "goal_achievement": 0.75},
            "code": {"test_pass_rate": 0.95, "proof_coverage": 0.7, "cyclomatic_complexity": 15, "documentation_score": 0.8, "type_coverage": 0.9},
        }
        
        result = scorer.score(agent)
        assert 0.0 <= result.product <= 1.0
        assert result.status in ["SUNSET", "SURVIVE", "BREED"]
        assert result.ethos.normalized >= 0.0
        assert result.pathos.normalized >= 0.0
        assert result.logos.normalized >= 0.0

    def test_trinity_product_formula(self):
        scorer = TrinityScore()
        agent = Agent(agent_id=1, name="test", vector=[0.1])
        agent.meta = {
            "hardware": {"thermal_pressure": 0.2, "memory_efficiency": 0.8, "gpu_utilization": 0.6, "power_efficiency": 0.9},
            "human": {"task_completion_rate": 0.9, "avg_latency_ms": 200, "user_feedback": 0.8, "goal_achievement": 0.75},
            "code": {"test_pass_rate": 0.95, "proof_coverage": 0.7, "cyclomatic_complexity": 15, "documentation_score": 0.8, "type_coverage": 0.9},
        }
        
        result = scorer.score(agent)
        expected_product = result.ethos.normalized * result.pathos.normalized * result.logos.normalized
        assert abs(result.product - expected_product) < 1e-10

    def test_batch_score(self):
        scorer = TrinityScore()
        agents = []
        for i in range(5):
            agent = Agent(agent_id=i, name=f"agent-{i}", vector=[0.1])
            agent.meta = {
                "hardware": {"thermal_pressure": 0.2, "memory_efficiency": 0.8, "gpu_utilization": 0.6, "power_efficiency": 0.9},
                "human": {"task_completion_rate": 0.9, "avg_latency_ms": 200, "user_feedback": 0.8, "goal_achievement": 0.75},
                "code": {"test_pass_rate": 0.95, "proof_coverage": 0.7, "cyclomatic_complexity": 15, "documentation_score": 0.8, "type_coverage": 0.9},
            }
            agents.append(agent)
        
        results = scorer.batch_score(agents)
        assert len(results) == 5
        for r in results:
            assert r.status in ["SUNSET", "SURVIVE", "BREED"]

    def test_tournament(self):
        scorer = TrinityScore()
        agents = []
        for i in range(8):
            agent = Agent(agent_id=i, name=f"agent-{i}", vector=[0.1])
            agent.fitness = i / 8.0
            agents.append(agent)
        
        winners = scorer.tournament(agents, tournament_size=4)
        assert len(winners) == 2
        assert winners[0][1].product >= winners[1][1].product

    def test_thresholds(self):
        scorer = TrinityScore()
        
        # Low fitness agent
        low = Agent(agent_id=1, name="low", vector=[0.1])
        low.meta = {
            "hardware": {"thermal_pressure": 0.9, "memory_efficiency": 0.2, "gpu_utilization": 0.2, "power_efficiency": 0.2},
            "human": {"task_completion_rate": 0.2, "avg_latency_ms": 900, "user_feedback": 0.2, "goal_achievement": 0.2},
            "code": {"test_pass_rate": 0.2, "proof_coverage": 0.1, "cyclomatic_complexity": 45, "documentation_score": 0.2, "type_coverage": 0.2},
        }
        result = scorer.score(low)
        assert result.status == "SUNSET"
        
        # High fitness agent
        high = Agent(agent_id=2, name="high", vector=[0.1])
        high.meta = {
            "hardware": {"thermal_pressure": 0.1, "memory_efficiency": 0.9, "gpu_utilization": 0.8, "power_efficiency": 0.9},
            "human": {"task_completion_rate": 0.95, "avg_latency_ms": 100, "user_feedback": 0.9, "goal_achievement": 0.9},
            "code": {"test_pass_rate": 0.98, "proof_coverage": 0.8, "cyclomatic_complexity": 10, "documentation_score": 0.9, "type_coverage": 0.95},
        }
        result = scorer.score(high)
        assert result.status == "BREED"
