import random
from uuid import uuid4

import factory
from faker import Faker

from deps_high_sparrow.domain import Rule, Severity

__all__ = ["RuleFactory"]

fake = Faker()


class RuleFactory(factory.Factory):
    class Meta:
        model = Rule

    name = factory.LazyFunction(lambda: uuid4().hex)
    severity = factory.LazyFunction(lambda: random.choice(list(Severity)))
    rule = factory.LazyFunction(lambda: uuid4().hex)
    issue_message = factory.LazyFunction(lambda: uuid4().hex)
    description = factory.LazyFunction(lambda: uuid4().hex)
    need_warning_even_if_optional = factory.LazyFunction(lambda: random.random() < 0.5)
    for_each = factory.LazyFunction(lambda: random.random() < 0.5)
    for_any = factory.LazyFunction(lambda: random.random() < 0.5)
    check_optional_fields = factory.LazyFunction(lambda: random.random() < 0.5)
