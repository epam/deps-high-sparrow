from uuid import uuid4

import factory

from deps_high_sparrow.domain.model.document_type import CrossFieldValidator
from deps_high_sparrow.domain.model.shared import EntityCode, Severity
from tests.factories.cross_field_issue_message import CrossFieldIssueMessageFactory

__all__ = ["CrossFieldValidatorFactory"]


class CrossFieldValidatorFactory(factory.Factory):
    class Meta:
        model = CrossFieldValidator

    id_ = factory.LazyFunction(lambda: uuid4().hex)
    name = factory.Sequence(lambda n: f"validator_{n}")
    description = factory.Sequence(lambda n: f"Description for validator_{n}")
    rule = "Ffield1 == Ffield2"
    severity = factory.LazyFunction(lambda: Severity.ERROR)
    validated_fields = factory.LazyFunction(lambda: [EntityCode("field1"), EntityCode("field2")])
    issue_message = factory.SubFactory(CrossFieldIssueMessageFactory)
    for_each = False
    for_any = False
