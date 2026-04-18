from typing import Any

from deps_high_sparrow.domain.model import DocumentType

from .cross_field_validator import CrossFieldValidatorMapper
from .external_validator import ExternalValidatorMapper
from .validator import ValidatorMapper

__all__ = ["DocumentTypeMapper"]


class DocumentTypeMapper:
    @staticmethod
    def from_dict(raw_doc_type: dict[str, Any]) -> DocumentType:
        validators = [ValidatorMapper.from_dict(validator) for validator in raw_doc_type["validators"] or []]
        external_validators = [
            ExternalValidatorMapper.from_dict(external_validator)
            for external_validator in raw_doc_type["external_validators"] or []
        ]

        cross_field_validators = [
            CrossFieldValidatorMapper.from_dict(cross_field_validator)
            for cross_field_validator in raw_doc_type["cross_field_validators"] or []
        ]

        return DocumentType(
            id_=raw_doc_type["id"],
            tenant_id=raw_doc_type["tenant_id"],
            validators=validators,
            external_validators=external_validators,
            cross_field_validators=cross_field_validators,
        )

    @staticmethod
    def to_dict(document_type: DocumentType) -> dict[str, Any]:
        raw_validators = [ValidatorMapper.to_dict(validator) for validator in document_type.validators]
        raw_external_validators = [
            ExternalValidatorMapper.to_dict(external_validator)
            for external_validator in document_type.external_validators
        ]
        raw_cross_field_validators = [
            CrossFieldValidatorMapper.to_dict(cross_field_validator)
            for cross_field_validator in document_type.cross_field_validators
        ]
        return {
            "id": document_type.id(),
            "tenant_id": document_type.tenant_id(),
            "validators": raw_validators or None,
            "external_validators": raw_external_validators or None,
            "cross_field_validators": raw_cross_field_validators or None,
        }
