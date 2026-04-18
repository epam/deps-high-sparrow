from ...shared import Guard, ImmutableCheck, LengthCheck, Severity

__all__ = ["Rule"]


class Rule:
    name = Guard[str](str, ImmutableCheck(), LengthCheck(min_length=1, max_length=100))
    severity = Guard[Severity](Severity, ImmutableCheck())
    rule = Guard[str](str, ImmutableCheck())
    issue_message = Guard[str](str, ImmutableCheck())
    description = Guard[str](str, ImmutableCheck())
    need_warning_even_if_optional = Guard[bool](bool, ImmutableCheck())
    for_each = Guard[bool](bool, ImmutableCheck())
    for_any = Guard[bool](bool, ImmutableCheck())
    check_optional_fields = Guard[bool](bool, ImmutableCheck())

    def __init__(
        self,
        name: str,
        severity: Severity,
        rule: str,
        issue_message: str,
        description: str,
        need_warning_even_if_optional: bool,
        for_each: bool,
        for_any: bool,
        check_optional_fields: bool,
    ):
        self.name = name
        self.severity = severity
        self.rule = rule
        self.issue_message = issue_message
        self.description = description
        self.need_warning_even_if_optional = need_warning_even_if_optional
        self.for_each = for_each
        self.for_any = for_any
        self.check_optional_fields = check_optional_fields

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, self.__class__)
            and self.name == other.name
            and self.severity == other.severity
            and self.rule == other.rule
            and self.issue_message == other.issue_message
            and self.description == other.description
            and self.need_warning_even_if_optional == other.need_warning_even_if_optional
            and self.for_any == other.for_any
            and self.for_each == other.for_each
            and self.check_optional_fields == other.check_optional_fields
        )
