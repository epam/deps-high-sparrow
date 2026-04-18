import ast
import logging
from collections import defaultdict
from dataclasses import dataclass
from dataclasses import field as dataclass_field
from typing import Any, Callable, DefaultDict, Dict, List, Optional, Union

from ..dto.field import FieldCodeAndDocumentType
from ..dto.prepared_field import (
    ArrayDataToValidate,
    BaseDataToValidate,
    DictDataToValidate,
    FieldDataToValidate,
    TableDataToValidate,
)
from ..dto.validation import ValidationResultDTO
from ..entities.constants import KeyValueId, OperandType, Severity
from ..entities.rule import RuleEntity
from ..exceptions import InvalidSyntax
from .constants import ITEM_OF_PREFIX, NAME_SEPARATOR, TYPE_PREFIX
from .type_validation.mappers import TYPE_MAPPER

logger = logging.getLogger(__name__)


@dataclass
class Message:
    message: str
    column: Optional[int] = None
    row: Optional[int] = None
    index: Optional[int] = None
    kv_id: Optional[KeyValueId] = None

    def __hash__(self):
        return hash(f"{self.message}-{self.column}-{self.row}-{self.index}-{self.kv_id}")

    def __eq__(self, other):
        if not isinstance(other, Message):
            return False
        return (
            self.message == other.message
            and self.column == other.column
            and self.row == other.row
            and self.index == other.index
            and self.kv_id == other.kv_id
        )

    def as_issue(self) -> dict[str, Union[str, int, None]]:
        return {
            "message": self.message,
            "column": self.column,
            "row": self.row,
            "index": self.index,
            "kv_id": self.kv_id.value if self.kv_id is not None else self.kv_id,
        }


@dataclass
class FieldValidationIssues:
    field_code: str
    document_id: int
    errors: List[Message] = dataclass_field(default_factory=list)
    warnings: List[Message] = dataclass_field(default_factory=list)

    def add(self, severity: Severity, message: Message) -> None:
        if severity == Severity.ERROR:
            self.errors.append(message)
            return
        self.warnings.append(message)


def cast_field(field_value: Any, field_type: OperandType) -> Any:
    try:
        local_cast_field = TYPE_MAPPER[field_type](field_value)  # type: ignore
    except Exception as exception:
        logger.debug(exception)
    else:
        return local_cast_field

    return field_value


def field_full_name(
    field: Union[
        RuleEntity,
        BaseDataToValidate,
        FieldDataToValidate,
        TableDataToValidate,
        DictDataToValidate,
    ]
) -> str:
    full_name = f"{TYPE_PREFIX}{field.document_type_code}{NAME_SEPARATOR}{field.field_code}"
    if "-" in full_name:
        full_name = full_name.replace("-", "_")
    return full_name


def document_type_and_field_name_by_full_name(
    full_name: str,
) -> FieldCodeAndDocumentType:
    document_type, field_code = full_name.split(NAME_SEPARATOR)
    return FieldCodeAndDocumentType(field_code=field_code, document_type_code=document_type)


def convert_table_to_raw(table: TableDataToValidate) -> Dict[int, Any]:
    raw: DefaultDict[int, Dict[int, Any]] = defaultdict(dict)
    for cell in table.data.cells:
        raw[cell.coordinates.column][cell.coordinates.row] = cell.value

    return dict(raw)


def fields_values_hash_table(
    fields: List[
        Union[
            FieldDataToValidate,
            TableDataToValidate,
            ArrayDataToValidate,
            BaseDataToValidate,
            DictDataToValidate,
        ]
    ],
) -> Dict[str, Any]:
    """
    This function creates a hash table between Fields and their values.
    Keys of this table (field_codes) will be available to reference in rules.
    """
    fields_hash_table = {}

    data_mappers: DefaultDict[OperandType, Callable] = defaultdict(
        lambda: lambda field: field.data.value  # noqa: WPS430
    )
    data_mappers.update(
        {
            OperandType.ARRAY: lambda field: [data_mappers[item.field_type](item) for item in field.data.items],
            OperandType.TABLE: convert_table_to_raw,
            OperandType.DICT: lambda field: [data_mappers[item.field_type](item) for item in field.data.items],
        }
    )

    # Legacy naming support for backward compatibility - type__doc_type__field_code
    for local_field in fields:
        key = field_full_name(local_field)
        mapper = data_mappers[local_field.field_type]
        fields_hash_table[key] = mapper(local_field)

    # New naming convention with - F<field_code>
    # We must start each of our field reference with 'F' because <field_code> can be invalid Python variable
    # if starts with number
    for local_field in fields:
        key = build_modern_field_name(local_field.field_code)
        mapper = data_mappers[local_field.field_type]
        fields_hash_table[key] = mapper(local_field)

    return fields_hash_table


def is_errors(field_validation_issues: FieldValidationIssues) -> List[Message]:
    return field_validation_issues.errors


def is_validation_issues(
    field_validation_issues: FieldValidationIssues,
) -> List[Message]:
    return is_errors(field_validation_issues) or field_validation_issues.warnings


def check_rule_syntax(rule: str):
    try:
        ast.parse(rule)
    except Exception as exception:
        raise InvalidSyntax(exception.args[0])


def has_value(field_value) -> bool:
    return field_value is not None and field_value != ""


def all_table_cells_in_bounds(table_data: TableDataToValidate) -> bool:
    """
    Check if there are no cells with a colum outside the table columns range
    """
    valid_column_indices: set[int] = {column.index for column in table_data.meta.columns}
    cells_column_indices: set[int] = {cell.coordinates.column for cell in table_data.data.cells}
    return not bool(cells_column_indices - valid_column_indices)


def build_colum_full_name(field: TableDataToValidate, column_index):
    return f"{TYPE_PREFIX}{field.document_type_code}{NAME_SEPARATOR}{field.field_code}{NAME_SEPARATOR}{column_index}"


def build_item_of_array_field_code(field_code: str) -> str:
    return f"{ITEM_OF_PREFIX}{NAME_SEPARATOR}{field_code}"


def add_error_marker(field: BaseDataToValidate, validation_issues: FieldValidationIssues):
    if validation_issues.errors:
        validation_issues.add(
            Severity.ERROR,
            Message(message="{0} contains {1}s".format(field.field_type.value.capitalize(), Severity.ERROR.value)),
        )


def union_validation_results(*results: ValidationResultDTO) -> ValidationResultDTO:
    mapping = {}
    details: List[FieldValidationIssues] = [detail for result in results for detail in result.detail]
    for validation_issues in details:
        key = (
            validation_issues.field_code,
            validation_issues.field_code,
        )
        if key not in mapping:
            mapping[key] = FieldValidationIssues(
                document_id=validation_issues.document_id,
                field_code=validation_issues.field_code,
            )
        issues = mapping[key]
        issues.errors = list({*issues.errors, *validation_issues.errors})
        issues.warnings = list({*issues.warnings, *validation_issues.warnings})

    return ValidationResultDTO(
        is_valid=all(result.is_valid for result in results),
        detail=list(mapping.values()),
    )


def exclude_tables_with_invalid_size(fields: List[BaseDataToValidate]) -> None:
    for field in fields:
        if isinstance(field, TableDataToValidate) and not field.is_column_size_correct:
            fields.remove(field)


def build_dict_key_field_code(field_code: str) -> str:
    return f"{field_code}{NAME_SEPARATOR}0"


def build_dict_value_field_code(field_code: str) -> str:
    return f"{field_code}{NAME_SEPARATOR}1"


def build_dict_item_full_name(field: DictDataToValidate, index: int) -> str:
    return f"{TYPE_PREFIX}{field.document_type_code}{NAME_SEPARATOR}{field.field_code}{NAME_SEPARATOR}{index}"


def sanitize_rule(rule: RuleEntity) -> RuleEntity:
    new_rule = getattr(rule, "rule").replace(rule.document_type_code, TYPE_PREFIX + rule.document_type_code)
    setattr(rule, "rule", new_rule)
    return rule


def build_modern_field_name(field_code: str) -> str:
    return f"F{field_code.replace('-', '_')}"
