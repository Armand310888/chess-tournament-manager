""""""
from datetime import datetime

from src.utils.validators import (
    validate_number,
)
from src.repository.player_repository import load_players


def prompt_until_valid(prompt_message, validator, *args):
    while True:
        raw_value = input(prompt_message)

        try:
            return validator(raw_value, *args)
        except (TypeError, ValueError) as error:
            print(error)


# qu'avais-je voulu faire ici. Est-ce bien la place de cette fonction?
def validate_player_selection(raw_player_selection):
    all_players = load_all_players()

    raw_player_selection = raw_player_selection.strip().replace(" ", "")

    raw_indices = raw_player_selection.split(",")

    selected_players = []

    for raw_index in raw_indices:
        raw_index = raw_index.strip()

        if not raw_index.isdigit():
            raise ValueError("Enter only numbers separated by comas.")

        index = int(raw_index)

        if index < 1 or index > len(all_players):
            raise ValueError(f"Invalid player number: {index}")

        selected_players.append(all_players[index - 1])

    return selected_players


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
