"""Cocapn Fleet — Unified Agent Ecosystem

This package brings together every fleet system into a single, coherent API:
- Turbovec DNA memory
- FLUX constraint checking
- PLATO room system
- A2A agent communication
- Trinity fitness scoring
- Breeding daemon
- Grammar engine
- Fleet nexus
"""

__version__ = "0.1.0"
__all__ = [
    "FleetCore",
    "AgentDNA",
    "TrinityScore",
    "A2AClient",
    "A2AServer",
    "PLATORoom",
    "FLUXChecker",
    "BreedingOrchestrator",
    "GrammarEngine",
    "FleetNexus",
]

from .core.fleet import FleetCore
from .core.dna import AgentDNA
from .trinity.scorer import TrinityScore
from .a2a.client import A2AClient
from .a2a.server import A2AServer
from .plato.room import PLATORoom
from .flux.checker import FLUXChecker
from .breeding.orchestrator import BreedingOrchestrator
from .grammar.engine import GrammarEngine
from .nexus.federation import FleetNexus
