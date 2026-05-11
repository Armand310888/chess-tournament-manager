""""""
from src.repository.player_repository import load_players
from src.repository.match_repository import load_matches
from src.repository.round_repository import load_rounds
from src.repository.tournament_repository import load_tournaments
from src.controllers.player_controller import PlayerController
from src.controllers.tournament_controller import TournamentController
from src.views.player_view import PlayerView
from src.views.tournament_view import TournamentView
from src.views.input_helpers import pause
from src.views.main_view import MainView


class MainController:
    """"""
    def __init__(self):
        self.players = load_players()
        self.matchs = load_matches(self.players)
        self.rounds = load_rounds(self.matchs)
        self.tournaments = load_tournaments(self.players, self.rounds)
        self.player_controller = PlayerController(self.players)
        self.tournament_controller = (
            TournamentController(self.tournaments, self.players)
        )
        self.player_view = PlayerView()
        self.tournament_view = TournamentView()
        self.main_view = MainView()

    def run(self) -> None:
        """"""
        print("Application started")

        while True:
            choice = self.main_view.prompt_main_menu_choice()

            if choice == "1":
                self.create_player_flow()
            elif choice == "2":
                self.list_players_flow()
            elif choice == "3":
                self.create_tournament_flow()
            elif choice == "4":
                self.list_tournaments_flow()
            elif choice == "5":
                self.add_player_flow()
            elif choice == "0":
                break
            else:
                print(
                    "Invalid choice.\n"
                    "Please enter the digit corresponding to your choice"
                )

    def create_player_flow(self) -> None:
        """"""
        player_data = self.player_view.prompt_for_player_data()

        try:
            player = self.player_controller.create_player(player_data)
        except (TypeError, ValueError) as error:
            print(error)
            return

        self.player_view.display_created_player(player)

        pause()

    def get_players_flow(self) -> None:
        """"""
        self.player_view.display_players(self.players)

        pause()

    def create_tournament_flow(self) -> None:
        """"""
        tournament_data = self.tournament_view.prompt_for_tournament_data()

        try:
            tournament = (
                self.tournament_controller.create_tournament(
                    tournament_data
                )
            )

        except (TypeError, ValueError) as error:
            print(error)
            return

        self.tournament_view.display_created_tournament(tournament)

        pause()

    def list_tournaments_flow(self) -> None:
        """"""
        self.tournament_view.display_tournaments(self.players, self.rounds)

        pause()

    def add_player_flow(self) -> None:
        """"""
        selected_tournament_index = (
            self.tournament_view
            .prompt_to_select_tournament(self.tournaments)
        )
        selected_tournament = (
            self.tournament_controller.select_tournament(
                selected_tournament_index,
            )
        )

        selectable_players = (
            self.tournament_controller
            .get_selectable_players(selected_tournament)
        )

        selected_players_indices = (
            self.tournament_view
            .prompt_to_select_players(selectable_players)
        )

        selected_players = (
            self.tournament_controller
            .select_players(
                selected_tournament,
                selectable_players,
                selected_players_indices
            )
        )

        self.player_view.display_players(selected_players)

        pause()
