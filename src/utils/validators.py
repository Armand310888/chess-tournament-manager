"""Validation helpers and validation constants."""

from datetime import date, datetime
import re
from enum import Enum


class Pattern(Enum):
    """"""
    STREET_NUMBER = re.compile(r"^\d+\s?(bis|ter|[A-Za-z])?$")
    POSTAL_CODE = re.compile(r"^\d{5}$")
    CHESS_NATIONAL_ID = re.compile(r"^[A-Z]{2}\d{5}$")
    ID = re.compile(r"^[TRM]\d{3,}$")


class PatternDescription(Enum):
    """"""
    STREET_NUMBER = (
        "One or more digits, optionally followed by a space "
        "and a suffix such as 'bis' or 'ter', or a single letter. "
        "Examples: 12, 12 bis, 12A"
    )
    POSTAL_CODE = "five positive digits. Example: 92700"
    CHESS_NATIONAL_ID = (
        "Two uppercase letters followed by five digits. "
        "Example: AB12345 "
        )
    ID = (
        "ID starts with one letter:\n"
        "- 'T' for tournament object\n"
        "- 'R' for round object\n"
        "- 'M' for match object\n"
        "Then the letter is followed by at least three digits\n"
        "Examples: M001, T012, R1520"
    )


ELO_MINIMUM = 0
ELO_MAXIMUM = 3000


def validate_non_empty_string(value: str, field_name: str) -> str:
    """Validate and clean a non-empty string.

    Args:
        value: Value to validate.
        field_name: Name of the validated field, used in error messages.

    Raises:
        TypeError: If value is not a string.
        ValueError: If value is empty after stripping whitespace.

    Returns:
        The cleaned string.
    """
    if not isinstance(value, str):
        raise TypeError(f"'{field_name}' must be a string")

    cleaned_value = value.strip()

    if not cleaned_value:
        raise ValueError(f"'{field_name}' must be a non-empty string")

    return cleaned_value


def validate_regex_match(
        value: str,
        field_name: str,
        regex_pattern: Pattern,
        pattern_description: PatternDescription
) -> str:
    """Validate that a string matches a regular expression.

    The value is stripped and converted to uppercase before validation.

    Args:
        value: String value to validate.
        field_name: Name of the validated field.
        regex_pattern: Regular expression pattern to match.
        pattern_description: Human-readable description of the expected format.

    Raises:
        TypeError: If value is not a string.
        ValueError: If value does not match the expected pattern.

    Returns:
        The cleaned uppercase string.
    """
    if not isinstance(regex_pattern, Pattern):
        raise TypeError("'regex_pattern' must be a Pattern object.")

    if not isinstance(pattern_description, PatternDescription):
        raise TypeError(
            "'pattern_description' must be a PatternDescription object."
        )

    cleaned_value = (
        validate_non_empty_string(value, field_name).upper()
    )

    if not regex_pattern.value.fullmatch(cleaned_value):
        raise ValueError(
            f"'{field_name}' format must be: "
            f"'{pattern_description.value}"
        )

    return cleaned_value


def validate_date_or_datetime(
        value: str | date | datetime,
        field_name: str,
) -> date | datetime:
    """Validate and normalize a date or datetime value.

    Accept either a string in ISO format (YYYY-MM-DD), a date,
    or a datetime object, and return a date instance.

    Args:
        value: Value to validate.
        field_name: Name of the field, used in error messages.

    Returns:
        A valid date object.

    Raises:
        TypeError: If value is not a string, date, or datetime.
        ValueError: If the string cannot be parsed as a valid date.
    """
    if isinstance(value, (date, datetime)):
        return value

    if not isinstance(value, str):
        raise TypeError(
            f"'{field_name}' must be a string, date, or datetime."
        )

    cleaned_value = validate_non_empty_string(value, field_name)

    try:
        return date.fromisoformat(cleaned_value)
    except ValueError:
        raise ValueError(
            f"'{field_name}' must be a valid date or datetime in isoformat.\n"
            "YYYY-MM-DD  HH:MM:SS\n")


def validate_date_order(
        start_date: date | datetime,
        end_date: date | datetime
) -> None:
    """Validate that an end date is not before a start date.

    If both values are datetimes, the end datetime must be strictly later than
    the start datetime. If both values are dates, the end date may be equal to
    the start date but cannot be earlier.

    Args:
        start_date: Start date or datetime.
        end_date: End date or datetime.

    Raises:
        TypeError: If start_date and end_date do not have the same type.
        ValueError: If the date order is invalid.
    """
    if type(start_date) is not type(end_date):
        raise TypeError(
            "start_date and end_date must be of the same type: "
            "date or datetime."
        )

    if isinstance(start_date, datetime):
        if end_date <= start_date:
            raise ValueError(
                "End date and time must be later than the start date and time"
            )

    elif isinstance(start_date, date):
        if end_date < start_date:
            raise ValueError(
                "End date cannot be before start date"
            )


def validate_number(
    value: int | float,
    field_name: str,
    expected_type: type,
    minimum: int | float | None = None,
    maximum: int | float | None = None,
) -> int | float:
    """Validate a number type and optional bounds.

    Args:
        value: Numeric value to validate.
        field_name: Name of the validated field.
        expected_type: Expected numeric type, either int or float.
        minimum: Optional inclusive minimum value.
        maximum: Optional inclusive maximum value.

    Raises:
        TypeError: If arguments have invalid types.
        ValueError: If bounds are inconsistent or value is outside bounds.

    Returns:
        The validated numeric value.
    """
    if expected_type not in (int, float):
        raise TypeError("'expected_type' must be int or float.")

    if minimum is not None:
        if not isinstance(minimum, (int, float)):
            raise TypeError("'minimum' must be an int or a float.")

    if maximum is not None:
        if not isinstance(maximum, (int, float)):
            raise TypeError("'maximum' must be an int or a float.")

    if minimum is not None and maximum is not None and minimum > maximum:
        raise ValueError("'minimum' cannot be greater than 'maximum'.")

    if not isinstance(value, expected_type):
        raise TypeError(
            f"'{field_name}' must be of type {expected_type.__name__}."
        )

    if minimum is not None and value < minimum:
        raise ValueError(
            f"'{field_name}' must be greater than or equal to {minimum}."
        )

    if maximum is not None and value > maximum:
        raise ValueError(
            f"'{field_name}' must be less than or equal to {maximum}."
        )

    return value


def validate_class_object(
        value: object,
        field_name: str,
        expected_class: type
) -> object:
    """Validate that a value is an instance of the expected class.

    Args:
        value: Object to validate.
        field_name: Name of the validated field.
        expected_class: Expected class.

    Raises:
        TypeError: If value is not an instance of expected_class.

    Returns:
        The validated object.
    """

    if not isinstance(value, expected_class):
        raise TypeError(
            f"'{field_name}' must be a '{expected_class.__name__}' object"
        )

    return value

def validate_ID():
    pass