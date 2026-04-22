
import json
from datetime import date
from pathlib import Path

from models.player import Player

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"

PLAYERS_FILE = DATA_DIR / "players.json"
TOURNAMENTS_FILE = DATA_DIR / "tournaments.json"


def player_to_dict(player: Player):
    """"""
    if not isinstance(player, Player):
        raise TypeError("'player' must be a Player object.")

    return {
        "first_name": player.first_name,
        "last_name": player.last_name,
        "birth_date": player.birth_date.isoformat(),
        "elo_rating": player.elo_rating,
        "chess_national_id": player.chess_national_id
    }


def player_from_dict(data: dict):
    """"""
    if not isinstance(data, dict):
        raise TypeError("'data' must be a dictionary.")

    try:
        return Player(
            first_name=data["first_name"],
            last_name=data["last_name"],
            birth_date=date.fromisoformat(data["birth_date"]),
            elo_rating=data["elo_rating"],
            chess_national_id=data["chess_national_id"]
        )
    except KeyError as missing_field:
        raise ValueError(f"Missing field: {missing_field}")


def load_all_players() -> list[Player]:
    if not DATA_DIR.exists():
        DATA_DIR.mkdir()

    if not PLAYERS_FILE.exists():
        return []

    with open(PLAYERS_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    all_players = []

    for player_data in data:
        player = player_from_dict(player_data)
        all_players.append(player)

    return all_players
# quid gestion erreur?

def save_all_players(all_players: list[Player]):
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    all_players_data = []

    for player in all_players:
        player_data = player_to_dict(player)
        all_players_data.append(player_data)

    with open(PLAYERS_FILE, "w", encoding="utf-8") as file:
        json.dump(all_players_data, file, indent=4)
# quid gestion erreur?