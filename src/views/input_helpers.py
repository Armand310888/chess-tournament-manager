""""""


def prompt_until_valid(prompt_message, validator, *args):
    while True:
        raw_value = input(prompt_message)

        try:
            return validator(raw_value, *args)
        except (TypeError, ValueError) as error:
            print(error)


def validate_index_selection(
        raw_selection,
        list_for_selection: list,
        minimum_selection: int = 1,
        maximum_selection: int | None = None,
) -> list[str]:
    """"""
    raw_indices = (
        raw_selection
        .strip()
        .replace(" ", "")
        .split(",")
    )

    selected_indices = []

    for raw_index in raw_indices:
        if not raw_index.isdigit():
            raise ValueError("Enter only numbers separated by comas.")

        index = int(raw_index)

        if index < 1:
            raise ValueError("The number cannot be zero")
        if index > len(list_for_selection):
            raise ValueError("The number cannot be out of range")

        selected_indices.append(index)

        if len(selected_indices) < minimum_selection:
            raise ValueError(
                f"A minimum of {minimum_selection} numbers must be selected."
            )
        if len(selected_indices) > maximum_selection:
            raise ValueError(
                f"A maximum of {maximum_selection} numbers must be selected."
            )

    return selected_indices


def validate_yes_or_no_string(
        raw_value: str,
):
    answer = raw_value.strip().lower()

    try:
        raw_value == "y" or raw_value == "n"
    except ValueError:
        raise ValueError(
            "Invalid value. Answer must be 'y' for YES or 'n' for NO"
        )

    return answer


def pause() -> None:
    input("\nPress Enter to continue...")
