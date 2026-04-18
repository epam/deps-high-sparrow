from typing import List, Optional

from pydantic import field_validator

from deps_high_sparrow.api.serializers.base import ConfiguredBaseModel
from deps_high_sparrow.domain.model.shared import Severity

__all__ = ["UpdateCrossFieldValidatorRequest", "UpdateCrossFieldValidatorResponse"]


class UpdateCrossFieldValidatorRequest(ConfiguredBaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    rule: Optional[str] = None
    severity: Optional[Severity] = None
    validated_fields: Optional[list[str]] = None
    issue_message: Optional[str] = None
    dependent_fields: Optional[list[str]] = None
    for_each: Optional[bool] = None
    for_any: Optional[bool] = None

    @field_validator("validated_fields")
    @classmethod
    def validate_fields_not_empty(cls, validated_fields: Optional[List[str]]) -> List[str]:  # noqa: N805
        if validated_fields is not None and not validated_fields:
            raise ValueError("Validated fields list cannot be empty. Please provide at least one field.")
        return validated_fields

    @field_validator("rule", "issue_message")
    @classmethod
    def validate_non_whitespace(cls, value: Optional[str], info) -> Optional[str]:  # noqa: N805
        if value is not None and (not value or value.isspace()):
            field_name = info.field_name.replace("_", " ").title()
            raise ValueError(f"{field_name} cannot be empty or contain only whitespace or special characters.")
        return value


class UpdateCrossFieldValidatorResponse(ConfiguredBaseModel):
    id: str
