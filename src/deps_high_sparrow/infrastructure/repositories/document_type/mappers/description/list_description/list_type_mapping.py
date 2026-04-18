from deps_high_sparrow.domain import OperandType

from ..key_value_description import KeyValueDescriptionMapper
from ..table_description import TableDescriptionMapper
from ..type_mapping import TYPE_MAPPING

__all__ = ["LIST_TYPE_MAPPING"]

LIST_TYPE_MAPPING = TYPE_MAPPING
LIST_TYPE_MAPPING.update(
    {
        OperandType.TABLE: TableDescriptionMapper,
        OperandType.DICT: KeyValueDescriptionMapper,
    },
)
