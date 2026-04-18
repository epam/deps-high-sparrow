import random

import factory

from deps_high_sparrow.domain import Issue, IssueType, Severity

__all__ = ["IssueFactory"]


class IssueFactory(factory.Factory):
    class Meta:
        model = Issue

    severity = factory.LazyFunction(lambda: random.choice(list(Severity)))
    type = factory.LazyFunction(lambda: random.choice(list(IssueType)))
    message = factory.Faker("sentence")
