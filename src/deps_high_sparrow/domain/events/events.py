from dataclasses import dataclass

from deps_message_flow.events.common import DomainEvent

__all__ = ["BusinessRuleViolated"]


@dataclass
class BusinessRuleViolated(DomainEvent):
    document_id: str
    field_code: str
    message: str
