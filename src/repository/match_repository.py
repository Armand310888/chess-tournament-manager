"""Provide repository functions for Match persistence and lookup.

This module handles loading and saving Match objects to a JSON
file, as well as retrieving matches by their generated ID. It
relies on Match serialization methods and external Player data
to rebuild player references during loading.
"""
from src import paths
import json

from models.match import Match
from models.player import Player
from utils.validators import Pattern, PatternDescription


def get_match_by_id(match_id: str, matches: list[Match]) -> Match:
    """Return the match matching the given generated ID.

    Args:
        match_id: Match ID to look up.
        matches: Matches to search through.

    Returns:
        The matching Match instance.

    Raises:
        TypeError: If match_id is not a string or matches is not
            a list.
        ValueError: If match_id has an invalid format or no match
            uses the given ID.
    """
    if not isinstance(match_id, str):
        raise TypeError("'match_id' must be a string.")

    if not Pattern.ID.value.fullmatch(match_id):
        raise ValueError(
            "'match_id' must be a string respecting following pattern:\n"
            f"{PatternDescription.ID.value}"
        )

    if not isinstance(matches, list):
        raise TypeError("'matches' must be a list.")

    for match in matches:
        if match.id == match_id:
            return match

    raise ValueError(f"Unknown match ID: {match_id}")


def load_matches(players: list[Player]) -> list[Match]:
    """Load all matches from the JSON storage file.

    Player data is required to resolve stored player IDs back to
    Player objects when rebuilding Match instances.

    Args:
        players: Available players used for ID resolution.

    Returns:
        A list of Match instances. Returns an empty list if the
        storage file does not exist.

    Raises:
        TypeError: If players is not a list.
        ValueError: If the JSON file is invalid or has unexpected
            structure.
    """
    paths.DATA_DIR.mkdir(parents=True, exist_ok=True)

    if not paths.MATCHES_FILE.exists():
        return []

    try:
        with open(paths.MATCHES_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
    except json.JSONDecodeError as error:
        raise ValueError(
            f"Invalid JSON data in {paths.MATCHES_FILE}."
        ) from error

    if not isinstance(data, list):
        raise ValueError(
            f"Expected a list of matches in {paths.MATCHES_FILE}."
        )

    matches = []

    for match_data in data:
        match = Match.from_dict(match_data, players)
        matches.append(match)

    return matches


def save_matches(matches: list[Match]) -> None:
    """Save matches to the JSON storage file.

    Converts each Match instance to a JSON-serializable dictionary
    before writing the full list to disk.

    Args:
        matches: Matches to persist.

    Raises:
        TypeError: If matches is not a list or contains non-Match
            objects.
    """
    if not isinstance(matches, list):
        raise TypeError("'matches' must be a list.")

    for match in matches:
        if not isinstance(match, Match):
            raise TypeError(
                "'matches' must contain only Match instances."
            )
    paths.DATA_DIR.mkdir(parents=True, exist_ok=True)

    matches_data = []

    for match in matches:
        match_data = match.to_dict()
        matches_data.append(match_data)

    with open(paths.MATCHES_FILE, "w", encoding="utf-8") as file:
        json.dump(matches_data, file, indent=4)
