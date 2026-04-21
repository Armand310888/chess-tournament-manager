from datetime import date, datetime
import re
from enum import Enum

STREET_NUMBER_PATTERN = r"^\d+\s?(bis|ter|[A-Za-z])?$"
POSTAL_CODE_PATTERN = r"^\d{5}$"
CHESS_NATIONAL_ID_PATTERN = r"^[A-Z]{2}\d{5}$"

class NumberType(Enum):
    INTEGER = int
    FLOAT = float

def validate_non_empty_string(value: str, field_name: str):
    if not isinstance(value, str):
        raise TypeError(f"'{field_name}' must be a string")

    cleaned_value = value.strip()
    if not value.strip():
        raise ValueError(f"'{field_name}' must be a non-empty string")

    return cleaned_value


def validate_street_number():
    pass


def validate_postal_code():
    pass


def validate_date(value: date, field_name: str):
    if not isinstance(value, date):
        raise TypeError(
            f"'{field_name}' must be a date"
        )

    return value


def validate_date_order(start_date: datetime, end_date: datetime)
    if end_date < start_date:
        raise ValueError("End date and time must be later than start date and time.")


def validate_chess_id(value):
    cleaned_value = (
        validate_non_empty_string(value, "chess_national_id").upper()
    )

    if not re.fullmatch(CHESS_NATIONAL_ID_PATTERN, cleaned_value):
        raise ValueError(
            "'chess_national_id' format must be: "
            "two uppercase letters followed by five digits "
            "(example: AB12345)"
            )

    return cleaned_value


def validate_number(
    value: int | float,
    field_name: str,
    expected_type: type,
    minimum: int | float | None = None,
    maximum: int | float | None = None,
):
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