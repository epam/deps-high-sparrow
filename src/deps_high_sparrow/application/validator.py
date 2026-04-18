import logging

from deps_high_sparrow.domain import IDocumentTypeRepository
from deps_high_sparrow.domain.exceptions import ValidatorNotFound
from deps_high_sparrow.shared import ExtractionField

from .validator_creators import ValidatorCreator

__all__ = ["ValidatorService"]


class ValidatorService:
    def __init__(
        self,
        document_type_repository: IDocumentTypeRepository,
    ) -> None:
        self._document_type_repository = document_type_repository

        self._logger = logging.getLogger(self.__class__.__name__)

    def remove_validator(
        self,
        document_type_id: str,
        tenant_id: str,
        field_code: str,
    ) -> None:
        if (document_type := self._document_type_repository.document_type_of_id(document_type_id, tenant_id)) is None:
            self._logger.warning(
                "Unable to remove `%s` validator: Document type `%s` not found for tenant `%s`",
                field_code,
                document_type_id,
                tenant_id,
            )
            return

        document_type.remove_validator(field_code)

        self._document_type_repository.save(document_type)

    def save_validator(
        self,
        document_type_id: str,
        tenant_id: str,
        field: ExtractionField,
    ) -> None:
        if (document_type := self._document_type_repository.document_type_of_id(document_type_id, tenant_id)) is None:
            self._logger.warning(
                "Unable to upsert `%s` validator: Document type `%s` not found for tenant `%s`",
                field["code"],
                document_type_id,
                tenant_id,
            )
            return

        try:
            rules = document_type.get_validator(field["code"]).rules
            document_type.remove_validator(field["code"])
        except ValidatorNotFound:
            rules = {}

        ValidatorCreator(document_type).create_for_field(field)

        if rules:
            document_type.add_rules_to_validator(code=field["code"], rules=rules.values())

        self._document_type_repository.save(document_type)
