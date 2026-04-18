import uuid

import factory

from deps_high_sparrow.domain import ValidationResult

from .issues import IssuesFactory

__all__ = ["ValidationResultFactory"]


class ValidationResultFactory(factory.Factory):
    class Meta:
        model = ValidationResult

    id = factory.LazyFunction(lambda: uuid.uuid4().hex)
    tenant_id = factory.LazyFunction(lambda: uuid.uuid4().hex)
    issues = factory.LazyFunction(lambda: [IssuesFactory()])
