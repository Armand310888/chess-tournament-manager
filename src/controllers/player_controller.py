

from models.player import Player
from views.player_view import PlayerView
from utils.storage import load_all_players, save_all_players


class PlayerController:
    def __init__(self):
        self.player_view = PlayerView()

    def create_player(self) -> Player:
        player_data = self.player_view.prompt_for_player()

        all_players = load_all_players()

        for player in all_players:
            if player.chess_national_id == player_data["chess_national_id"]:
                raise ValueError(
                    f"A player with chess national ID "
                    f"{player.chess_national_id} already exists. "
                    f"His name is {player.first_name} {player.last_name}"
                )

        player = Player(**player_data)

        all_players.append(player)

        save_all_players(all_players)

        return player

    def modify_player(self):
        pass

    def delete_player(self):
        pass
