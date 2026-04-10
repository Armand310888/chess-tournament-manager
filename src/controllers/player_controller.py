
from datetime import date

from models.player import Player


def get_player_by_chess_national_id(
        chess_national_id: str,
        players: list[Player],
        exclude_player: Player | None = None
):
    normalized_id = chess_national_id.strip().upper()

    for player in players:
        if exclude_player is not None and player is exclude_player:
            continue

        if player.chess_national_id == normalized_id:
            return player

    return None

def create_player(
        first_name: str,
        last_name: str,
        birth_date: date,
        elo_rating: int,
        chess_national_id: str,
        players: list[Player]
):
    """Create a new player if the chess national ID is unique."""

    existing_player = get_player_by_chess_national_id(
        chess_national_id, players
    )

    if existing_player is not None:
        raise ValueError(
            f"Chess national ID '{chess_national_id.strip().upper()}' "
            f"is already used by "
            f"{existing_player.first_name} {existing_player.last_name}."
        )

    new_player = Player(
        first_name=first_name,
        last_name=last_name,
        birth_date=birth_date,
        elo_rating=elo_rating,
        chess_national_id=chess_national_id
    )

    players.append(new_player)

    return new_player
