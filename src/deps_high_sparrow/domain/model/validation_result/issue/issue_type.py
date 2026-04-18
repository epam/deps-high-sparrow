from enum import Enum

__all__ = ["IssueType"]


class IssueType(Enum):
    PRE_CHECK = "pre_check"
    TYPE_CHECK = "type_check"
    RULES_CHECK = "rules_check"
    EXTERNAL_CHECK = "external_check"
