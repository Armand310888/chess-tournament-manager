

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

        all_players = load_players()

        for player in all_players:
            if player.chess_national_id == submitted_chess_national_id:
                raise ValueError(
                    f"A player with chess national ID "
                    f"{player.chess_national_id} already exists. "
                    f"His name is {player.first_name} {player.last_name}")

        player = Player(**player_data)

        save_player(player) # ici?????

        return player

    def modify_player(self):
        pass

    def delete_player(self):
        pass
