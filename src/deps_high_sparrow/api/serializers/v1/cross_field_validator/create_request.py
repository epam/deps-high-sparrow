from typing import List, Optional

from pydantic import Field, field_validator

from deps_high_sparrow.api.serializers.base import ConfiguredBaseModel
from deps_high_sparrow.domain.model.shared import Severity

__all__ = ["CreateCrossFieldValidatorRequest", "CrossFieldValidatorCreatedResponse"]


class CreateCrossFieldValidatorRequest(ConfiguredBaseModel):
    name: str
    description: Optional[str] = ""
    rule: str
    severity: Severity
    validated_fields: List[str]
    issue_message: str
    dependent_fields: Optional[List[str]] = Field(default_factory=list, alias="dependentFields")
    for_each: Optional[bool] = False
    for_any: Optional[bool] = False

    @field_validator("validated_fields")
    @classmethod
    def validate_fields_not_empty(cls, validated_fields: Optional[List[str]]) -> List[str]:  # noqa: N805
        if validated_fields is not None and not validated_fields:
            raise ValueError("Validated fields list cannot be empty. Please provide at least one field.")
        return validated_fields

    @field_validator("rule", "issue_message")
    @classmethod
    def validate_non_whitespace(cls, value: Optional[str], info) -> str:  # noqa: N805
        if not value or value.isspace():
            raise ValueError(f"`{info.field_name}` cannot be empty or contain only whitespace or special characters.")
        return value

    @field_validator("dependent_fields", mode="before")
    @classmethod
    def convert_none_to_empty_list(cls, dependent_fields: Optional[List[str]]) -> List[str]:  # noqa: N805
        return [] if dependent_fields is None else dependent_fields


class CrossFieldValidatorCreatedResponse(ConfiguredBaseModel):
    id: str = Field(..., description="The ID of the created cross-field validator")
