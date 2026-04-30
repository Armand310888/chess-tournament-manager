"""Provide repository functions for Round persistence and lookup.

This module handles loading and saving Round objects to a JSON
file, as well as retrieving rounds by their ID. It relies on
Round serialization methods and resolves Match relationships
during deserialization. Basic validation of inputs and stored
data is also enforced.
"""
import json

from src import paths
from utils.validators import Pattern, PatternDescription
from models.round import Round
from models.match import Match


def get_round_by_id(round_id: str, rounds: list[Round]) -> Round:
    """Return the round matching the given ID.

    Args:
        round_id: ID of the round to retrieve.
        rounds: Rounds to search in.

    Returns:
        The round matching the given ID.

    Raises:
        TypeError: If round_id is not a string or rounds is not a list.
        ValueError: If round_id is invalid or unknown.
    """
    if not isinstance(round_id, str):
        raise TypeError("'round_id' must be a string.")

    if not Pattern.ID.value.fullmatch(round_id):
        raise ValueError(
            "'round_id' must be a string respecting following pattern:\n"
            f"{PatternDescription.ID.value}"
        )

    if not isinstance(rounds, list):
        raise TypeError("'roundes' must be a list.")

    for round in rounds:
        if round.id == round_id:
            return round

    raise ValueError(f"Unknown round ID: {round_id}")


def load_rounds(matches: list[Match]) -> list[Round]:
    """Load rounds from the JSON storage file.

    Match IDs stored in JSON are resolved into Match instances by
    Round.from_dict.

    Args:
        matches: Existing matches used to rebuild round objects.

    Returns:
        A list of loaded rounds, or an empty list if no file exists.

    Raises:
        ValueError: If the JSON file is invalid or has an invalid shape.
    """
    paths.DATA_DIR.mkdir(parents=True, exist_ok=True)

    if not paths.ROUNDS_FILE.exists():
        return []

    try:
        with open(paths.ROUNDS_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
    except json.JSONDecodeError as error:
        raise ValueError(
            f"Invalid JSON data in {paths.ROUNDS_FILE}."
        ) from error

    if not isinstance(data, list):
        raise ValueError(
            f"Expected a list of rounds in {paths.ROUNDS_FILE}."
        )

    rounds = []

    for round_data in data:
        round = Round.from_dict(round_data, matches)
        rounds.append(round)

    return rounds


def save_rounds(rounds: list[Round]) -> None:
    """Save rounds to the JSON storage file.

    Round objects are converted to JSON-serializable dictionaries
    before being written to disk.

    Args:
        rounds: Rounds to persist.

    Raises:
        TypeError: If rounds is not a list or contains non-Round items.
    """
    if not isinstance(rounds, list):
        raise TypeError("'roundes' must be a list.")

    for round in rounds:
        if not isinstance(round, Round):
            raise TypeError(
                "'rounds' must contain only Round instances."
            )
    paths.DATA_DIR.mkdir(parents=True, exist_ok=True)

    rounds_data = []

    for round in rounds:
        round_data = round.to_dict()
        rounds_data.append(round_data)

    with open(paths.ROUNDS_FILE, "w", encoding="utf-8") as file:
        json.dump(rounds_data, file, indent=4)
