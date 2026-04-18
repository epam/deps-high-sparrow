from dataclasses import dataclass
from typing import Any, Dict, Optional, Union

from deps_message_flow.events.common import DomainEvent

__all__ = [
    "DocumentTypeFieldCreated",
    "DocumentTypeFieldUpdated",
    "DocumentTypeFieldDeleted",
    "ExtractorFieldCreated",
    "ExtractorFieldUpdated",
    "ExtractorFieldDeleted",
    "ExtractionFieldUpsertedEvent",
]


@dataclass
class DocumentTypeFieldCreated(DomainEvent):
    document_type_code: str
    field: Dict[str, Any]


@dataclass
class DocumentTypeFieldUpdated(DomainEvent):
    document_type_code: str
    field: Dict[str, Any]


@dataclass
class DocumentTypeFieldDeleted(DomainEvent):
    document_type_pk: int
    document_type_code: str
    field_code: str


@dataclass
class ExtractorFieldCreated(DomainEvent):
    document_type_code: str
    code: str
    field_type: str
    description: Optional[dict[str, Any]]
    required: bool


@dataclass
class ExtractorFieldUpdated(ExtractorFieldCreated):
    pass


@dataclass
class ExtractorFieldDeleted(DomainEvent):
    code: str
    document_type_code: str
    extractor_type: str


ExtractionFieldUpsertedEvent = Union[
    ExtractorFieldCreated,
    ExtractorFieldUpdated,
]
