"""TrinityScore — Ethos × Pathos × Logos = Fitness.

The trinity scoring system evaluates agents across three dimensions:
- Ethos: Hardware fitness (thermal, memory, GPU utilization)
- Pathos: Human satisfaction (task completion, latency, feedback)
- Logos: Code quality (test pass rate, proof coverage, complexity)

Fitness = product of normalized scores. Agents with product > threshold survive.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any

from ..core.dna import Agent


@dataclass
class DimensionScore:
    """Score for a single trinity dimension."""
    
    raw: float = 0.0
    normalized: float = 0.0
    weight: float = 1.0
    details: dict[str, float] = None
    
    def __post_init__(self) -> None:
        if self.details is None:
            self.details = {}


@dataclass 
class TrinityResult:
    """Complete trinity evaluation result."""
    
    ethos: DimensionScore
    pathos: DimensionScore
    logos: DimensionScore
    product: float = 0.0
    status: str = "UNKNOWN"
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "ethos": {
                "raw": self.ethos.raw,
                "normalized": self.ethos.normalized,
                "weight": self.ethos.weight,
                "details": self.ethos.details,
            },
            "pathos": {
                "raw": self.pathos.raw,
                "normalized": self.pathos.normalized,
                "weight": self.pathos.weight,
                "details": self.pathos.details,
            },
            "logos": {
                "raw": self.logos.raw,
                "normalized": self.logos.normalized,
                "weight": self.logos.weight,
                "details": self.logos.details,
            },
            "product": self.product,
            "status": self.status,
        }


class EthosScorer:
    """Hardware fitness scoring.
    
    Measures: thermal pressure, memory efficiency, GPU utilization,
    power draw, hardware longevity.
    """
    
    def score(self, agent: Agent) -> DimensionScore:
        """Score agent hardware fitness.
        
        Returns:
            DimensionScore with normalized 0-1 value
        """
        meta = agent.meta.get("hardware", {})
        
        # Extract metrics
        thermal = meta.get("thermal_pressure", 0.5)  # 0=hot, 1=cool
        memory = meta.get("memory_efficiency", 0.7)   # 0=wasted, 1=optimal
        gpu = meta.get("gpu_utilization", 0.6)        # 0=idle, 1=maxed
        power = meta.get("power_efficiency", 0.8)    # 0=hog, 1=lean
        
        # Penalize thermal throttling heavily
        thermal_score = 1.0 - max(0.0, thermal - 0.3) / 0.7
        
        # Weighted combination
        raw = (
            thermal_score * 0.35 +
            memory * 0.25 +
            gpu * 0.20 +
            power * 0.20
        )
        
        # Normalize with sigmoid for sharp cutoff
        normalized = 1.0 / (1.0 + math.exp(-5.0 * (raw - 0.6)))
        
        return DimensionScore(
            raw=raw,
            normalized=normalized,
            weight=0.35,
            details={
                "thermal": thermal_score,
                "memory": memory,
                "gpu": gpu,
                "power": power,
            }
        )


class PathosScorer:
    """Human satisfaction scoring.
    
    Measures: task completion rate, latency, user feedback,
    interaction quality, goal achievement.
    """
    
    def score(self, agent: Agent) -> DimensionScore:
        """Score agent human satisfaction."""
        meta = agent.meta.get("human", {})
        
        completion = meta.get("task_completion_rate", 0.8)
        latency_score = 1.0 - min(1.0, meta.get("avg_latency_ms", 500) / 1000)
        feedback = meta.get("user_feedback", 0.7)
        goals = meta.get("goal_achievement", 0.75)
        
        # Latency is critical — quadratic penalty
        latency_penalty = latency_score ** 2
        
        raw = (
            completion * 0.30 +
            latency_penalty * 0.30 +
            feedback * 0.25 +
            goals * 0.15
        )
        
        normalized = 1.0 / (1.0 + math.exp(-4.0 * (raw - 0.5)))
        
        return DimensionScore(
            raw=raw,
            normalized=normalized,
            weight=0.35,
            details={
                "completion": completion,
                "latency": latency_score,
                "feedback": feedback,
                "goals": goals,
            }
        )


class LogosScorer:
    """Code quality scoring.
    
    Measures: test pass rate, proof coverage, complexity,
    documentation, type safety.
    """
    
    def score(self, agent: Agent) -> DimensionScore:
        """Score agent code quality."""
        meta = agent.meta.get("code", {})
        
        tests = meta.get("test_pass_rate", 0.9)
        proofs = meta.get("proof_coverage", 0.6)
        complexity = 1.0 - min(1.0, meta.get("cyclomatic_complexity", 20) / 50)
        docs = meta.get("documentation_score", 0.7)
        types = meta.get("type_coverage", 0.8)
        
        # Proofs are rare but valuable — sigmoid boost
        proof_boost = 1.0 / (1.0 + math.exp(-8.0 * (proofs - 0.5)))
        
        raw = (
            tests * 0.25 +
            proof_boost * 0.30 +
            complexity * 0.20 +
            docs * 0.15 +
            types * 0.10
        )
        
        normalized = 1.0 / (1.0 + math.exp(-5.0 * (raw - 0.55)))
        
        return DimensionScore(
            raw=raw,
            normalized=normalized,
            weight=0.30,
            details={
                "tests": tests,
                "proofs": proofs,
                "complexity": complexity,
                "docs": docs,
                "types": types,
            }
        )


class TrinityScore:
    """Unified trinity fitness scorer.
    
    Evaluates agents across ethos, pathos, and logos dimensions.
    The product of normalized scores determines survival.
    
    Example::
    
        scorer = TrinityScore()
        result = scorer.score(agent)
        
        if result.status == "SURVIVE":
            print(f"Agent survives with fitness {result.product:.3f}")
    """
    
    SURVIVE_THRESHOLD = 0.45
    BREED_THRESHOLD = 0.65
    
    def __init__(self) -> None:
        self.ethos = EthosScorer()
        self.pathos = PathosScorer()
        self.logos = LogosScorer()
    
    def score(self, agent: Agent) -> TrinityResult:
        """Evaluate an agent's complete fitness.
        
        Args:
            agent: Agent to evaluate
            
        Returns:
            TrinityResult with dimension scores and survival status
        """
        e = self.ethos.score(agent)
        p = self.pathos.score(agent)
        l = self.logos.score(agent)
        
        # Product of normalized scores
        product = e.normalized * p.normalized * l.normalized
        
        # Determine status
        if product < self.SURVIVE_THRESHOLD:
            status = "SUNSET"
        elif product < self.BREED_THRESHOLD:
            status = "SURVIVE"
        else:
            status = "BREED"
        
        return TrinityResult(
            ethos=e,
            pathos=p,
            logos=l,
            product=product,
            status=status,
        )
    
    def batch_score(self, agents: list[Agent]) -> list[TrinityResult]:
        """Score multiple agents efficiently."""
        return [self.score(a) for a in agents]
    
    def tournament(self, agents: list[Agent], 
                   tournament_size: int = 4) -> list[tuple[Agent, TrinityResult]]:
        """Run a tournament to select top agents.
        
        Divides agents into random tournaments and returns
        winners sorted by fitness product.
        
        Args:
            agents: All competing agents
            tournament_size: Agents per tournament round
            
        Returns:
            Sorted list of (Agent, TrinityResult) winners
        """
        import random
        
        if len(agents) < tournament_size:
            tournament_size = max(2, len(agents))
        
        # Shuffle and divide into tournaments
        shuffled = agents.copy()
        random.shuffle(shuffled)
        
        winners: list[tuple[Agent, TrinityResult]] = []
        for i in range(0, len(shuffled), tournament_size):
            group = shuffled[i:i + tournament_size]
            scored = [(a, self.score(a)) for a in group]
            scored.sort(key=lambda x: x[1].product, reverse=True)
            winners.append(scored[0])
        
        winners.sort(key=lambda x: x[1].product, reverse=True)
        return winners
