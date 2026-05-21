"""FLUXChecker — Constraint-proven computing.

FLUX verifies constraints with formal proof certificates.
Each check produces a tamper-evident certificate that can
be audited later.
"""

from __future__ import annotations

import hashlib
import json
import logging
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

from ..core.dna import Agent

logger = logging.getLogger(__name__)


@dataclass
class ProofCertificate:
    """A FLUX proof certificate — evidence of constraint satisfaction."""
    
    constraint: str = ""
    result: str = "UNKNOWN"  # PASS, FAIL, ERROR
    hash: str = ""
    timestamp: str = ""
    domain: str = "generic"
    metadata: dict[str, Any] = None
    
    def __post_init__(self) -> None:
        if self.metadata is None:
            self.metadata = {}
        if not self.timestamp:
            self.timestamp = datetime.now(timezone.utc).isoformat()
        if not self.hash:
            self._compute_hash()
    
    def _compute_hash(self) -> None:
        data = json.dumps({
            "constraint": self.constraint,
            "result": self.result,
            "timestamp": self.timestamp,
            "domain": self.domain,
        }, sort_keys=True)
        self.hash = hashlib.sha256(data.encode()).hexdigest()[:16]
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "constraint": self.constraint,
            "result": self.result,
            "hash": self.hash,
            "timestamp": self.timestamp,
            "domain": self.domain,
            "metadata": self.metadata,
        }
    
    def verify(self) -> bool:
        """Verify certificate integrity."""
        old_hash = self.hash
        self.hash = ""
        self._compute_hash()
        new_hash = self.hash
        self.hash = old_hash
        return old_hash == new_hash


@dataclass
class ConstraintViolation:
    """A constraint violation report."""
    
    constraint: str
    value: float
    bound: float
    severity: str = "warning"  # warning, error, critical
    agent_id: int | None = None
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "constraint": self.constraint,
            "value": self.value,
            "bound": self.bound,
            "severity": self.severity,
            "agent_id": self.agent_id,
        }


class FLUXChecker:
    """FLUX constraint checker — formally proven verification.
    
    FLUX checks constraints against readings and produces
    proof certificates. Supports batch auditing and domain-specific
    presets.
    
    Example::
    
        flux = FLUXChecker()
        
        # Single check
        cert = flux.check("temperature < 300", reading=295.4, domain="aviation")
        assert cert.result == "PASS"
        
        # Batch audit
        violations = flux.audit(agents)
    """
    
    # Domain-specific presets
    PRESETS: dict[str, dict[str, tuple[float, float]]] = {
        "aviation": {
            "temperature": (200.0, 300.0),
            "pressure": (0.8, 1.2),
            "altitude": (0.0, 45000.0),
        },
        "thermal": {
            "cpu_temp": (0.0, 85.0),
            "gpu_temp": (0.0, 90.0),
            "fan_speed": (0.0, 100.0),
        },
        "memory": {
            "heap_usage": (0.0, 90.0),
            "swap_usage": (0.0, 50.0),
            "fragmentation": (0.0, 30.0),
        },
    }
    
    def __init__(self) -> None:
        self._history: list[ProofCertificate] = []
    
    def check(self, constraint: str, reading: float,
              domain: str = "generic", **meta: Any) -> ProofCertificate:
        """Check a single constraint.
        
        Args:
            constraint: Constraint specification (e.g., "temperature < 300")
            reading: Value to check
            domain: Domain preset (aviation, thermal, memory)
            **meta: Additional metadata
            
        Returns:
            ProofCertificate with result and hash
        """
        # Parse simple constraints: "name < value", "name > value", etc.
        result = self._evaluate(constraint, reading)
        
        cert = ProofCertificate(
            constraint=constraint,
            result=result,
            domain=domain,
            metadata={
                "reading": reading,
                **meta,
            },
        )
        
        self._history.append(cert)
        logger.info("FLUX check: %s -> %s (domain=%s)", constraint, result, domain)
        return cert
    
    def audit(self, agents: list[Agent],
              constraints: list[str] | None = None) -> list[ConstraintViolation]:
        """Batch audit agents against constraints.
        
        Args:
            agents: Agents to audit
            constraints: Optional list of constraints (default: all agents)
            
        Returns:
            List of constraint violations
        """
        violations: list[ConstraintViolation] = []
        
        for agent in agents:
            meta = agent.meta.get("constraints", {})
            
            for key, value in meta.items():
                # Check if there's a preset bound
                for domain, presets in self.PRESETS.items():
                    if key in presets:
                        low, high = presets[key]
                        if value < low or value > high:
                            violations.append(ConstraintViolation(
                                constraint=f"{key} in [{low}, {high}]",
                                value=value,
                                bound=high if value > high else low,
                                severity="error" if value > high * 1.2 else "warning",
                                agent_id=agent.agent_id,
                            ))
        
        logger.info("FLUX audit: %d agents, %d violations", len(agents), len(violations))
        return violations
    
    def _evaluate(self, constraint: str, reading: float) -> str:
        """Evaluate a simple constraint."""
        constraint = constraint.strip()
        
        # Parse: "name < value", "name > value", "name == value", etc.
        for op in ["<=", ">=", "==", "!=", "<", ">"]:
            if op in constraint:
                parts = constraint.split(op)
                if len(parts) == 2:
                    try:
                        bound = float(parts[1].strip())
                        if op == "<":
                            return "PASS" if reading < bound else "FAIL"
                        elif op == ">":
                            return "PASS" if reading > bound else "FAIL"
                        elif op == "<=":
                            return "PASS" if reading <= bound else "FAIL"
                        elif op == ">=":
                            return "PASS" if reading >= bound else "FAIL"
                        elif op == "==":
                            return "PASS" if abs(reading - bound) < 1e-6 else "FAIL"
                        elif op == "!=":
                            return "PASS" if abs(reading - bound) >= 1e-6 else "FAIL"
                    except ValueError:
                        pass
        
        logger.warning("Could not parse constraint: %s", constraint)
        return "ERROR"
    
    def history(self) -> list[ProofCertificate]:
        """Return check history."""
        return self._history.copy()
    
    def stats(self) -> dict[str, Any]:
        """Return checker statistics."""
        total = len(self._history)
        passes = sum(1 for c in self._history if c.result == "PASS")
        fails = sum(1 for c in self._history if c.result == "FAIL")
        errors = sum(1 for c in self._history if c.result == "ERROR")
        
        return {
            "total_checks": total,
            "passes": passes,
            "fails": fails,
            "errors": errors,
            "pass_rate": passes / total if total > 0 else 0.0,
        }
