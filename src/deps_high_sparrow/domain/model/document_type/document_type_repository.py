from typing import Optional, Protocol

from ..document_type import DocumentType

__all__ = ["IDocumentTypeRepository"]


class IDocumentTypeRepository(Protocol):
    def document_type_of_id(self, document_type_id: str, tenant_id: str) -> Optional[DocumentType]:
        ...

    def delete(self, document_type_id: str, tenant_id: str) -> None:
        ...

    def save(self, document_type: DocumentType) -> None:
        ...

    def save_all(self, document_types: list[DocumentType]) -> None:
        ...

    def save_new(self, document_type: DocumentType) -> None:
        ...

    def save_new_all(self, document_types: list[DocumentType]) -> None:
        ...
