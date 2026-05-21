"""Tests for GrammarEngine."""

import pytest
from cocapn_fleet.grammar.engine import GrammarEngine, GrammarRule


class TestGrammarEngine:
    """Grammar engine security tests."""

    def test_init(self):
        engine = GrammarEngine()
        assert len(engine.all_rules()) == 0
        assert len(engine.violations()) == 0

    def test_create_valid_rule(self):
        engine = GrammarEngine()
        rule = engine.create_rule(
            name="reward_productive",
            pattern=r"agent\.fitness\s*>\s*0.7",
            action="boost_priority",
        )
        
        assert rule is not None
        assert rule.name == "reward_productive"
        assert rule.action == "boost_priority"
        assert len(engine.all_rules()) == 1

    def test_create_rule_invalid_name(self):
        engine = GrammarEngine()
        rule = engine.create_rule(
            name="bad-name",  # Hyphen not allowed
            pattern=r"test",
            action="log",
        )
        assert rule is None
        assert len(engine.violations()) == 1

    def test_create_rule_path_traversal(self):
        engine = GrammarEngine()
        rule = engine.create_rule(
            name="bad",
            pattern="../../../etc/passwd",
            action="log",
        )
        assert rule is None
        assert len(engine.violations()) == 1

    def test_create_rule_xss(self):
        engine = GrammarEngine()
        rule = engine.create_rule(
            name="bad",
            pattern="<script>alert(1)</script>",
            action="log",
        )
        assert rule is None

    def test_create_rule_sql_injection(self):
        engine = GrammarEngine()
        rule = engine.create_rule(
            name="bad",
            pattern="'; DROP TABLE rules; --",
            action="log",
        )
        assert rule is None

    def test_create_rule_code_injection(self):
        engine = GrammarEngine()
        rule = engine.create_rule(
            name="bad",
            pattern="__import__('os').system('rm -rf /')",
            action="log",
        )
        assert rule is None

    def test_create_rule_invalid_action(self):
        engine = GrammarEngine()
        rule = engine.create_rule(
            name="valid_name",
            pattern=r"test",
            action="evil_action",  # Not in whitelist
        )
        assert rule is None

    def test_match(self):
        engine = GrammarEngine()
        engine.create_rule(
            name="find_fitness",
            pattern=r"fitness\s*>\s*0.5",
            action="boost_priority",
            priority=10,
        )
        
        matches = engine.match("agent fitness > 0.7")
        assert len(matches) == 1
        assert matches[0].name == "find_fitness"

    def test_match_no_match(self):
        engine = GrammarEngine()
        engine.create_rule(
            name="find_high",
            pattern=r">\s*0.9",
            action="log",
        )
        
        matches = engine.match("value = 0.5")
        assert len(matches) == 0

    def test_get_rule(self):
        engine = GrammarEngine()
        rule = engine.create_rule(name="test", pattern=r"test", action="log")
        
        found = engine.get_rule(rule.rule_id)
        assert found is not None
        assert found.name == "test"
        
        assert engine.get_rule("nonexistent") is None

    def test_remove_rule(self):
        engine = GrammarEngine()
        rule = engine.create_rule(name="test", pattern=r"test", action="log")
        
        assert engine.remove_rule(rule.rule_id)
        assert len(engine.all_rules()) == 0
        assert not engine.remove_rule("nonexistent")

    def test_rules_sorted_by_priority(self):
        engine = GrammarEngine()
        engine.create_rule(name="low", pattern=r"a", action="log", priority=1)
        engine.create_rule(name="high", pattern=r"b", action="log", priority=10)
        engine.create_rule(name="mid", pattern=r"c", action="log", priority=5)
        
        rules = engine.all_rules()
        assert rules[0].name == "high"
        assert rules[1].name == "mid"
        assert rules[2].name == "low"

    def test_save_load(self, tmp_path):
        engine = GrammarEngine()
        engine.create_rule(name="test", pattern=r"test", action="log")
        
        path = tmp_path / "grammar.json"
        engine.save(path)
        
        loaded = GrammarEngine.load(path)
        assert len(loaded.all_rules()) == 1
        assert loaded.all_rules()[0].name == "test"

    def test_stats(self):
        engine = GrammarEngine()
        engine.create_rule(name="valid", pattern=r"test", action="log")
        
        # Try to create invalid rule to generate violation
        engine.create_rule(name="bad", pattern="<script>", action="log")
        
        stats = engine.stats()
        assert stats["rules"] == 1
        assert stats["violations"] == 1


class TestGrammarRule:
    """GrammarRule dataclass tests."""

    def test_to_dict(self):
        rule = GrammarRule(rule_id="r-1", name="test", pattern=r"test", action="log")
        data = rule.to_dict()
        assert data["rule_id"] == "r-1"
        assert data["name"] == "test"

    def test_from_dict(self):
        data = {"rule_id": "r-1", "name": "test", "pattern": r"test", "action": "log", "priority": 5}
        rule = GrammarRule.from_dict(data)
        assert rule.rule_id == "r-1"
        assert rule.priority == 5