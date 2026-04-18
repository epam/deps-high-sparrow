from typing import Optional

from deps_high_sparrow.domain.model import Severity

from ...base import ConfiguredBaseModel

__all__ = ["CreateRuleRequest"]


class CreateRuleRequest(ConfiguredBaseModel):
    name: str
    severity: Severity
    rule: str
    issue_message: str
    description: Optional[str] = ""
    need_warning_even_if_optional: Optional[bool] = False
    for_each: Optional[bool] = False
    for_any: Optional[bool] = False
    check_optional_fields: Optional[bool] = False
