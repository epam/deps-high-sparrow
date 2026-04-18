import factory

from deps_high_sparrow.domain.model.shared import EntityCode
from deps_high_sparrow.domain.model.validation_result import CrossFieldIssueMessage

__all__ = ["CrossFieldIssueMessageFactory"]


class CrossFieldIssueMessageFactory(factory.Factory):
    class Meta:
        model = CrossFieldIssueMessage

    message = factory.Sequence(lambda n: f"Issue message ${{field1}} ${{field2}} {n}")
    dependent_fields = factory.LazyFunction(lambda: [EntityCode("field1"), EntityCode("field2")])
