"""Reusable validation helpers for models and console inputs."""

from datetime import date, datetime
import re
from enum import Enum


class Pattern(Enum):
    """Store regular expressions used by validators."""

    STREET_NUMBER = re.compile(r"^\d+\s?(bis|ter|[A-Za-z])?$")
    POSTAL_CODE = re.compile(r"^\d{5}$")
    CHESS_NATIONAL_ID = re.compile(r"^[A-Z]{2}\d{5}$")
    ID = re.compile(r"^[TRM]\d{3,}$")


class PatternDescription(Enum):
    """Store user-facing descriptions of expected input formats."""

    STREET_NUMBER = (
        "One or more digits, optionally followed by a space\n"
        "and a suffix such as 'bis' or 'ter', or a single letter.\n"
        "Examples: 12, 12 bis, 12A"
    )
    POSTAL_CODE = (
        "five positive digits.\n"
        "Example: 92700"
    )
    CHESS_NATIONAL_ID = (
        "Two uppercase letters followed by five digits.\n"
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


def validate_non_empty_string(
        value: str,
        field_name: str,
        max_length: int | None = None,
) -> str:
    """Validate a non-empty string and return it stripped."""

    if not isinstance(value, str):
        raise TypeError(f"'{field_name}' must be a string.")

    if max_length is not None:
        if not isinstance(max_length, int):
            raise TypeError(f"'{max_length}' must be an integer.")

    cleaned_value = value.strip()

    if not cleaned_value:
        raise ValueError(f"'{field_name}' must be a non-empty string.")

    if max_length is not None and len(cleaned_value) > max_length:
        raise ValueError(
            f"'{field_name}' must be {max_length} characters maximum."
        )

    return cleaned_value


def validate_person_name(
    value: str,
    field_name: str,
    max_length: int | None = None,
) -> str:
    """Validate a person's name."""

    cleaned_value = validate_non_empty_string(
        value,
        field_name,
        max_length
    )

    if not re.fullmatch(
        r"[A-Za-zÀ-ÖØ-öø-ÿ' -]+",
        cleaned_value
    ):
        raise ValueError(
            f"'{field_name}' contains invalid characters "
            "such as numbers or unsupported signs."
        )

    return cleaned_value


def validate_regex_match(
        value: str,
        field_name: str,
        regex_pattern: Pattern,
        pattern_description: PatternDescription
) -> str:
    """Validate a string against a predefined regex pattern.

    The value is stripped and converted to uppercase before matching.
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
            f"{pattern_description.value}"
        )

    return cleaned_value


def validate_date(
        value: str | date,
        field_name: str,
) -> date | datetime:
    """Validate and return a date from an ISO date string.

    Existing date objects are returned unchanged.
    """
    if isinstance(value, datetime):
        raise TypeError(f"'{field_name}' must be a date, not a datetime.")

    if isinstance(value, date):
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
            f"'{field_name}' must be a valid date in isoformat.\n"
            "YYYY-MM-DD")


def validate_datetime(
        value: str | datetime,
        field_name: str,
) -> date | datetime:
    """Validate and return a datetime from an ISO datetime string.

    Existing datetime objects are returned unchanged.
    """

    if isinstance(value, datetime):
        return value

    if not isinstance(value, str):
        raise TypeError(
            f"'{field_name}' must be a string, date, or datetime."
        )

    cleaned_value = validate_non_empty_string(value, field_name)

    try:
        return datetime.fromisoformat(cleaned_value)
    except ValueError:
        raise ValueError(
            f"'{field_name}' must be a valid datetime in isoformat.\n"
            "YYYY-MM-DD HH:MM:SS")


def validate_date_order(
        start_date: date | datetime,
        end_date: date | datetime
) -> None:
    """Validate chronological order between two dates or datetimes.

    Dates may be equal. Datetimes must be strictly ordered.
    """

    if type(start_date) is not type(end_date):
        raise TypeError(
            "start_date and end_date must be of the same type: "
            "date or datetime."
        )

    if isinstance(start_date, datetime):
        if end_date <= start_date:
            raise ValueError(
                "End date and time must be later than the start date and time."
            )

    elif isinstance(start_date, date):
        if end_date < start_date:
            raise ValueError(
                "End date cannot be before start date."
            )


def validate_number(
    value: str,
    field_name: str,
    expected_type: type,
    minimum: int | float | None = None,
    maximum: int | float | None = None,
) -> int | float:
    """Validate and convert a numeric value.

    The returned value keeps the requested type: int or float.
    Optional bounds are inclusive.
    """

    if expected_type not in (int, float):
        raise TypeError("'expected_type' must be integer or float.")

    try:
        number = expected_type(value)
    except ValueError as error:
        raise ValueError(
            f"'{field_name}' must be a valid number."
        ) from error

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

    if minimum is not None and number < minimum:
        raise ValueError(
            f"'{field_name}' must be greater than or equal to {minimum}."
        )

    if maximum is not None and number > maximum:
        raise ValueError(
            f"'{field_name}' must be less than or equal to {maximum}."
        )

    return number


def validate_class_object(
        value: object,
        field_name: str,
        expected_class: type
) -> object:
    """Validate that a value is an instance of the expected class."""

    if not isinstance(value, expected_class):
        raise TypeError(
            f"'{field_name}' must be a '{expected_class.__name__}' object."
        )

    return value
