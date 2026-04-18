from dataclasses import dataclass


@dataclass
class ValidateDocument:
    document_id: str


@dataclass
class ValidationReply:
    document_id: str
    is_valid: bool


@dataclass
class PerformValidation:
    document_id: str
    document_type_id: str


@dataclass
class PerformValidationReply:
    result: bool
