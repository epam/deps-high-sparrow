import factory.fuzzy
from faker import Faker
from pytest_factoryboy import register

from deps_high_sparrow.domain.model.document_type.validator.validation.entities.constants import (
    Severity,
)
from deps_high_sparrow.domain.model.document_type.validator.validation.entities.rule import (
    RuleEntity,
)

fake = Faker()


@register
class RuleFactory(factory.Factory):
    class Meta:
        model = RuleEntity

    id = factory.Faker("pyint")
    name = factory.Faker("text")
    severity = factory.fuzzy.FuzzyChoice(Severity)
    field_code = factory.Faker("word")
    document_type_code = factory.Faker("word")
    rule = factory.fuzzy.FuzzyChoice(("1+2", "True", "None != False", "(29*14/43) in range(0, 20)"))
    is_active = factory.fuzzy.FuzzyChoice((True, False))
    issue_message = factory.Faker("word")
