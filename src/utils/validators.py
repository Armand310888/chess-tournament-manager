from datetime import date, datetime
import re
from enum import Enum

STREET_NUMBER_PATTERN = r"^\d+\s?(bis|ter|[A-Za-z])?$"
STREET_NUMBER_PATTERN_DESCRIPTION = (
    "One or more digits, optionally followed by a space "
    "and a suffix such as 'bis' or 'ter', or a single letter. "
    "Examples: 12, 12 bis, 12A"
)

POSTAL_CODE_PATTERN = r"^\d{5}$"
POSTAL_CODE_PATTERN_DESCRIPTION = "five positive digits. Example: 92700"

CHESS_NATIONAL_ID_PATTERN = r"^[A-Z]{2}\d{5}$"
CHESS_NATIONAL_ID_PATTERN_DESCRIPTION = (
    "Two uppercase letters followed by five digits. "
    "Example: AB12345 "
)

ELO_MINIMUM = 0
ELO_MAXIMUM = 3000


class NumberType(Enum):
    INTEGER = int
    FLOAT = float


def validate_non_empty_string(value: str, field_name: str) -> str:
    """"""
    if not isinstance(value, str):
        raise TypeError(f"'{field_name}' must be a string")

    cleaned_value = value.strip()
    if not value.strip():
        raise ValueError(f"'{field_name}' must be a non-empty string")

    return cleaned_value


def validate_regex_match(
        value: str,
        field_name: str,
        regex_pattern: str,
        pattern_description: str
) -> str:
    """"""
    cleaned_value = (
        validate_non_empty_string(value, field_name).upper()
    )

    if not re.fullmatch(regex_pattern, cleaned_value):
        raise ValueError(
            f"'{field_name}' format must be: "
            f"'{pattern_description}"
        )

    return cleaned_value


def validate_date(value: date | datetime, field_name: str) -> date:
    """"""
    if not isinstance(value, date | datetime):
        raise TypeError(
            f"'{field_name}' must be a date or datetime"
        )

    return value


def validate_date_order(
        start_date: date | datetime,
        end_date: date | datetime
) -> None:
    """"""
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

    if isinstance(start_date, date):
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
    """"""
    # Validate field_name
    if not isinstance(field_name, str) or not field_name.strip():
        raise TypeError("'field_name' must be a non-empty string.")

    # Validate expected_type
    if expected_type not in (int, float):
        raise TypeError("'expected_type' must be int or float.")

    # Validate minimum and maximum types
    if minimum is not None:
        if not isinstance(minimum, (int, float)):
            raise TypeError("'minimum' must be an int or a float.")

    if maximum is not None:
        if not isinstance(maximum, (int, float)):
            raise TypeError("'maximum' must be an int or a float.")

    # Validate logical consistency of bounds
    if minimum is not None and maximum is not None and minimum > maximum:
        raise ValueError("'minimum' cannot be greater than 'maximum'.")

    # Validate value type
    if not isinstance(value, expected_type):
        raise TypeError(
            f"'{field_name}' must be of type {expected_type.__name__}."
        )
    # Validate bounds
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
    """"""

    if not isinstance(value, expected_class):
        raise TypeError(
            f"'{field_name}' must be a '{expected_class.__name__}' object"
        )

    return value

def validate_ID():
    pass