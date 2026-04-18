from typing import Any

from deps_high_sparrow.domain.model import Validator

from .rule import RuleMapper
from .validator_type import ValidatorTypeMapper

__all__ = ["ValidatorMapper"]


class ValidatorMapper:
    @staticmethod
    def from_dict(raw_validator: dict[str, Any]) -> Validator:
        rules = {rule["name"]: RuleMapper.from_dict(rule) for rule in raw_validator["rules"] or []}
        return Validator(
            code=raw_validator["code"],
            type_=ValidatorTypeMapper.from_dict(raw_validator["type"]),
            is_required=raw_validator["is_required"],
            rules=rules,
        )

    @staticmethod
    def to_dict(validator: Validator) -> dict[str, Any]:
        raw_rules = [RuleMapper.to_dict(rule) for rule in validator.rules.values()]
        return {
            "code": validator.code.value,
            "type": ValidatorTypeMapper.to_dict(validator.type_),
            "is_required": validator.is_required,
            "rules": raw_rules or None,
        }
