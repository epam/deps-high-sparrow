from copy import deepcopy
from typing import Optional

from deps_high_sparrow.domain.model import DocumentType, IDocumentTypeRepository

__all__ = ["FakeDocumentTypeRepository"]

DocTypeIdentifier = tuple[str, str]


class FakeDocumentTypeRepository(IDocumentTypeRepository):
    def __init__(self, fake_db: Optional[dict[DocTypeIdentifier, DocumentType]] = None) -> None:
        self._document_type_db: Optional[dict[DocTypeIdentifier, DocumentType]] = {}
        if fake_db:
            self._document_type_db = fake_db

    def __repr__(self) -> str:
        return str(self._document_type_db)

    def document_type_of_id(self, document_type_id: str, tenant_id: str) -> Optional[DocumentType]:
        key = self._get_dict_key(document_type_id=document_type_id, tenant_id=tenant_id)
        return self._document_type_db.get(key)

    def save(self, document_type: DocumentType) -> None:
        key = self._get_dict_key(document_type_id=document_type.id(), tenant_id=document_type.tenant_id())
        self._document_type_db[key] = deepcopy(document_type)

    def save_all(self, document_types: list[DocumentType]) -> None:
        for doc_type in document_types:
            self.save(doc_type)

    def save_new(self, document_type: DocumentType) -> None:
        key = self._get_dict_key(document_type_id=document_type.id(), tenant_id=document_type.tenant_id())
        if self._document_type_db.get(key):
            return

        self._document_type_db[key] = deepcopy(document_type)

    def save_new_all(self, document_types: list[DocumentType]) -> None:
        for doc_type in document_types:
            self.save_new(doc_type)

    def delete(self, document_type_id: str, tenant_id: str) -> None:
        key = self._get_dict_key(document_type_id=document_type_id, tenant_id=tenant_id)
        self._document_type_db.pop(key, None)

    @staticmethod
    def _get_dict_key(*, document_type_id: str, tenant_id: str) -> DocTypeIdentifier:
        return document_type_id, tenant_id
