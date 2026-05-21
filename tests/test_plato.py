"""Tests for PLATORoom."""

import pytest
from cocapn_fleet.plato.room import PLATORoom, Spell, Equipment
from cocapn_fleet.core.dna import Agent


class TestPLATORoom:
    """PLATO room tests."""

    def test_init(self):
        room = PLATORoom(name="test-room")
        assert room.name == "test-room"
        assert len(room.agents()) == 0
        assert len(room.spells()) == 10  # Standard spells

    def test_enter_leave(self):
        room = PLATORoom(name="test-room")
        agent = Agent(agent_id=1, name="test", vector=[0.1])
        
        room.enter(agent)
        assert agent.agent_id in room.agents()
        assert agent.room == "test-room"
        
        room.leave(agent)
        assert agent.agent_id not in room.agents()

    def test_cast_spell(self):
        room = PLATORoom(name="test-room")
        result = room.cast("summon_scout", target="mud")
        
        assert result["spell"] == "summon_scout"
        assert result["room"] == "test-room"
        assert result["status"] == "cast"

    def test_cast_unknown_spell(self):
        room = PLATORoom(name="test-room")
        with pytest.raises(ValueError):
            room.cast("nonexistent")

    def test_add_spell(self):
        room = PLATORoom(name="test-room")
        spell = Spell(name="custom", description="A custom spell", effect={"type": "custom"})
        
        room.add_spell(spell)
        assert len(room.spells()) == 11
        assert "custom" in [s.name for s in room.spells()]

    def test_equip(self):
        room = PLATORoom(name="test-room")
        equip = Equipment(name="analyzer", modifier={"detail": "high"})
        
        room.equip(equip)
        assert len(room._equipment) == 1

    def test_link(self):
        room = PLATORoom(name="harbor")
        room.link("forge")
        room.link("tide-pool")
        
        assert "forge" in room._federation_links
        assert "tide-pool" in room._federation_links
        
        # Duplicate link is ignored
        room.link("forge")
        assert len(room._federation_links) == 2

    def test_save_load(self, tmp_path):
        room = PLATORoom(name="test-room")
        agent = Agent(agent_id=1, name="test", vector=[0.1])
        room.enter(agent)
        
        path = tmp_path / "room.json"
        room.save(path)
        
        loaded = PLATORoom(name="test-room")
        loaded.load(path)
        
        assert loaded.name == "test-room"
        assert 1 in loaded.agents()

    def test_standard_spells(self):
        room = PLATORoom(name="test")
        spells = room.spells()
        spell_names = [s.name for s in spells]
        
        expected = ["summon_scout", "lightning_bolt", "shield", "scry",
                    "nexus_link", "baton_pass", "mirror_of_identity",
                    "pen_of_memory", "lens_of_architecture", "brush_of_design"]
        for name in expected:
            assert name in spell_names

    def test_repr(self):
        room = PLATORoom(name="test")
        assert "test" in repr(room)
        assert "agents=0" in repr(room)
