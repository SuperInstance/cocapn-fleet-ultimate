"""Test fixtures and utilities."""

import pytest
from cocapn_fleet import FleetCore, FleetConfig
from cocapn_fleet.core.dna import AgentDNA
from cocapn_fleet.trinity.scorer import TrinityScore
from cocapn_fleet.flux.checker import FLUXChecker
from cocapn_fleet.plato.room import PLATORoom
from cocapn_fleet.grammar.engine import GrammarEngine
from cocapn_fleet.nexus.federation import FleetNexus


@pytest.fixture
def fleet():
    """Create a test fleet with small dimensions."""
    return FleetCore(FleetConfig(dim=64, name="test-fleet"))


@pytest.fixture
def dna():
    """Create a test DNA index."""
    return AgentDNA(dim=64, bit_width=4)


@pytest.fixture
def scorer():
    """Create a trinity scorer."""
    return TrinityScore()


@pytest.fixture
def flux():
    """Create a FLUX checker."""
    return FLUXChecker()


@pytest.fixture
def room():
    """Create a PLATO room."""
    return PLATORoom(name="test-room")


@pytest.fixture
def grammar():
    """Create a grammar engine."""
    return GrammarEngine()


@pytest.fixture
def nexus():
    """Create a fleet nexus."""
    return FleetNexus()
