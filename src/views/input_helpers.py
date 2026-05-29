"""Input validation helpers for console views."""

from enum import Enum
from typing import Callable, TypeVar

from rich.console import Console

from src.views.base_view import BaseView

T = TypeVar("T")


class OptionalOrNot(Enum):
    """Represent whether a prompt allows empty input."""

    OPTIONAL = "yes"
    NOT_OPTIONAL = "no"


def prompt_until_valid(
    optional_or_not: OptionalOrNot,
    prompt_message: str,
    validator: Callable[..., T],
    *args,
    console: Console
) -> T | None:
    """Prompt until the user enters a valid value.

    Empty input returns None only when the prompt is optional. Validation
    errors are displayed and the prompt is repeated.

    Args:
        optional_or_not: Whether empty input is accepted.
        prompt_message: Message displayed to the user.
        validator: Callable used to validate and convert raw input.
        *args: Additional positional arguments passed to the validator.
        console: Rich console used for input and error display.

    Returns:
        Validated value, or None for accepted optional empty input.

    Raises:
        TypeError: If optional_or_not has an invalid type.
    """
    if not isinstance(optional_or_not, OptionalOrNot):
        raise TypeError("'optional_or_not' must be an OptionalOrNot value.")

    while True:
        raw_value = console.input(prompt_message)

        if optional_or_not == OptionalOrNot.OPTIONAL and raw_value == "":
            return None

        try:
            return validator(raw_value, *args)

        except (TypeError, ValueError) as error:
            console.print(BaseView.error_format(str(error)))


def validate_index_selection(
    raw_selection,
    list_for_selection: list,
    minimum_selection: int = 1,
    maximum_selection: int | None = None,
) -> list[str]:
    """Validate comma-separated indices against a selectable list.

    Returned indices are one-based so they can be reused directly with
    view-level numbered selections.

    Args:
        raw_selection: Raw comma-separated user input.
        list_for_selection: Selectable items used to validate bounds.
        minimum_selection: Minimum number of required selections.
        maximum_selection: Optional maximum number of accepted selections.

    Returns:
        One-based selected indices.

    Raises:
        ValueError: If the input is malformed or outside accepted bounds.
    """
    raw_indices = (
        raw_selection
        .strip()
        .replace(" ", "")
        .split(",")
    )

    selected_indices = []

    for raw_index in raw_indices:
        if not raw_index.isdigit():
            raise ValueError("Enter only numbers separated by commas.")

        index = int(raw_index)

        if index < 1:
            raise ValueError("The number cannot be zero.")

        if index > len(list_for_selection):
            raise ValueError("The number cannot be out of range.")

        selected_indices.append(index)

    if len(selected_indices) < minimum_selection:
        raise ValueError(
            f"A minimum of {minimum_selection} numbers must be selected."
        )

    if len(selected_indices) != len(set(selected_indices)):
        raise ValueError("The same number cannot be selected twice.")

    if (
        maximum_selection is not None
        and len(selected_indices) > maximum_selection
    ):
        raise ValueError(
            f"A maximum of {maximum_selection} numbers must be selected."
        )

    return selected_indices


def validate_yes_or_no_string(
    raw_value: str,
) -> str:
    """Validate a yes/no answer and return it normalized.

    Args:
        raw_value: Raw user input.

    Returns:
        Normalized answer, either ``"y"`` or ``"n"``.

    Raises:
        ValueError: If the answer is neither ``"y"`` nor ``"n"``.
    """
    answer = raw_value.strip().lower()

    if answer not in ("y", "n"):
        raise ValueError(
            "Invalid value. Answer must be 'y' for YES or 'n' for NO"
        )

    return answer
