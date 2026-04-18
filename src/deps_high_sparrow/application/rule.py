import logging

from deps_high_sparrow.domain.exceptions import DocumentTypeNotFound
from deps_high_sparrow.domain.model import (
    DocumentType,
    IDocumentTypeRepository,
    Rule,
    Severity,
)

__all__ = ["RuleService"]


class RuleService:
    def __init__(
        self,
        document_type_repository: IDocumentTypeRepository,
    ):
        self._document_type_repository = document_type_repository
        self._logger = logging.getLogger(self.__class__.__name__)

    def create_rule(
        self,
        tenant_id: str,
        document_type_id: str,
        validator_code: str,
        name: str,
        severity: Severity,
        rule: str,
        issue_message: str,
        description: str,
        need_warning_even_if_optional: bool,
        for_each: bool,
        for_any: bool,
        check_optional_fields: bool,
    ) -> Rule:
        document_type = self._get_document_type(document_type_id=document_type_id, tenant_id=tenant_id)
        validator = document_type.get_validator(code=validator_code)
        rule = validator.add_rule(
            name=name,
            severity=severity,
            rule=rule,
            issue_message=issue_message,
            description=description,
            need_warning_even_if_optional=need_warning_even_if_optional,
            for_each=for_each,
            for_any=for_any,
            check_optional_fields=check_optional_fields,
        )
        self._document_type_repository.save(document_type)
        return rule

    def delete_rule(
        self,
        tenant_id: str,
        document_type_id: str,
        validator_code: str,
        name: str,
    ) -> None:
        document_type = self._get_document_type(document_type_id=document_type_id, tenant_id=tenant_id)
        validator = document_type.get_validator(code=validator_code)
        validator.delete_rule(name=name)
        self._document_type_repository.save(document_type)

    def _get_document_type(
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
