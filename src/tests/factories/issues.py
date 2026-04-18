import factory

from deps_high_sparrow.domain import EntityCode, Issues

from .issue import IssueFactory

__all__ = ["IssuesFactory"]


class IssuesFactory(factory.Factory):
    class Meta:
        model = Issues

    code = factory.LazyFunction(lambda: EntityCode())
    errors = factory.LazyFunction(lambda: [IssueFactory(), IssueFactory()])
    warnings = factory.LazyFunction(lambda: [IssueFactory()])
