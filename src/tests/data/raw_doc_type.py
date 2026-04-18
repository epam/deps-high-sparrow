import uuid

from .raw_document_type_fields import raw_number_field1, raw_string_field1

__all__ = ["raw_document_type"]

raw_document_type = {
    "document_type_id": uuid.uuid4().hex,
    "tenant_id": uuid.uuid4().hex,
    "fields": [
        raw_string_field1,
        raw_number_field1,
    ],
}
