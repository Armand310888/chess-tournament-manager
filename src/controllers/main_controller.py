""""""
from src.repository.player_repository import load_players
from src.repository.match_repository import load_matches
from src.repository.round_repository import load_rounds
from src.repository.tournament_repository import load_tournaments
from src.controllers.player_controller import PlayerController
from src.controllers.round_controller import RoundController
from src.controllers.tournament_controller import TournamentController
from src.views.player_view import PlayerView
from src.views.round_view import RoundView
from src.views.tournament_view import TournamentView
from src.views.input_helpers import pause
from src.views.main_view import MainView


class MainController:
    """"""
    def __init__(self):
        self.players = load_players()
        self.matches = load_matches(self.players)
        self.rounds = load_rounds(self.matches)
        self.tournaments = load_tournaments(self.players, self.rounds)
        self.player_controller = PlayerController(self.players)
        self.round_controller = RoundController(
            self.matches,
            self.rounds,
            self.tournaments
        )
        self.tournament_controller = (
            TournamentController(self.tournaments, self.players)
        )
        self.player_view = PlayerView()
        self.round_view = RoundView()
        self.tournament_view = TournamentView()
        self.main_view = MainView()

    def run(self) -> None:
        """"""
        print("Application started")

        while True:
            choice = self.main_view.display_main_menu()

            if choice == "1":
                self.player_menu_flow()
            elif choice == "2":
                self.tournament_menu_flow()
            elif choice == "0":
                break

    def player_menu_flow(self) -> None:
        """"""
        while True:
            choice = self.main_view.display_player_menu()

            if choice == "1":
                self.create_player_flow()
            elif choice == "2":
                self.list_players_menu_flow()
            elif choice == "0":
                break
            else:
                self.main_view.invalid_choice_message()

    def list_players_menu_flow(self) -> None:
        """"""
        while True:
            self.player_view.display_players(self.players, "Registered")

            choice = self.main_view.display_list_players_menu()

            if choice == "1":
                self.show_selected_players_details_flow()
            elif choice == "0":
                break
            else:
                self.main_view.invalid_choice_message()

    def tournament_menu_flow(self) -> None:
        """"""
        while True:
            choice = self.main_view.display_tournaments_menu()

            if choice == "1":
                self.create_tournament_flow()
            elif choice == "2":
                self.get_tournaments_flow()
            elif choice == "3":
                self.run_tournament_flow()
            elif choice == "0":
                break
            else:
                self.main_view.invalid_choice_message()

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
        self.player_view.display_players(self.players, "Available")

        pause()

    def show_selected_players_details_flow(self) -> None:
        """"""
        selected_indices = self.player_view.prompt_to_select_players_indices(
            self.players,
        )

        selected_players = [
            self.players[index - 1]
            for index in selected_indices
        ]

        self.player_view.display_players_details(selected_players)

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

    def get_tournaments_flow(self) -> None:
        """"""
        self.tournament_view.display_tournaments(self.tournaments)

        pause()

    def add_player_to_tournament_flow(self) -> None:
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

        self.player_view.display_players(selected_players, "Selected")

        pause()

    def create_next_round_flow(self) -> None:
        """"""
        choice = self.round_view.prompt_for_new_round()

        if choice != "y":
            return None

        selected_tournament_index = (
            self.tournament_view
            .prompt_to_select_tournament(self.tournaments)
        )
        selected_tournament = (
            self.tournament_controller.select_tournament(
                selected_tournament_index,
            )
        )
        new_round = (
            self.round_controller
            .create_new_round(
                selected_tournament,
            )
        )

        new_round.matches = (
            self.round_controller
            .create_match_for_round(
                new_round,
                selected_tournament
            )
        )

        pause()
