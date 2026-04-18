from typing import Any

from deps_high_sparrow.domain.model import Rule, Severity

__all__ = ["RuleMapper"]


class RuleMapper:
    @staticmethod
    def from_dict(raw_rule: dict[str, Any]) -> Rule:
        return Rule(
            name=raw_rule["name"],
            description=raw_rule["description"],
            severity=Severity(raw_rule["severity"]),
            rule=raw_rule["rule"],
            issue_message=raw_rule["issue_message"],
            need_warning_even_if_optional=raw_rule["need_warning_even_if_optional"],
            for_each=raw_rule["for_each"],
            for_any=raw_rule["for_any"],
            check_optional_fields=raw_rule["check_optional_fields"],
        )

    @staticmethod
    def to_dict(rule: Rule) -> dict[str, Any]:
        return {
            "name": rule.name,
            "description": rule.description,
            "severity": rule.severity.value,
            "rule": rule.rule,
            "issue_message": rule.issue_message,
            "need_warning_even_if_optional": rule.need_warning_even_if_optional,
            "for_each": rule.for_each,
            "for_any": rule.for_any,
            "check_optional_fields": rule.check_optional_fields,
        }
