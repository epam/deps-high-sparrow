from dataclasses import asdict, dataclass, field
from inspect import signature

from .constants import Severity


@dataclass
class RuleEntityMeta:
    need_warning_even_if_optional: bool = False
    for_each: bool = False
    for_any: bool = False
    check_optional_fields: bool = False

    @classmethod
    def from_dict(cls, **values):
        return cls(**{key: value for key, value in values.items() if key in signature(cls).parameters})

    def as_dict(self):
        data = {}
        for key, parameter in signature(self.__class__).parameters.items():
            instance_value = getattr(self, key)
            if instance_value != parameter.default:
                data[key] = instance_value
        return data


@dataclass
class RuleEntity:
    id: int
    name: str
    severity: Severity
    field_code: str
    document_type_code: str
    rule: str
    issue_message: str
    is_active: bool = True
    meta: RuleEntityMeta = field(default_factory=RuleEntityMeta)

    def __post_init__(self):
        if isinstance(self.meta, dict):
            self.meta = RuleEntityMeta.from_dict(**self.meta)

    def as_dict(self):
        entity_dict = asdict(self)
        entity_dict["severity"] = self.severity.value
        entity_dict["meta"] = self.meta.as_dict()

        return entity_dict
