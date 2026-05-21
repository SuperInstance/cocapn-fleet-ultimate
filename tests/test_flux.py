"""Tests for FLUXChecker."""

import pytest
from cocapn_fleet.flux.checker import FLUXChecker, ProofCertificate, ConstraintViolation
from cocapn_fleet.core.dna import Agent


class TestFLUXChecker:
    """FLUX constraint checking tests."""

    def test_check_pass(self):
        flux = FLUXChecker()
        cert = flux.check("temperature < 300", reading=295.4, domain="aviation")
        
        assert cert.result == "PASS"
        assert cert.constraint == "temperature < 300"
        assert cert.domain == "aviation"
        assert cert.verify()

    def test_check_fail(self):
        flux = FLUXChecker()
        cert = flux.check("temperature < 300", reading=305.0, domain="aviation")
        
        assert cert.result == "FAIL"
        assert cert.verify()

    def test_check_greater_than(self):
        flux = FLUXChecker()
        cert = flux.check("pressure > 0.8", reading=0.9, domain="aviation")
        assert cert.result == "PASS"

    def test_check_equal(self):
        flux = FLUXChecker()
        cert = flux.check("altitude == 35000", reading=35000.0, domain="aviation")
        assert cert.result == "PASS"

    def test_check_not_equal(self):
        flux = FLUXChecker()
        cert = flux.check("status != 0", reading=1.0)
        assert cert.result == "PASS"

    def test_check_less_equal(self):
        flux = FLUXChecker()
        cert = flux.check("temp <= 300", reading=300.0)
        assert cert.result == "PASS"

    def test_check_greater_equal(self):
        flux = FLUXChecker()
        cert = flux.check("temp >= 300", reading=300.0)
        assert cert.result == "PASS"

    def test_certificate_integrity(self):
        cert = ProofCertificate(
            constraint="test < 100",
            result="PASS",
            domain="test",
        )
        assert cert.verify()
        
        # Tamper
        cert.result = "FAIL"
        assert not cert.verify()

    def test_audit(self):
        flux = FLUXChecker()
        
        agents = []
        for i in range(5):
            agent = Agent(agent_id=i, name=f"agent-{i}", vector=[0.1])
            agent.meta = {"constraints": {"cpu_temp": 95.0 if i == 0 else 50.0}}
            agents.append(agent)
        
        violations = flux.audit(agents)
        assert len(violations) == 1  # Only agent-0 exceeds 85.0
        assert violations[0].agent_id == 0
        assert violations[0].severity in ["warning", "error"]

    def test_history(self):
        flux = FLUXChecker()
        flux.check("a < 10", reading=5.0)
        flux.check("b > 20", reading=25.0)
        
        history = flux.history()
        assert len(history) == 2
        assert history[0].constraint == "a < 10"

    def test_stats(self):
        flux = FLUXChecker()
        flux.check("a < 10", reading=5.0)
        flux.check("a < 10", reading=15.0)
        
        stats = flux.stats()
        assert stats["total_checks"] == 2
        assert stats["passes"] == 1
        assert stats["fails"] == 1
        assert stats["pass_rate"] == 0.5

    def test_domain_presets(self):
        flux = FLUXChecker()
        
        assert "aviation" in flux.PRESETS
        assert "thermal" in flux.PRESETS
        assert "memory" in flux.PRESETS
        
        # Check aviation bounds
        aviation = flux.PRESETS["aviation"]
        assert "temperature" in aviation
        assert aviation["temperature"] == (200.0, 300.0)
