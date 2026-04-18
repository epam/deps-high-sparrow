from uuid import uuid4

import factory
from faker import Faker

from deps_high_sparrow.domain import ExternalValidator

__all__ = ["ExternalValidatorFactory"]

fake = Faker()


class ExternalValidatorFactory(factory.Factory):
    class Meta:
        model = ExternalValidator

    name = factory.LazyFunction(lambda: uuid4().hex)
    url = factory.LazyFunction(lambda: fake.url())
