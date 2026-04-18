from typing import Optional

from pydantic import Field

from deps_high_sparrow.domain.model import Validator

from ...base import ConfiguredBaseModel
from ..rule import SerializedRule
from .validator_type import SerializedValidatorType

__all__ = ["SerializedValidator"]


class SerializedValidator(ConfiguredBaseModel):
    code: str
    type: SerializedValidatorType
    is_required: bool = Field(alias="isRequired")
    rules: Optional[list[SerializedRule]]

    @classmethod
    def from_model(cls, validator: Validator) -> "SerializedValidator":
        return cls(
            code=validator.code.value,
            type=SerializedValidatorType.from_model(validator.type_),
            is_required=validator.is_required,
            rules=[SerializedRule.from_model(rule) for rule in validator.rules.values()],
        )
