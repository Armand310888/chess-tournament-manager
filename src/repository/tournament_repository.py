"""Provide repository functions for Tournament persistence and lookup.

This module handles loading and saving Tournament objects to a JSON
file, as well as retrieving tournaments by their ID. It relies on
Tournament serialization methods and resolves Player and Round
relationships during deserialization. Basic validation of inputs
and stored data is also enforced.
"""
import json

from src.utils.validators import Pattern, PatternDescription
from src.models.tournament import Tournament
from src.models.round import Round
from src.models.player import Player
from src import paths


def get_tournament_by_id(
        tournament_id: str,
        tournaments: list[Tournament],
) -> Tournament:
    """Return the tournament matching the given ID.

    Args:
        tournament_id: ID of the tournament to retrieve.
        tournaments: Tournaments to search in.

    Returns:
        The tournament matching the given ID.

    Raises:
        TypeError: If tournament_id is not a string or tournaments
            is not a list.
        ValueError: If tournament_id is invalid or unknown.
    """
    if not isinstance(tournament_id, str):
        raise TypeError("'tournament_id' must be a string.")

    if not Pattern.ID.value.fullmatch(tournament_id):
        raise ValueError(
            "'tournament_id' must be a string respecting following pattern:\n"
            f"{PatternDescription.ID.value}"
        )

    if not isinstance(tournaments, list):
        raise TypeError("'tournaments' must be a list.")

    for tournament in tournaments:
        if tournament.id == tournament_id:
            return tournament

    raise ValueError(f"Unknown tournament ID: {tournament_id}")


def load_tournaments(
        players: list[Player],
        rounds: list[Round]
) -> list[Tournament]:
    """Load tournaments from the JSON storage file.

    Player and round IDs stored in JSON are resolved into
    Player and Round instances via Tournament.from_dict.

    Args:
        players: Existing players used for reconstruction.
        rounds: Existing rounds used for reconstruction.

    Returns:
        A list of loaded tournaments, or an empty list if no file
        exists.

    Raises:
        ValueError: If the JSON file is invalid or malformed.
    """
    paths.DATA_DIR.mkdir(parents=True, exist_ok=True)

    if not paths.TOURNAMENTS_FILE.exists():
        return []

    try:
        with open(paths.TOURNAMENTS_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
    except json.JSONDecodeError as error:
        raise ValueError(
            f"Invalid JSON data in {paths.TOURNAMENTS_FILE}."
        ) from error

    if not isinstance(data, list):
        raise ValueError(
            f"Expected a list of tournaments in {paths.TOURNAMENTS_FILE}."
        )

    tournaments = []

    for tournament_data in data:
        tournament = Tournament.from_dict(tournament_data, players, rounds)
        tournaments.append(tournament)

    return tournaments


def save_tournaments(tournaments: list[Tournament]) -> None:
    """Save tournaments to the JSON storage file.

    Tournament objects are converted to JSON-serializable
    dictionaries before being written to disk.

    Args:
        tournaments: Tournaments to persist.

    Raises:
        TypeError: If tournaments is not a list or contains
            non-Tournament items.
    """
    if not isinstance(tournaments, list):
        raise TypeError("'tournaments' must be a list.")

    for tournament in tournaments:
        if not isinstance(tournament, Tournament):
            raise TypeError(
                "'tournaments' must contain only Tournament instances."
            )
    paths.DATA_DIR.mkdir(parents=True, exist_ok=True)

    tournaments_data = []

    for tournament in tournaments:
        tournament_data = tournament.to_dict()
        tournaments_data.append(tournament_data)

    with open(paths.TOURNAMENTS_FILE, "w", encoding="utf-8") as file:
        json.dump(tournaments_data, file, indent=4)
