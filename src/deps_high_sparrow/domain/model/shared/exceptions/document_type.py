from .base import NotFoundError

__all__ = ["DocumentTypeNotFound"]


class DocumentTypeNotFound(NotFoundError):
    code = "document_type_not_found_error"
