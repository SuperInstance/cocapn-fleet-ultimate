"""Tests for AgentDNA."""

import pytest
import numpy as np
from cocapn_fleet.core.dna import AgentDNA, Agent


class TestAgentDNA:
    """AgentDNA unit tests."""

    def test_init(self):
        dna = AgentDNA(dim=64, bit_width=4)
        assert dna.dim == 64
        assert dna.bit_width == 4
        assert len(dna) == 0

    def test_add(self):
        dna = AgentDNA(dim=64)
        vector = np.random.randn(64).astype(np.float32).tolist()
        agent = dna.add(name="test", vector=vector)
        
        assert agent.name == "test"
        assert agent.agent_id == 1
        assert len(dna) == 1

    def test_add_invalid_dim(self):
        dna = AgentDNA(dim=64)
        with pytest.raises(ValueError):
            dna.add(name="bad", vector=[0.1] * 32)  # Wrong dimension

    def test_search(self):
        dna = AgentDNA(dim=64)
        
        # Add agents with known vectors
        v1 = np.ones(64, dtype=np.float32) * 0.5
        v2 = np.ones(64, dtype=np.float32) * -0.5
        
        dna.add(name="positive", vector=v1.tolist())
        dna.add(name="negative", vector=v2.tolist())
        
        # Search with positive vector
        results = dna.search(v1.tolist(), k=2)
        assert len(results) == 2
        assert results[0][0].name == "positive"

    def test_remove(self):
        dna = AgentDNA(dim=64)
        agent = dna.add(name="removable", vector=np.random.randn(64).tolist())
        
        assert dna.remove(agent.agent_id)
        assert len(dna) == 0
        assert not dna.remove(999)  # Non-existent

    def test_all(self):
        dna = AgentDNA(dim=64)
        for i in range(5):
            dna.add(name=f"agent-{i}", vector=np.random.randn(64).tolist())
        
        agents = dna.all()
        assert len(agents) == 5

    def test_get(self):
        dna = AgentDNA(dim=64)
        agent = dna.add(name="findable", vector=np.random.randn(64).tolist())
        
        found = dna.get(agent.agent_id)
        assert found is not None
        assert found.name == "findable"
        
        assert dna.get(999) is None

    def test_stats(self):
        dna = AgentDNA(dim=64, bit_width=4)
        dna.add(name="test", vector=np.random.randn(64).tolist())
        
        stats = dna.stats()
        assert stats["agents"] == 1
        assert stats["dim"] == 64
        assert stats["bit_width"] == 4
        assert "compression" in stats

    def test_save_load(self, tmp_path):
        dna = AgentDNA(dim=64)
        dna.add(name="persistent", vector=np.random.randn(64).tolist())
        
        path = tmp_path / "dna.tvim"
        dna.write(path)
        
        loaded = AgentDNA.load(path, dim=64)
        assert loaded.dim == 64
        assert len(loaded) == 1
        assert loaded.get(1).name == "persistent"

    def test_agent_to_dict(self):
        agent = Agent(agent_id=1, name="test", vector=[0.1, 0.2])
        data = agent.to_dict()
        assert data["agent_id"] == 1
        assert data["name"] == "test"
        
        restored = Agent.from_dict(data)
        assert restored.agent_id == 1
