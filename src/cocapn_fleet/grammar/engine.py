"""GrammarEngine — Secure rule ingestion and pattern matching.

The grammar engine validates and stores behavioral rules for agents.
It enforces strict input validation to prevent chaos injection
(SQLi, XSS, path traversal, code execution).
"""

from __future__ import annotations

import json
import logging
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class GrammarRule:
    """A validated grammar rule."""
    
    rule_id: str
    name: str
    pattern: str
    action: str
    priority: int = 0
    meta: dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "rule_id": self.rule_id,
            "name": self.name,
            "pattern": self.pattern,
            "action": self.action,
            "priority": self.priority,
            "meta": self.meta,
        }
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "GrammarRule":
        return cls(**{k: data.get(k, default) for k, default in {
            "rule_id": "", "name": "", "pattern": "", "action": "",
            "priority": 0, "meta": {},
        }.items()})


class GrammarEngine:
    """Secure grammar rule engine.
    
    Validates all rule inputs to prevent injection attacks:
    - Name: alphanumeric + underscore only
    - Pattern: regex with timeout
    - Action: whitelist of safe actions
    
    Example::
    
        engine = GrammarEngine()
        
        # Safe rule
        engine.create_rule(
            name="reward_productive",
            pattern=r"agent\.fitness\s*>\s*0.7",
            action="boost_priority",
        )
        
        # Blocked: contains SQL injection
        engine.create_rule(
            name="bad_rule",
            pattern="'; DROP TABLE rules; --",  # REJECTED
            action="evil",
        )
    """
    
    # Whitelist of safe action types
    SAFE_ACTIONS: set[str] = {
        "boost_priority", "reduce_priority", "log", "notify",
        "spawn_child", "archive", "migrate", "tag",
    }
    
    # Blocked patterns (chaos vectors)
    BLOCKED_PATTERNS: list[tuple[str, str]] = [
        (r"\.\./", "path_traversal"),
        (r"<script", "xss"),
        (r"DROP\s+TABLE", "sql_injection"),
        (r"__import__|eval\(|exec\(", "code_injection"),
        (r"rm\s+-rf", "command_injection"),
        (r"\b(?:SELECT|INSERT|UPDATE|DELETE|UNION)\b", "sql_keyword"),
    ]
    
    def __init__(self) -> None:
        self._rules: dict[str, GrammarRule] = {}
        self._next_id = 1
        self._violation_log: list[dict[str, Any]] = []
    
    def create_rule(self, name: str, pattern: str, action: str,
                    priority: int = 0, **meta: Any) -> GrammarRule | None:
        """Create a new grammar rule with validation.
        
        Args:
            name: Rule name (alphanumeric + underscore)
            pattern: Regex pattern
            action: Action type (must be in SAFE_ACTIONS)
            priority: Rule priority (higher = first)
            **meta: Additional metadata
            
        Returns:
            GrammarRule if valid, None if rejected
        """
        # Validate name
        if not self._validate_name(name):
            logger.warning("Rule name rejected: %s", name)
            return None
        
        # Validate pattern
        if not self._validate_pattern(pattern):
            logger.warning("Rule pattern rejected: %s", pattern[:50])
            return None
        
        # Validate action
        if not self._validate_action(action):
            logger.warning("Rule action rejected: %s", action)
            return None
        
        rule = GrammarRule(
            rule_id=f"rule-{self._next_id}",
            name=name,
            pattern=pattern,
            action=action,
            priority=priority,
            meta=meta,
        )
        self._next_id += 1
        self._rules[rule.rule_id] = rule
        
        logger.info("Created rule %s (%s)", rule.rule_id, name)
        return rule
    
    def match(self, text: str) -> list[GrammarRule]:
        """Find all rules matching the given text.
        
        Args:
            text: Input text to match against
            
        Returns:
            List of matching rules, sorted by priority
        """
        matches = []
        for rule in self._rules.values():
            try:
                if re.search(rule.pattern, text, timeout=0.5):
                    matches.append(rule)
            except Exception:
                # Regex timeout or error
                pass
        
        matches.sort(key=lambda r: r.priority, reverse=True)
        return matches
    
    def get_rule(self, rule_id: str) -> GrammarRule | None:
        """Get rule by ID."""
        return self._rules.get(rule_id)
    
    def all_rules(self) -> list[GrammarRule]:
        """Return all rules sorted by priority."""
        return sorted(self._rules.values(), key=lambda r: r.priority, reverse=True)
    
    def remove_rule(self, rule_id: str) -> bool:
        """Remove a rule."""
        if rule_id in self._rules:
            del self._rules[rule_id]
            logger.info("Removed rule %s", rule_id)
            return True
        return False
    
    def _validate_name(self, name: str) -> bool:
        """Validate rule name: alphanumeric + underscore only."""
        if not name:
            return False
        if not re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*$", name):
            self._log_violation("invalid_name", name)
            return False
        return True
    
    def _validate_pattern(self, pattern: str) -> bool:
        """Validate regex pattern: no chaos vectors."""
        for blocked, reason in self.BLOCKED_PATTERNS:
            if re.search(blocked, pattern, re.IGNORECASE):
                self._log_violation(reason, pattern[:100])
                return False
        
        # Verify it's valid regex
        try:
            re.compile(pattern)
        except re.error:
            self._log_violation("invalid_regex", pattern[:100])
            return False
        
        return True
    
    def _validate_action(self, action: str) -> bool:
        """Validate action: must be in whitelist."""
        return action in self.SAFE_ACTIONS
    
    def _log_violation(self, reason: str, content: str) -> None:
        """Log a security violation."""
        from datetime import datetime, timezone
        self._violation_log.append({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "reason": reason,
            "content": content,
        })
        logger.warning("Security violation: %s - %s", reason, content[:50])
    
    def violations(self) -> list[dict[str, Any]]:
        """Return security violation log."""
        return self._violation_log.copy()
    
    def save(self, path: Path) -> None:
        """Save rules to disk."""
        with open(path, "w") as f:
            json.dump({
                "rules": [r.to_dict() for r in self._rules.values()],
                "next_id": self._next_id,
                "violations": self._violation_log,
            }, f, indent=2)
    
    @classmethod
    def load(cls, path: Path) -> "GrammarEngine":
        """Load rules from disk."""
        instance = cls()
        
        with open(path) as f:
            data = json.load(f)
        
        for rule_data in data.get("rules", []):
            rule = GrammarRule.from_dict(rule_data)
            instance._rules[rule.rule_id] = rule
        
        instance._next_id = data.get("next_id", 1)
        instance._violation_log = data.get("violations", [])
        
        return instance
    
    def stats(self) -> dict[str, Any]:
        """Return engine statistics."""
        return {
            "rules": len(self._rules),
            "violations": len(self._violation_log),
            "safe_actions": list(self.SAFE_ACTIONS),
        }
