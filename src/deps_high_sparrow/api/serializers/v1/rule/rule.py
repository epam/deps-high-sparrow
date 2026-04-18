from deps_high_sparrow.domain.model import Rule, Severity

from ...base import ConfiguredBaseModel

__all__ = ["SerializedRule"]


class SerializedRule(ConfiguredBaseModel):
    name: str
    severity: Severity
    rule: str
    issue_message: str
    description: str
    need_warning_even_if_optional: bool
    for_each: bool
    for_any: bool
    check_optional_fields: bool

    @classmethod
    def from_model(cls, rule: Rule) -> "SerializedRule":
        return cls(
            name=rule.name,
            severity=rule.severity,
            rule=rule.rule,
            issue_message=rule.issue_message,
            description=rule.description,
            need_warning_even_if_optional=rule.need_warning_even_if_optional,
            for_each=rule.for_each,
            for_any=rule.for_any,
            check_optional_fields=rule.check_optional_fields,
        )
