from typing import Optional

from deps_high_sparrow.domain.model import DocumentType, IDocumentTypeRepository
from deps_high_sparrow.extras.datasource import Database

from .mappers import DocumentTypeMapper
from .query_factory import DocumentTypeQueryFactory

__all__ = ["DocumentTypeRepository"]


class DocumentTypeRepository(IDocumentTypeRepository):
    def __init__(self, database: Database) -> None:
        self._db = database
        self._query_factory = DocumentTypeQueryFactory()

    def document_type_of_id(self, document_type_id: str, tenant_id: str) -> Optional[DocumentType]:
        with self._db.connection() as conn:
            document_type = conn.execute(
                self._query_factory.select_document_type(document_type_id, tenant_id),
            ).fetchone()

        if document_type:
            return DocumentTypeMapper.from_dict(document_type)

        return None

    def delete(self, document_type_id: str, tenant_id: str) -> None:
        with self._db.connection() as conn:
            conn.execute(self._query_factory.delete_document_type(document_type_id, tenant_id))

    def save(self, document_type: DocumentType) -> None:
        raw_document_type = DocumentTypeMapper.to_dict(document_type)
        with self._db.connection() as conn:
            conn.execute(self._query_factory.insert_document_type(), raw_document_type)

    def save_all(self, document_types: list[DocumentType]) -> None:
        raw_document_types = [DocumentTypeMapper.to_dict(document_type) for document_type in document_types]
        with self._db.connection() as conn:
            conn.execute(self._query_factory.insert_document_type(), raw_document_types)

    def save_new(self, document_type: DocumentType) -> None:
        raw_document_type = DocumentTypeMapper.to_dict(document_type)
        with self._db.connection() as conn:
            conn.execute(self._query_factory.insert_document_type_without_update(), raw_document_type)

    def save_new_all(self, document_types: list[DocumentType]) -> None:
        raw_document_types = [DocumentTypeMapper.to_dict(document_type) for document_type in document_types]
        with self._db.connection() as conn:
            conn.execute(self._query_factory.insert_document_type_without_update(), raw_document_types)
