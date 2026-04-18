import factory.fuzzy
from faker import Faker
from pytest_factoryboy import register

from deps_high_sparrow.domain.model.document_type.validator.validation.dto.prepared_field import (
    FieldDataToValidate,
)
from deps_high_sparrow.domain.model.document_type.validator.validation.entities.constants import (
    OperandType,
)
from deps_high_sparrow.domain.model.document_type.validator.validation.entities.mapper import (
    get_field_type_meta_class,
)

fake = Faker()


@register
class FieldDataToValidateFactory(factory.Factory):
    class Meta:
        model = FieldDataToValidate

    field_type = factory.fuzzy.FuzzyChoice(OperandType)
    field_value = factory.Faker("word")
    document_id = factory.Faker("pyint")
    field_code = factory.Faker("word")
    document_type_code = factory.Faker("word")

    @factory.lazy_attribute
    def meta(self):
        if self.field_type == OperandType.STRING:
            return get_field_type_meta_class("string")()
        return get_field_type_meta_class(str(self.field_type.value))()
