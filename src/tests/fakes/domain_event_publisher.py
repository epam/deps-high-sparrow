from collections import namedtuple

from deps_message_flow.events.common import DomainEvent

__all__ = ["FakeDomainEventPublisher", "Events"]

Events = namedtuple("Events", ("aggregate_type", "aggregate_id", "events"))


class FakeDomainEventPublisher:
    def __init__(self) -> None:
        self._published: list[Events] = []

    @property
    def published(self) -> list[Events]:
        return self._published

    @published.deleter
    def published(self) -> None:
        self._published.clear()

    def publish(self, aggregate_type: str, aggregate_id: str, domain_events: list[DomainEvent], **kwargs) -> None:
        self._published.append(Events(aggregate_type=aggregate_type, aggregate_id=aggregate_id, events=domain_events))
