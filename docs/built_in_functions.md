# Built-in Functions for Validation Rules

This page lists all built-in functions available for use in custom validation rule expressions. These functions extend basic Python syntax with useful helpers for working with strings, dates, fields, and document data.

---

## Basic Functions

| Function | Description |
|----------|-------------|
| `all(iterable)` | Returns `True` if all elements in the iterable are true. |
| `any(iterable)` | Returns `True` if at least one element is true. |
| `len(value)` | Returns the number of items in a container. |
| `min(values)` | Returns the smallest item in an iterable. |
| `max(values)` | Returns the largest item in an iterable. |
| `range(start, end)` | Returns a list of numbers from `start` to `end` (inclusive). Supports float values. |

---

## Date & Time Functions

| Function | Description |
|----------|-------------|
| `today()` | Returns the current date (`datetime.date`) object. |
| `today_iso()` | Returns the current datetime as an ISO-formatted string. |
| `date(day, month, year)` | Constructs a `date` object from integers. |
| `validate_timedelta(date1, date2, diff, frames="days", op="eq")` | Checks if `date1 + diff` equals or compares with `date2` (e.g., `gt`, `lt`). `frames` can be `"days"`, `"years"`, etc. |
| `compare_dates(date1, date2, op="gt")` | Compares two dates using operator: `gt`, `lt`, `eq`, etc. |
| `validate_date_for_specific_format(value, format)` | Checks if a date string matches a specific format like `%Y-%m-%d`. |

---

## Validation Utilities

| Function | Description |
|----------|-------------|
| `is_currency_code(code)` | Validates if the value is a known ISO 4217 currency code. |
| `is_country_code(code)` | Validates if the value is a valid ISO 3166-1 alpha-2 country code. |
| `is_phone_number(number)` | Checks if the value is a valid phone number. |
| `is_phone_number_for_country(number, country_code)` | Validates phone number against a specific country. |
| `is_unique(value, list)` | Checks if `value` appears exactly once in the given list. |
| `is_state(value)` | Validates US state names or codes. |
| `is_postal_code(value)` | Validates a U.S. 5-digit ZIP code. |
| `is_city(value)` | Validates a city name (letters, numbers, spaces, hyphens, commas). |
| `validate_ssn_format(value)` | Checks if the value is a valid SSN format (`XXX-XX-XXXX` or 9-digit). |
| `validate_ssn_content(value)` | Ensures all characters in SSN are digits or dashes. |
| `validate_field_content(value, regex)` | Validates that `value` matches the given regular expression. |

---

## Field & Table Utilities

| Function | Description |
|----------|-------------|
| `cell(table, column, row)` | Retrieves a specific cell value from a 2D table (dictionary format). |
| `check_dependency(depended, *others)` | Returns `True` if `depended` has value or any of the `others` has a value. |
| `find_value_by_key(pairs, key)` | Given a list of `[key, value]` pairs, returns the value matching the given key. |

---

## Text & Format Helpers

| Function | Description |
|----------|-------------|
| `lower(value)` | Converts the string to lowercase. |
| `is_alpha(value)` | Returns `True` if all characters are alphabetic. |
| `is_name(value)` | Returns `True` if the string is a valid name (letters and spaces). |
| `is_numeric(value)` | Checks if the string contains only numbers and common numeric characters (`()+`). |
| `is_telephone(value)` | Validates a phone/telephone format (`0-9`, `()`, `+`, `-`, spaces). |
| `str_replace_endings(value, new)` | Replaces all newline characters (`\n`) in a string with `new`. |
| `merge_whitespaces(value)` | Collapses multiple whitespace characters into a single space. |

---

## Notes

- All functions are safe for use within rule expressions.
- Field values should be accessed using the `F<fieldCode>` format and cast appropriately (`int()`, `str()`, etc.).
- Validation logic is executed in a controlled environment — external imports and functions are restricted.

---

## Example Usage

```python
int(F12345) > 100 and is_currency_code(FcurrencyField)
```
