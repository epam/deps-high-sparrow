import logging
import re
from typing import Optional, Tuple

from ...dto.prepared_field import DictDataToValidate
from ...entities.constants import DICT_ITEMS
from ...entities.rule import RuleEntity
from ..constants import NAME_SEPARATOR

_logger = logging.getLogger(__name__)


class RulePositionExtractor:
    CELL_SUBSCRIPT_PATTERN = r"\[\d+\]\[\d+\]"
    CELL_FUNCTION_PATTERN = r"\bcell\("
    ARRAY_SUBSCRIPT_PATTERN = r"\b[a-zA-Z_]\w*\[(\d+)\]"
    ARRAY_KV_SUBSCRIPT_PATTERN = r"\b[a-zA-Z_]\w*\[(\d+)\]\[([01])\]"
    FIELD_SUBSCRIPT_PATTERN = r"\b[a-zA-Z_]\w*\[(\d+)\]\[(\d+)\]"
    CELL_FUNCTION_EXTRACTION_PATTERN = r"\bcell\(\s*[a-zA-Z_]\w*\s*,\s*(\d+)\s*,\s*(\d+)\s*\)"

    def has_explicit_cell_subscript(self, rule: RuleEntity) -> bool:
        if re.search(self.CELL_SUBSCRIPT_PATTERN, rule.rule):
            return True
        if re.search(self.CELL_FUNCTION_PATTERN, rule.rule):
            return True
        return False

    def get_cell_position(self, rule: RuleEntity) -> Tuple[Optional[int], Optional[int]]:
        # First, try to match direct subscript pattern: Ftable[column][row]
        match = re.search(self.FIELD_SUBSCRIPT_PATTERN, rule.rule)
        if match:
            return int(match.group(1)), int(match.group(2))

        # Second, try to match cell() function: cell(Ftable, column, row)
        match = re.search(self.CELL_FUNCTION_EXTRACTION_PATTERN, rule.rule)
        if match:
            column = int(match.group(1))
            row = int(match.group(2))
            return column, row

        _logger.debug(f"Could not extract cell position from rule: {rule.rule}")
        return None, None

    def has_explicit_array_subscript(self, rule: RuleEntity) -> bool:
        return bool(re.search(self.ARRAY_SUBSCRIPT_PATTERN, rule.rule))

    def get_array_position(self, rule: RuleEntity) -> Tuple[Optional[int], Optional[str]]:
        # Match pattern like: field_name[index][kv_index]
        match = re.search(self.ARRAY_KV_SUBSCRIPT_PATTERN, rule.rule)
        if match:
            index = int(match.group(1))
            kv_index = int(match.group(2))
            kv_id = DICT_ITEMS[kv_index]
            return index, kv_id.value

        # Match pattern like: field_name[index]
        match = re.search(self.ARRAY_SUBSCRIPT_PATTERN, rule.rule)
        if match:
            return int(match.group(1)), None

        _logger.debug(f"Could not extract array position from rule: {rule.rule}")
        return None, None

    def get_dict_item_index(
        self,
        used_variables: set,
        field: DictDataToValidate,
        rule: RuleEntity,
        legacy_field_name: str,
        modern_field_name: str,
    ) -> int:
        # Check rule text for bracket notation first (e.g., Ffield[0] or Ffield[1])
        match = re.search(rf"\b{re.escape(modern_field_name)}\[([01])\]", rule.rule)
        if not match:
            match = re.search(rf"\b{re.escape(legacy_field_name)}\[([01])\]", rule.rule)

        if match:
            return int(match.group(1))

        # Fall back to checking used_variables for subscript notation (e.g., field__0 or field__1)
        for variable in used_variables:
            try:
                field_name, index = variable.rsplit(NAME_SEPARATOR, 1)
                if field_name in (legacy_field_name, modern_field_name) and int(index) in {0, 1}:
                    return int(index)
            except ValueError:
                pass
        # Use "key" as a fallback value if no used_variables
        return 0
