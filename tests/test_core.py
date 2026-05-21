"""Tests for FleetCore."""

import pytest
from cocapn_fleet import FleetCore, FleetConfig


class TestFleetCore:
    """FleetCore integration tests."""

    def test_init(self):
        fleet = FleetCore(FleetConfig(dim=64, name="test"))
        assert fleet.config.name == "test"
        assert fleet.config.dim == 64
        assert len(fleet.rooms) == 8
        assert fleet.flux is not None
        assert fleet.breeding is not None

    def test_welcome(self):
        fleet = FleetCore(FleetConfig(dim=64))
        status = fleet.welcome()
        assert "test-fleet" in status or "fleet" in status
        assert "version" in status

    def test_spawn(self):
        fleet = FleetCore(FleetConfig(dim=64))
        agent = fleet.spawn(name="test-agent", room="harbor")
        assert agent.name == "test-agent"
        assert agent.room == "harbor"
        assert agent.agent_id == 1
        assert len(agent.vector) == 64

    def test_spawn_multiple(self):
        fleet = FleetCore(FleetConfig(dim=64))
        for i in range(5):
            fleet.spawn(name=f"agent-{i}")
        assert len(fleet.dna) == 5

    def test_tick(self):
        fleet = FleetCore(FleetConfig(dim=64))
        fleet.spawn(name="agent-1")
        result = fleet.tick()
        assert "generation" in result
        assert "events" in result
        assert "stats" in result

    def test_save_load(self, tmp_path):
        fleet = FleetCore(FleetConfig(dim=64))
        fleet.spawn(name="persistent")
        
        save_path = tmp_path / "state"
        fleet.save(save_path)
        
        loaded = FleetCore.load(save_path)
        assert loaded.config.name == fleet.config.name
        assert loaded.config.dim == 64

    def test_room_assignment(self):
        fleet = FleetCore(FleetConfig(dim=64))
        agent = fleet.spawn(name="explorer", room="forge")
        assert agent.room == "forge"
        assert agent.agent_id in fleet.rooms["forge"].agents()

    def test_disable_subsystems(self):
        fleet = FleetCore(FleetConfig(
            dim=64, enable_flux=False,
            enable_breeding=False, enable_grammar=False
        ))
        assert fleet.flux is None
        assert fleet.breeding is None
        assert fleet.grammar is None
