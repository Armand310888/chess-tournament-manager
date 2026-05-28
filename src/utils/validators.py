"""Reusable validation helpers for models and console inputs."""

from datetime import date, datetime
from enum import Enum
import re


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
    """Validate and return a stripped non-empty string.

    Args:
        value: Value to validate.
        field_name: Field name used in error messages.
        max_length: Optional maximum accepted length.

    Returns:
        Stripped string value.

    Raises:
        TypeError: If value is not a string or max_length is invalid.
        ValueError: If value is empty or exceeds max_length.
    """
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
    """Validate and return a stripped person name.

    The name may contain letters, spaces, apostrophes, and hyphens.

    Args:
        value: Name value to validate.
        field_name: Field name used in error messages.
        max_length: Optional maximum accepted length.

    Returns:
        Stripped name.

    Raises:
        TypeError: If value is not a string.
        ValueError: If the name is empty, too long, or contains invalid
            characters.
    """
    cleaned_value = validate_non_empty_string(
        value,
        field_name,
        max_length,
    )

    if not re.fullmatch(
        r"[A-Za-zÀ-ÖØ-öø-ÿ' -]+",
        cleaned_value,
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
    """Validate and return a string matching a predefined pattern.

    The value is stripped and converted to uppercase before matching.

    Args:
        value: String value to validate.
        field_name: Field name used in error messages.
        regex_pattern: Pattern enum member containing the regex.
        pattern_description: Human-readable expected format.

    Returns:
        Stripped uppercase value.

    Raises:
        TypeError: If regex_pattern or pattern_description has an
            invalid type.
        ValueError: If value is empty or does not match the pattern.
    """
    if not isinstance(regex_pattern, Pattern):
        raise TypeError("'regex_pattern' must be a Pattern object.")

    if not isinstance(pattern_description, PatternDescription):
        raise TypeError(
            "'pattern_description' must be a PatternDescription object."
        )

    cleaned_value = (
        validate_non_empty_string(
            value,
            field_name
        )
    ).upper()

    if not regex_pattern.value.fullmatch(cleaned_value):
        raise ValueError(
            f"'{field_name}' format must be: "
            f"{pattern_description.value}"
        )

    return cleaned_value


def validate_date(
    value: str | date,
    field_name: str,
) -> date:
    """Validate and return a date from a date or ISO date string.

    Existing date objects are returned unchanged. Datetime objects are
    rejected to avoid silently losing time information.

    Args:
        value: Date object or ISO date string to validate.
        field_name: Field name used in error messages.

    Returns:
        Validated date.

    Raises:
        TypeError: If value is not a string or date, or if it is a
            datetime.
        ValueError: If the string is empty or not a valid ISO date.
    """
    if isinstance(value, datetime):
        raise TypeError(f"'{field_name}' must be a date, not a datetime.")

    if isinstance(value, date):
        return value

    if not isinstance(value, str):
        raise TypeError(
            f"'{field_name}' must be a string or a date."
        )

    cleaned_value = validate_non_empty_string(value, field_name)

    try:
        return date.fromisoformat(cleaned_value)
    except ValueError:
        raise ValueError(
            f"'{field_name}' must be a valid date in isoformat.\n"
            "YYYY-MM-DD"
        )


def validate_datetime(
    value: str | datetime,
    field_name: str,
) -> datetime:
    """Validate and return a datetime from a datetime or ISO string.

    Existing datetime objects are returned unchanged.

    Args:
        value: Datetime object or ISO datetime string to validate.
        field_name: Field name used in error messages.

    Returns:
        Validated datetime.

    Raises:
        TypeError: If value is not a string or datetime.
        ValueError: If the string is empty or not a valid ISO datetime.
    """
    if isinstance(value, datetime):
        return value

    if not isinstance(value, str):
        raise TypeError(
            f"'{field_name}' must be a string or a datetime."
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

    Args:
        start_date: Start date or datetime.
        end_date: End date or datetime.

    Raises:
        TypeError: If both values are not of the same date type.
        ValueError: If the end value is before the start value, or not
            strictly later for datetimes.
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

    Args:
        value: Raw value to convert.
        field_name: Field name used in error messages.
        expected_type: Numeric type to return, either int or float.
        minimum: Optional inclusive lower bound.
        maximum: Optional inclusive upper bound.

    Returns:
        Converted int or float.

    Raises:
        TypeError: If expected_type, minimum, or maximum is invalid.
        ValueError: If value cannot be converted or is out of bounds.
    """
    if expected_type not in (int, float):
        raise TypeError("'expected_type' must be integer or float.")

    try:
        number = expected_type(value)
    except ValueError as error:
        raise ValueError(
            f"'{field_name}' must be a valid number."
        ) from error

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
    """Validate that a value is an instance of the expected class.

    Args:
        value: Object to validate.
        field_name: Field name used in error messages.
        expected_class: Required class.

    Returns:
        The validated object.

    Raises:
        TypeError: If value is not an instance of expected_class.
    """

    if not isinstance(value, expected_class):
        raise TypeError(
            f"'{field_name}' must be a '{expected_class.__name__}' object."
        )

    return value
