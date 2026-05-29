"""Main application controller and high-level menu flows."""

from src.controllers.match_controller import MatchController
from src.controllers.player_controller import PlayerController
from src.controllers.round_controller import RoundController
from src.controllers.tournament_controller import TournamentController
from src.models.match import MatchResult
from src.models.tournament import Tournament
from src.repository.match_repository import load_matches
from src.repository.player_repository import load_players
from src.repository.round_repository import load_rounds
from src.repository.tournament_repository import load_tournaments
from src.utils.exceptions import RoundNotFinishedError
from src.views.main_view import MainView
from src.views.match_view import MatchView
from src.views.player_view import PlayerView
from src.views.round_view import RoundView
from src.views.tournament_view import TournamentView


class MainController:
    """Coordinate application startup, menus, and user flows."""

    def __init__(self) -> None:
        """Load persisted data and initialize controllers and views."""
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
        self.match_controller = MatchController(
            self.matches,
            self.rounds,
            self.tournaments
        )
        self.tournament_controller = (
            TournamentController(self.tournaments, self.players)
        )
        self.player_view = PlayerView()
        self.match_view = MatchView()
        self.round_view = RoundView()
        self.tournament_view = TournamentView()
        self.main_view = MainView()

    def run(self) -> None:
        """Run the main application loop until the user exits."""

        while True:
            choice = self.main_view.display_main_menu()

            if choice == "manage_players":
                self.player_menu_flow()
            elif choice == "manage_tournaments":
                self.tournament_menu_flow()
            elif choice == "exit":
                break

    def player_menu_flow(self) -> None:
        """Run the player management menu loop."""
        while True:
            choice = self.main_view.display_player_menu()

            if choice == "add_player":
                self.create_player_flow()
            elif choice == "list_players":
                self.list_players_menu_flow()
            elif choice == "back":
                break

    def list_players_menu_flow(self) -> None:
        """Run the registered players listing menu loop."""
        while True:
            self.main_view.display_application_header()
            self.player_view.display_players(self.players, "Registered")

            choice = self.main_view.display_list_players_menu()

            if choice == "players_details":
                self.show_selected_players_details_flow()
            elif choice == "back":
                break

    def tournament_menu_flow(self) -> None:
        """Run the tournament management entry menu loop."""
        while True:
            choice = self.main_view.display_tournaments_menu()

            if choice == "create_tournament":
                self.create_tournament_flow()
            elif choice == "manage_tournaments":
                self.manage_tournament_menu_flow()
            elif choice == "back":
                break

    def manage_tournament_menu_flow(self) -> None:
        """Run the tournament selection menu loop."""
        while True:
            self.main_view.display_application_header()
            self.tournament_view.display_tournaments(self.tournaments)

            choice = self.main_view.display_manage_tournament_menu()

            if choice == "select_tournament":
                selected_index = (
                    self.tournament_view
                    .prompt_to_select_tournament_index(
                        self.tournaments
                    )
                )

                selected_tournament = (
                    self.tournament_controller
                    .select_tournament(
                        selected_index
                    )
                )

                self.select_tournament_menu_flow(
                    selected_tournament
                )

            elif choice == "back":
                break

    def select_tournament_menu_flow(
        self,
        selected_tournament: Tournament
    ) -> None:
        """Run the menu loop for a selected tournament."""
        while True:
            self.main_view.display_application_header()

            choice = (
                self.main_view
                .display_select_tournament_menu(
                    selected_tournament
                )
            )

            if choice == "add_players":
                self.add_player_to_tournament_flow(selected_tournament)
            elif choice == "players_and_ranks":
                self.tournament_view.display_tournament_players_and_ranks(
                    selected_tournament
                )
                self.main_view.pause()
            elif choice == "next_round":
                try:
                    self.create_next_round_flow(selected_tournament)
                except ValueError as error:
                    self.round_view.display_error(error)
                    self.main_view.pause()

            elif choice == "rounds_and_matches":
                self.tournament_view.display_tournament_rounds_and_matches(
                    selected_tournament
                )
                self.main_view.pause()
            elif choice == "match_results":
                self.enter_matches_results_flow(selected_tournament)
            elif choice == "back":
                break

    def create_player_flow(self) -> None:
        """"""
        player_data = self.player_view.prompt_for_player_data()

        try:
            player = self.player_controller.create_player(player_data)
        except (TypeError, ValueError) as error:
            self.main_view.display_error(error)
            self.main_view.pause()
            return

        self.player_view.display_created_player(player)

        self.main_view.pause()

    def get_players_flow(self) -> None:
        """"""
        self.player_view.display_players(self.players, "Available")

        self.main_view.pause()

    def show_selected_players_details_flow(self) -> None:
        """"""
        selected_indices = self.player_view.prompt_to_select_players_indices(
            self.players,
        )

        self.player_view.display_players_details(
            self.players,
            selected_indices,
        )

        self.main_view.pause()

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
            self.main_view.display_error(error)
            self.main_view.pause()
            return

        self.tournament_view.display_created_tournament(tournament)

        self.main_view.pause()

    def get_tournaments_flow(self) -> None:
        """"""
        self.tournament_view.display_tournaments(self.tournaments)

        self.main_view.pause()

    def add_player_to_tournament_flow(
        self,
        selected_tournament: Tournament
    ) -> None:
        """Prompt for players and register them in the selected tournament.

        Args:
            selected_tournament: Tournament receiving selected players.
        """
        selectable_players = (
            self.tournament_controller
            .get_selectable_players(selected_tournament)
        )

        if not selectable_players:
            self.main_view.display_error("No selectable players available.")

        self.player_view.display_players(
            selectable_players,
            "Selectable players"
        )

        selected_players_indices = (
            self.player_view
            .prompt_to_select_players_indices(selectable_players)
        )

        selected_players = (
            self.tournament_controller
            .select_players(
                selected_tournament,
                selectable_players,
                selected_players_indices
            )
        )

        self.player_view.display_players(
            selected_players,
            "Added players to the tournament"
        )

        self.main_view.pause()

    def create_next_round_flow(
        self,
        selected_tournament: Tournament
    ) -> None:
        """Prompt for confirmation and create the next tournament round.

        Args:
            selected_tournament: Tournament receiving the next round.
        """
        choice = self.round_view.prompt_for_new_round()

        if choice != "y":
            return None

        try:
            new_round = (
                self.round_controller
                .create_new_round(
                    selected_tournament,
                )
            )
        except RoundNotFinishedError as error:
            self.main_view.display_error(error)
            self.main_view.pause()
            return

        new_round.matches = (
            self.round_controller
            .create_matches_for_round(
                new_round,
                selected_tournament,
            )
        )

        self.round_view.display_created_round(new_round)

        self.main_view.pause()

    def enter_matches_results_flow(
        self,
        selected_tournament: Tournament
    ) -> None:
        """Prompt for unfinished matches and record their results.

        Args:
            selected_tournament: Tournament whose current round is scored.
        """
        if not isinstance(selected_tournament, Tournament):
            raise TypeError(
                "'selected_tournament' must be a Tournament object."
            )

        result_by_choice = {
            "white_player": MatchResult.WHITE_WIN,
            "black_player": MatchResult.BLACK_WIN,
            "draw": MatchResult.DRAW,
        }

        if selected_tournament.current_round is None:
            self.match_view.display_error(
                "No current round available for this tournament."
            )
            self.main_view.pause()
            return

        while True:
            unfinished_matches = (
                self.round_controller
                .get_round_unfinished_matches(
                    selected_tournament.current_round
                )
            )

            if not unfinished_matches:
                self.match_view.display_success(
                    "All match results have been entered."
                )
                break

            self.main_view.clear()

            choice = (
                self.match_view.prompt_to_select_match(
                    unfinished_matches
                )
            )

            if choice == "back":
                break

            match = choice

            self.match_view.display_unfinished_match(match)
            choice = self.match_view.prompt_for_match_result()

            if choice == "back":
                break

            self.match_controller.enter_match_results(
                match,
                result_by_choice[choice],
            )

            self.main_view.clear()
            self.match_view.display_success("Match result saved.")
