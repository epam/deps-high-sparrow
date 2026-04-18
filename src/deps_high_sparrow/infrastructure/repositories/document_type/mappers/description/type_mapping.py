from deps_high_sparrow.domain.model import OperandType

from .basic_description import BasicDescriptionMapper
from .date_description import DateDescriptionMapper
from .enum_description import EnumDescriptionMapper
from .string_description import StringDescriptionMapper

__all__ = ["TYPE_MAPPING"]


TYPE_MAPPING = {  # noqa: WPS407
    OperandType.STRING: StringDescriptionMapper,
    OperandType.NUMBER: BasicDescriptionMapper,
    OperandType.BOOL: BasicDescriptionMapper,
    OperandType.RANGE: BasicDescriptionMapper,
    OperandType.DATETIME: BasicDescriptionMapper,
    OperandType.TIME: BasicDescriptionMapper,
    OperandType.ENUM: EnumDescriptionMapper,
    OperandType.DATE: DateDescriptionMapper,
}
