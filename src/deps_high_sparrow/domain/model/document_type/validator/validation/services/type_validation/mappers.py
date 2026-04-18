import datetime
import re
from typing import List, Union

from ...entities.constants import OperandType
from ..frange import frange
from .constants import DATE_FORMATS


def convert_to_frange(x: str) -> Union[frange, List]:
    # Find structure like: '  range(   21.16226   ,   25,5   )  '
    regex = re.compile(
        r"""
        range\(
            (?: # group with spaces and digits
                [ ]* #space after '('
                ( #group with first number
                    (?:-?\d+) #integer part of number
                    (?:\.\d*)? #decimal part of number
                )
                [ ]*\,[ ]* #spaces and semicolon
                ( #group with second number
                    (?:-?\d+) #integer part of number
                    (?:\.\d*)? #decimal part of number
                )
                [ ]* #spaces before \)

            )

        \)
    """,
        re.VERBOSE,
    )
    result = re.findall(regex, x)
    if not result:
        return []
    result = result[0]
    start, end = float(result[0]), float(result[1])
    return frange(start, end)


def cast_date(date: str):
    for num, date_format in enumerate(DATE_FORMATS):
        try:
            res = datetime.datetime.strptime(date, date_format).date()
            break
        except ValueError:
            if num == len(DATE_FORMATS) - 1:
                raise

    return res


TYPE_MAPPER = {  # noqa: WPS407
    OperandType.STRING: str,
    OperandType.NUMBER: float,
    OperandType.BOOL: bool,
    OperandType.RANGE: convert_to_frange,
    OperandType.DATE: cast_date,
    OperandType.ARRAY: list,
}
