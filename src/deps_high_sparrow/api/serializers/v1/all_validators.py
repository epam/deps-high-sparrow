from pydantic import Field

from deps_high_sparrow.domain.model import DocumentType

from ..base import ConfiguredBaseModel
from .cross_field_validator import SerializedCrossFieldValidator
from .external_validator import SerializedExternalValidator
from .validator import SerializedValidator

__all__ = ["AllValidatorsResponse"]


class AllValidatorsResponse(ConfiguredBaseModel):
    validators: list[SerializedValidator]
    cross_field_validators: list[SerializedCrossFieldValidator] = Field(alias="crossFieldValidators")
    external_validators: list[SerializedExternalValidator] = Field(alias="externalValidators")

    @classmethod
    def from_model(cls, document_type: DocumentType) -> "AllValidatorsResponse":
        return cls(
            validators=[SerializedValidator.from_model(validator) for validator in document_type.validators],
            cross_field_validators=[
                SerializedCrossFieldValidator.from_model(cross_field_validator)
                for cross_field_validator in document_type.cross_field_validators
            ],
            external_validators=[
                SerializedExternalValidator.from_model(external_validator)
                for external_validator in document_type.external_validators
            ],
        )
