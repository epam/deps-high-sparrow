import logging
from typing import Any, List, Optional

from deps_message_flow.commands.producer import CommandProducer

from deps_high_sparrow.constants import COMMANDS_CHANNEL, COMMANDS_REPLIES_CHANNEL
from deps_high_sparrow.domain import DocumentTypeFactory, IDocumentTypeRepository
from deps_high_sparrow.domain.exceptions import DocumentTypeNotFound
from deps_high_sparrow.domain.model import DocumentType
from deps_high_sparrow.domain.model.shared import Severity
from deps_high_sparrow.messaging import GetDocumentTypes

from .validator_creators import ValidatorCreator

__all__ = ["DocumentTypeService"]


class DocumentTypeService:
    def __init__(
        self,
        document_type_repository: IDocumentTypeRepository,
        command_producer: CommandProducer,
    ) -> None:
        self._document_type_repository = document_type_repository
        self._command_producer = command_producer

        self._logger = logging.getLogger(self.__class__.__name__)

    def initialize(self):
        self._command_producer.send(
            COMMANDS_CHANNEL,
            GetDocumentTypes(),
            COMMANDS_REPLIES_CHANNEL,
        )

    def find_document_type(
        self,
        document_type_id: str,
        tenant_id: str,
    ) -> DocumentType:
        document_type = self._document_type_repository.document_type_of_id(
            document_type_id=document_type_id,
            tenant_id=tenant_id,
        )
        if document_type is None:
            raise DocumentTypeNotFound(document_type_id)

        return document_type

    def save_new_document_type(self, document_type_id: str, tenant_id: str) -> None:
        self._document_type_repository.save_new(
            DocumentTypeFactory.create(
                id_=document_type_id,
                tenant_id=tenant_id,
            ),
        )

    def delete_document_type(self, document_type_id: str, tenant_id: str) -> None:
        self._document_type_repository.delete(document_type_id=document_type_id, tenant_id=tenant_id)

    def initialize_document_types(self, raw_document_types: list[dict[str, Any]]) -> None:
        document_types = []
        for raw_type in raw_document_types:
            try:
                document_type = DocumentTypeFactory.create(
                    id_=raw_type["document_type_id"],
                    tenant_id=raw_type["tenant_id"],
                )

                ValidatorCreator(document_type).create_for_fields(raw_type["fields"])

                document_types.append(document_type)
            except Exception as exc:
                self._logger.error(
                    "Failed to create DocumentType `%s`. `%s` occurred: ```%s```",
                    raw_type["document_type_id"],
                    exc.__class__.__name__,
                    str(exc),
                )

        self._document_type_repository.save_new_all(document_types)

    def attach_validator(self, tenant_id: str, document_type_id: str, name: str, url: str) -> None:
        document_type = self.find_document_type(document_type_id=document_type_id, tenant_id=tenant_id)
        document_type.attach_external_validator(name=name, url=url)
        self._document_type_repository.save(document_type)

    def remove_validator(self, tenant_id: str, document_type_id: str, name: str) -> None:
        document_type = self.find_document_type(document_type_id=document_type_id, tenant_id=tenant_id)
        document_type.remove_external_validator(name=name)
        self._document_type_repository.save(document_type)

    def add_cross_field_validator(
        self,
        tenant_id: str,
        document_type_id: str,
        name: str,
        description: str,
        rule: str,
        severity: Severity,
        validated_fields: List[str],
        issue_message: str,
        dependent_fields: List[str],
        for_each: bool = False,
        for_any: bool = False,
    ) -> str:
        document_type = self.find_document_type(document_type_id=document_type_id, tenant_id=tenant_id)

        validator_id = document_type.add_cross_field_validator(
            name=name,
            description=description,
            rule=rule,
            severity=severity,
            validated_fields=validated_fields,
            issue_message=issue_message,
            dependent_fields=dependent_fields,
            for_each=for_each,
            for_any=for_any,
        )

        self._document_type_repository.save(document_type)

        return validator_id

    def update_cross_field_validator(
        self,
        validator_id: str,
        tenant_id: str,
        document_type_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        rule: Optional[str] = None,
        severity: Optional[Severity] = None,
        validated_fields: Optional[list[str]] = None,
        issue_message: Optional[str] = None,
        dependent_fields: Optional[list[str]] = None,
        for_each: Optional[bool] = None,
        for_any: Optional[bool] = None,
    ) -> None:
        document_type = self.find_document_type(document_type_id=document_type_id, tenant_id=tenant_id)

        document_type.update_cross_field_validator(
            validator_id=validator_id,
            name=name,
            description=description,
            rule=rule,
            severity=severity,
            validated_fields=validated_fields,
            issue_message=issue_message,
            dependent_fields=dependent_fields,
            for_each=for_each,
            for_any=for_any,
        )
        self._document_type_repository.save(document_type)

    def delete_cross_field_validator(self, document_type_id: str, tenant_id: str, validator_id: str) -> None:
        document_type = self.find_document_type(document_type_id=document_type_id, tenant_id=tenant_id)

        document_type.remove_cross_field_validator(validator_id=validator_id)

        self._document_type_repository.save(document_type)
