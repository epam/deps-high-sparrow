from dataclasses import dataclass


@dataclass
class DocumentDeleted:
    document_id: str


@dataclass
class DocumentValidationPassed:
    document_id: str


@dataclass
class DocumentValidationFailed:
    document_id: str


@dataclass
class DocumentValidationProcessingFailed:
    document_id: str
    message: str


@dataclass
class DocumentTypeChanged:
    document_id: str


@dataclass
class BusinessRuleViolated:
    document_id: str
    field_code: str
    message: str
