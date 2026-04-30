"""Provide repository functions for Player persistence and lookup.

This module handles loading and saving Player objects to a JSON
file, as well as retrieving players by their chess national ID.
It relies on Player serialization methods and ensures basic
validation of inputs and stored data.
"""
import json

from src.models.player import Player
from src import paths


def get_player_by_id(chess_national_id: str, players: list[Player]) -> Player:
    """Return the player matching the given chess national ID.

    Args:
        chess_national_id: Player ID to look up.
        players: Players to search through.

    Returns:
        The matching Player instance.

    Raises:
        ValueError: If no player matches the given ID.
    """
    if not isinstance(chess_national_id, str):
        raise TypeError("'chess_national_id' must be a string.")

    if not isinstance(players, list):
        raise TypeError("'players' must be a list.")

    for player in players:
        if player.chess_national_id == chess_national_id:
            return player

    raise ValueError(f"Unknown player ID: {chess_national_id}")


def load_players() -> list[Player]:
    """Load all players from the JSON storage file.

    Returns:
        A list of Player instances. Returns an empty list if the
        storage file does not exist.

    Raises:
        ValueError: If the JSON file is invalid or has unexpected
        structure.
    """
    paths.DATA_DIR.mkdir(parents=True, exist_ok=True)

    if not paths.PLAYERS_FILE.exists():
        return []

    try:
        with open(paths.PLAYERS_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
    except json.JSONDecodeError as error:
        raise ValueError(
            f"Invalid JSON data in {paths.PLAYERS_FILE}."
        ) from error

    if not isinstance(data, list):
        raise ValueError(
            f"Expected a list of players in {paths.PLAYERS_FILE}."
        )

    players = []

    for player_data in data:
        player = Player.from_dict(player_data)
        players.append(player)

    return players


def save_players(players: list[Player]) -> None:
    """Save players to the JSON storage file.

    Converts each Player instance to a JSON-serializable dictionary
    before writing the full list to disk.

    Args:
        players: Players to persist.

    Raises:
        TypeError: If players is not a list or contains non-Player
        objects.
    """
    if not isinstance(players, list):
        raise TypeError("'players' must be a list.")

    for player in players:
        if not isinstance(player, Player):
            raise TypeError(
                "'players' must contain only Player instances."
            )

    paths.DATA_DIR.mkdir(parents=True, exist_ok=True)

    players_data = []

    for player in players:
        player_data = player.to_dict()
        players_data.append(player_data)

    with open(paths.PLAYERS_FILE, "w", encoding="utf-8") as file:
        json.dump(players_data, file, indent=4)
