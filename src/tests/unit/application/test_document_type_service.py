import pytest

from deps_high_sparrow.application import DocumentTypeService
from deps_high_sparrow.constants import COMMANDS_CHANNEL, COMMANDS_REPLIES_CHANNEL
from deps_high_sparrow.domain.exceptions import DocumentTypeNotFound
from deps_high_sparrow.domain.model import DocumentType, IDocumentTypeRepository
from deps_high_sparrow.messaging import GetDocumentTypes
from tests.data import raw_document_type
from tests.fakes import Command


class TestRuleService:
    def test_find_doc_type__ok(
        self,
        fake_document_type_repository: IDocumentTypeRepository,
        document_type_service: DocumentTypeService,
        document_type_with_string_validator_and_one_rule,
    ):
        fake_document_type_repository.save(document_type_with_string_validator_and_one_rule)
        document_type = document_type_service.find_document_type(
            document_type_id=document_type_with_string_validator_and_one_rule.id(),
            tenant_id=document_type_with_string_validator_and_one_rule.tenant_id(),
        )

        assert isinstance(document_type, DocumentType)
        assert document_type.id() == document_type_with_string_validator_and_one_rule.id()
        assert document_type.tenant_id() == document_type_with_string_validator_and_one_rule.tenant_id()
        assert document_type.validators == document_type_with_string_validator_and_one_rule.validators

    def test_find_doc_type__not_exists__raises(
        self,
        fake_document_type_repository: IDocumentTypeRepository,
        document_type_service: DocumentTypeService,
        document_type_with_string_validator_and_one_rule,
        tenant_id,
    ):
        not_existed_document_type_id = "not_existed_document_type_id"
        with pytest.raises(DocumentTypeNotFound):
            document_type_service.find_document_type(
                document_type_id=not_existed_document_type_id,
                tenant_id=tenant_id,
            )

    @pytest.mark.document_type
    def test_initialize__ok(self, command_producer, document_type_service: DocumentTypeService):
        document_type_service.initialize()

        assert command_producer.sent == [
            Command(channel=COMMANDS_CHANNEL, command=GetDocumentTypes(), reply_to=COMMANDS_REPLIES_CHANNEL),
        ]

    @pytest.mark.document_type
    def test_save_new_delete_document_type__ok(
        self,
        fake_document_type_repository: IDocumentTypeRepository,
        document_type_service: DocumentTypeService,
        document_type_id,
        tenant_id,
    ):
        document_type_service.save_new_document_type(document_type_id=document_type_id, tenant_id=tenant_id)

        saved_document_type = fake_document_type_repository.document_type_of_id(
            document_type_id=document_type_id,
            tenant_id=tenant_id,
        )
        assert saved_document_type.id() == document_type_id
        assert saved_document_type.tenant_id() == tenant_id

        document_type_service.delete_document_type(document_type_id=document_type_id, tenant_id=tenant_id)

        deleted_document_type = fake_document_type_repository.document_type_of_id(
            document_type_id=document_type_id,
            tenant_id=tenant_id,
        )
        assert deleted_document_type is None

    @pytest.mark.validator_creation
    def test_initialize_document_types__ok(
        self,
        fake_document_type_repository: IDocumentTypeRepository,
        document_type_service: DocumentTypeService,
    ):
        document_type_service.initialize_document_types([raw_document_type])

        saved_document_type = fake_document_type_repository.document_type_of_id(
            document_type_id=raw_document_type["document_type_id"],
            tenant_id=raw_document_type["tenant_id"],
        )
        assert len(saved_document_type.validators) == len(raw_document_type["fields"])

    @pytest.mark.document_type
    def test_attach_validator__ok(
        self,
        fake_document_type_repository: IDocumentTypeRepository,
        document_type_service: DocumentTypeService,
        document_type: DocumentType,
        document_type_id,
        tenant_id,
        external_validator_name,
        external_validator_url,
        external_validator,
    ):
        fake_document_type_repository.save(document_type)

        document_type_service.attach_validator(
            tenant_id=tenant_id,
            document_type_id=document_type_id,
            name=external_validator_name,
            url=external_validator_url,
        )

        saved_document_type = fake_document_type_repository.document_type_of_id(
            document_type_id=document_type_id, tenant_id=tenant_id
        )
        assert len(saved_document_type.external_validators) == 1
        assert saved_document_type.external_validators[0] == external_validator

    @pytest.mark.document_type
    def test_attach_validator__doc_type_doesnt_exist__not_found(
        self,
        document_type_service: DocumentTypeService,
        document_type_id,
        tenant_id,
        external_validator_name,
        external_validator_url,
    ):
        with pytest.raises(DocumentTypeNotFound):
            document_type_service.attach_validator(
                tenant_id=tenant_id,
                document_type_id=document_type_id,
                name=external_validator_name,
                url=external_validator_url,
            )

    @pytest.mark.document_type
    def test_remove_validator__ok(
        self,
        fake_document_type_repository: IDocumentTypeRepository,
        document_type_service: DocumentTypeService,
        document_type_with_external_validator: DocumentType,
        document_type_id,
        tenant_id,
        external_validator_name,
    ):
        fake_document_type_repository.save(document_type_with_external_validator)

        document_type_service.remove_validator(
            tenant_id=tenant_id,
            document_type_id=document_type_id,
            name=external_validator_name,
        )

        saved_document_type = fake_document_type_repository.document_type_of_id(
            document_type_id=document_type_id, tenant_id=tenant_id
        )
        assert len(saved_document_type.external_validators) == 0

    @pytest.mark.document_type
    def test_remove_validator__doc_type_doesnt_exist__not_found(
        self,
        document_type_service: DocumentTypeService,
        document_type_id,
        tenant_id,
        external_validator_name,
    ):
        with pytest.raises(DocumentTypeNotFound):
            document_type_service.remove_validator(
                tenant_id=tenant_id,
                document_type_id=document_type_id,
                name=external_validator_name,
            )
