import operator
import re
from datetime import date, datetime
from typing import Any, Dict, List, Union

import us
from dateutil.parser import parse as du_parse
from dateutil.relativedelta import relativedelta
from iso3166 import countries_by_alpha2
from iso4217 import Currency
from phonenumbers import is_valid_number, is_valid_number_for_region, parse

from ..utils import has_value


def to_date(day: Union[str, int], month: Union[str, int], year: Union[str, int]) -> date:
    return date(day=int(day), month=int(month), year=int(year))


def validate_timedelta(
    first_date_str: Union[datetime, date, str],
    second_date_str: Union[datetime, date, str],
    diff: int,
    frames: str = "days",
    op: str = "eq",
):
    """Compare first date shifted by a relative delta to a second date.

    - first_date_str, second_date_str: datetime/date/ISO string
    - frames: one of 'years', 'months', 'weeks', 'days', 'hours', 'minutes', 'seconds'
    - diff: integer amount applied to the given frames
    - op: comparison operator name: 'eq', 'ne', 'lt', 'le', 'gt', 'ge'

    Returns: bool result of op(first + relativedelta(...), second)
    """
    operation = getattr(operator, op)
    delta = relativedelta(**{frames: diff})  # type: ignore

    if isinstance(first_date_str, date):
        first_date_str = datetime.combine(first_date_str, datetime.min.time())
    if isinstance(second_date_str, date):
        second_date_str = datetime.combine(second_date_str, datetime.min.time())

    if isinstance(first_date_str, str):
        first_date_str = du_parse(first_date_str)
    if isinstance(second_date_str, str):
        second_date_str = du_parse(second_date_str)

    return operation(first_date_str + delta, second_date_str)


def validate_currency_code(currency_code: str) -> bool:
    """Return True if `currency_code` is a valid ISO 4217 code (incl. special X-codes)."""
    currency_code = currency_code.upper()
    try:
        return bool(Currency(currency_code))
    except ValueError:
        return currency_code in {
            "XAG",
            "XAU",
            "XBA",
            "XBB",
            "XBC",
            "XBD",
            "XPD",
            "XPT",
            "XSU",
            "XUA",
            "XDR",
        }


def validate_country_code(country_code: str) -> bool:
    """Return True if `country_code` is a valid ISO-3166 alpha-2 code."""
    return bool(countries_by_alpha2.get(country_code.upper(), False))


def validate_phone_number(phone_number: str) -> bool:
    """Validate international phone number format using libphonenumber."""
    return is_valid_number(parse(phone_number))


def validate_phone_number_for_country(phone_number: str, country_code: str) -> bool:
    """Validate that `phone_number` is valid for the given `country_code`."""
    return is_valid_number_for_region(parse(phone_number), country_code)


def is_unique(value: Any, value_list: List[Any]):
    """Check that `value` occurs exactly once in `value_list`."""
    return value_list.count(value) == 1


def is_state(value: str) -> bool:
    """Return True if `value` matches a US state (code or name)."""
    return bool(us.states.lookup(value))


def is_postal_code(value: str) -> bool:
    """Validate a 5-digit US postal/ZIP code."""
    return bool(re.compile("[0-9]{5}").fullmatch(value))


def is_city(value: str) -> bool:
    """Validate city-like text (letters, digits, spaces, hyphen, comma)."""
    return bool(re.compile(r"[a-zA-Z \-,0-9]*").fullmatch(value))


def validate_ssn_format(value: str) -> bool:
    """Validate SSN format: 9 digits or XXX-XX-XXXX pattern."""
    ssn_regexp = re.compile(r"(?:(.){9}|(.){3}-(.){2}-(.){4})\b")
    return bool(ssn_regexp.fullmatch(value.strip()))


def validate_ssn_content(value: str) -> bool:
    """Ensure SSN contains only digits and hyphens (no letters/symbols)."""
    return all(ch.isdigit() or ch == "-" for ch in value)


def validate_date_for_specific_format(value: Union[datetime, date, str], format_: str) -> bool:
    try:
        if isinstance(value, (datetime, date)):  # This skips format validation for datetime and date types
            return True

        return bool(datetime.strptime(value.strip(), format_))
    except (ValueError, TypeError):
        return False


def is_telephone(value: str) -> bool:
    """Validate telephone-like content (digits, spaces, +, -, parentheses)."""
    return bool(re.compile(r"[0-9 \-()+]*").fullmatch(value))


def get_table_cell(value: Dict[int, Dict[int, Any]], column: int, row: int) -> Any:
    """Return the cell value from a 2-level dict by `column` and `row` indices."""
    return value[column][row]


def check_dependency(depended_cell_value, *cells_to_check_values) -> bool:
    """
    Some crap, works very strangly...
    """
    if has_value(depended_cell_value):
        return True
    return any(has_value(value) for value in cells_to_check_values)


def validate_field_content(value: str, content_regexp: str) -> bool:
    """
    Deprecated: use regex_match instead
    """
    return bool(re.compile(content_regexp).fullmatch(value.strip()))


def regex_match(value: str, regex: str) -> bool:
    """
    Validate that the value matches the given regex
    """
    return bool(re.compile(regex).fullmatch(value.strip()))


def compare_dates(first_date: str, second_date: str, op: str = "gt") -> bool:
    """Compare two date/time strings using operator `op` (e.g., 'gt', 'lt', 'eq')."""
    operation = getattr(operator, op)
    return operation(du_parse(first_date), du_parse(second_date))


def find_value_by_key(value_list: List[List[Any]], key: str) -> Any:
    for value in value_list:
        if not isinstance(value, list) or len(value) < 2:
            raise ValueError("Each element in value_list must be a list with at least two elements")

        if value[0] == key:
            return value[1]

    raise KeyError(f"Key '{key}' not found in the list")


def today() -> str:
    """Return current date-time in ISO 8601 string format."""
    return datetime.now().isoformat()


def str_replace_endings(value: str, new: str) -> str:
    """Replace newline characters in `value` with `new`."""
    return value.replace("\n", new)


def merge_whitespaces(value: str) -> str:
    """Collapse consecutive whitespace in `value` to single spaces and trim edges."""
    return " ".join(value.split())
