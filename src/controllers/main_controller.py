from src.repository.player_repository import load_players
from src.controllers.player_controller import PlayerController
from src.views.player_view import PlayerView


class MainController:
    """"""
    def __init__(self):
        self.players = load_players()
        self.player_controller = PlayerController(self.players)
        self.player_view = PlayerView()

    def run(self) -> None:
        print("Application started")

        while True:
            print("\n0. Quit")
            print("1. Create a player\n")

            choice = input("Choice: ")

            if choice == "1":
                self.create_player_flow()
            elif choice == "0":
                break
            else:
                print(
                    "Invalid choice.\n"
                    "Please enter the digit corresponding to your choice"
                )

    def create_player_flow(self) -> None:
        player_data = self.player_view.prompt_for_player_data()

        try:
            player = self.player_controller.create_player(player_data)
        except (TypeError, ValueError) as error:
            print(error)
            return

        self.player_view.display_created_player(player)
