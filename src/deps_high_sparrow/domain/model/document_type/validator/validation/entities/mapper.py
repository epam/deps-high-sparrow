from typing import Any, Dict

from ..dto.field import (
    ArrayFieldTypeMeta,
    BasicFieldTypeMeta,
    DateFieldTypeMeta,
    DictFieldTypeMeta,
    EnumFieldTypeMeta,
    StringFieldTypeMeta,
    TableFieldTypeMeta,
)
from .constants import OperandType, Severity
from .rule import RuleEntity


def build_rule_entity(rule_dict: Dict[str, Any]) -> RuleEntity:
    return RuleEntity(
        id=rule_dict["id"],
        name=rule_dict["name"],
        severity=Severity(rule_dict["severity"]),
        field_code=rule_dict["field_code"],
        document_type_code=rule_dict["document_type_code"],
        rule=rule_dict["rule"],
        is_active=rule_dict["is_active"],
        issue_message=rule_dict["issue_message"],
        meta=rule_dict["meta"],
    )


def get_field_type_meta_class(field_type: str):
    field_meta_mapper = {
        OperandType.STRING: StringFieldTypeMeta,
        OperandType.ARRAY: ArrayFieldTypeMeta,
        OperandType.ENUM: EnumFieldTypeMeta,
        OperandType.TABLE: TableFieldTypeMeta,
        OperandType.DICT: DictFieldTypeMeta,
        OperandType.DATE: DateFieldTypeMeta,
    }
    return field_meta_mapper.get(OperandType(field_type), BasicFieldTypeMeta)


def build_meta(field_type, values_dict):
    meta_class = get_field_type_meta_class(field_type)
    try:
        return meta_class(**values_dict)
    except TypeError:
        return BasicFieldTypeMeta(**values_dict)
