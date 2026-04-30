from src.models.player import Player
from src.repository.player_repository import save_players


class PlayerController:
    def __init__(self, players: list[Player]):
        self.players = players

    def create_player(self, player_data: dict) -> Player:
        """"""
        try:
            player = Player(**player_data)
        except (TypeError, ValueError) as error:
            raise ValueError(f"Invalid player data: {error}") from error

        for existing_player in self.players:
            if existing_player.chess_national_id == player.chess_national_id:
                raise ValueError(
                    f"A player with chess national ID "
                    f"{player.chess_national_id} already exists. "
                    f"His name is {existing_player.first_name} "
                    f"{existing_player.last_name}."
                )

        self.players.append(player)
        save_players(self.players)
        return player

    def list_players(self):
        pass

    def save(self):
        pass
