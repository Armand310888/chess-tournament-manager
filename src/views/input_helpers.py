""""""
from datetime import datetime

from utils.validators import (
    validate_number,
)


def prompt_until_valid(prompt_message, validator, *args):
    while True:
        raw_value = input(prompt_message)

        try:
            return validator(raw_value, *args)
        except (TypeError, ValueError) as error:
            print(error)


def validate_datetime_string(raw_value: str, field_name: str) -> datetime:
    if not isinstance(raw_value, str):
        raise TypeError(f"'{field_name}' must be a string")

    try:
        parsed_value = datetime.fromisoformat(raw_value.strip())
    except ValueError:
        raise ValueError(
            f"'{field_name}' must be in ISO format "
            f"(YYYY-MM-DD HH:MM)"
        )

    return parsed_value


def validate_int_string(
        raw_value: str,
        field_name: str,
        minimum: int | None = None,
        maximum: int | None = None
) -> int:

    try:
        parsed = int(raw_value)
    except ValueError:
        raise ValueError(f"'{field_name}' must be an integer")

    return validate_number(parsed, field_name, int, minimum, maximum)
