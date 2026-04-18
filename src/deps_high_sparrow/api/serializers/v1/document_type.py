from typing import Optional

from pydantic import Field

from deps_high_sparrow.domain.model import DocumentType

from ..base import ConfiguredBaseModel
from .cross_field_validator import SerializedCrossFieldValidator
from .external_validator import SerializedExternalValidator
from .validator import SerializedValidator

__all__ = ["SerializedDocumentType"]


class SerializedDocumentType(ConfiguredBaseModel):
    id: str
    tenant_id: str = Field(alias="tenantId")
    validators: Optional[list[SerializedValidator]]
    external_validators: Optional[list[SerializedExternalValidator]] = Field(alias="externalValidators")
    cross_field_validators: Optional[list[SerializedCrossFieldValidator]] = Field(alias="crossFieldValidators")

    @classmethod
    def from_model(cls, document_type: DocumentType) -> "SerializedDocumentType":
        return cls(
            id=document_type.id(),
            tenant_id=document_type.tenant_id(),
            validators=[SerializedValidator.from_model(validator) for validator in document_type.validators],
            external_validators=[
                SerializedExternalValidator.from_model(external_validator)
                for external_validator in document_type.external_validators
            ],
            cross_field_validators=[
                SerializedCrossFieldValidator.from_model(cross_field_validator)
                for cross_field_validator in document_type.cross_field_validators
            ],
        )
