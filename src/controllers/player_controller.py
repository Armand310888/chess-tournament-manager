
from datetime import date

from models.player import Player
from views.player_view import PlayerView


class PlayerController:
    def __init__(self):
        self.player_view = PlayerView()

    def create_player(self):
        player_data = self.player_view.prompt_for_player()
        submitted_chess_national_id = (
            player_data["chess_national_id"].strip().upper()
        )

        registered_players = load_players()

        for player in registered_players:
            if player.chess_national_id == submitted_chess_national_id:
                raise ValueError(
                    f"A player with chess national ID "
                    f"{player.chess_national_id} already exists. "
                    f"His name is {player.first_name} {player.last_name}")

        new_player = Player(**player_data)

        save_player(new_player)

        return new_player

