"""Main menu view for the console application."""

import questionary

from src.models.tournament import Tournament
from src.views.base_view import BaseView
from src.views.tournament_view import TournamentView


class MainView(BaseView):
    """Display top-level navigation menus."""

    def __init__(self) -> None:
        """Initialize the main view and nested tournament view."""
        super().__init__()
        self.tournament_view = TournamentView()

    def display_main_menu(self) -> str:
        """Display the main menu and return the selected action."""
        self.display_application_header()
        self.display_section_title("Main Menu")

        return questionary.select(
            "Choose a menu\n",
            choices=[
                questionary.Choice(
                    "Players Menu",
                    value="manage_players",
                ),
                questionary.Choice(
                    "Tournaments Menu",
                    value="manage_tournaments",
                ),
                questionary.Choice(
                    "← Exit",
                    value="exit",
                ),
            ],
            instruction="Use ↑ ↓ and 'Enter' to navigate",
            style=self.QUESTIONARY_STYLE,
            qmark="",
        ).ask()

    def display_player_menu(self) -> str:
        """Display the player menu and return the selected action."""
        self.display_application_header()
        self.display_section_title("Player Menu")

        return questionary.select(
            "Choose an action\n",
            choices=[
                questionary.Choice(
                    "Add Player",
                    value="add_player",
                ),
                questionary.Choice(
                    "List Players",
                    value="list_players",
                ),
                questionary.Choice(
                    "← Back",
                    value="back",
                ),
            ],
            instruction="Use ↑ ↓ and 'Enter' to navigate",
            style=self.QUESTIONARY_STYLE,
            qmark="",
        ).ask()

    def display_list_players_menu(self) -> str:
        """Display player list actions and return the selected action."""
        self.display_section_title("Player Menu")
        return questionary.select(
            "Choose an action\n",
            choices=[
                questionary.Choice(
                    "Show Player(s) details",
                    value="players_details",
                ),
                questionary.Choice(
                    "← Back",
                    value="back",
                )
            ],
            instruction="Use ↑ ↓ and 'Enter' to navigate",
            style=self.QUESTIONARY_STYLE,
            qmark="",
        ).ask()

    def display_tournaments_menu(self) -> str:
        """Display the tournament menu and return the selected action."""
        self.display_application_header()
        self.display_section_title("Tournament Menu")

        return questionary.select(
            "Choose an action\n",
            choices=[
                questionary.Choice(
                    "Create Tournament",
                    value="create_tournament",
                ),
                questionary.Choice(
                    "Manage Tournaments",
                    value="manage_tournaments",
                ),
                questionary.Choice(
                    "← Back",
                    value="back",
                )
            ],
            instruction="Use ↑ ↓ and 'Enter' to navigate",
            style=self.QUESTIONARY_STYLE,
            qmark="",
        ).ask()

    def display_manage_tournament_menu(self) -> str:
        """Display tournament actions and return the selected action."""
        self.display_section_title("Tournament Menu")

        return questionary.select(
            "Choose an action\n",
            choices=[
                questionary.Choice(
                    "Select a tournament to manage",
                    value="select_tournament",
                ),
                questionary.Choice(
                    "← Back",
                    value="back",
                )
            ],
            instruction="Use ↑ ↓ and 'Enter' to navigate",
            style=self.QUESTIONARY_STYLE,
            qmark="",
        ).ask()

    def display_select_tournament_menu(
        self,
        selected_tournament: Tournament
    ) -> str:
        """Display actions for the selected tournament.

        Args:
            selected_tournament: Tournament currently being managed.

        Returns:
            Selected menu action.
        """
        self.display_section_title(
            f"Tournament: {selected_tournament.name}"
        )

        self.tournament_view.display_tournament_details(
            selected_tournament
        )

        return questionary.select(
            "Choose an action\n",
            choices=[
                questionary.Choice(
                    "Add Players",
                    value="add_players",
                ),
                questionary.Choice(
                    "List players by rank",
                    value="players_and_ranks",
                ),
                questionary.Choice(
                    "Create next Round",
                    value="next_round",
                ),
                questionary.Choice(
                    "List Rounds and matches",
                    value="rounds_and_matches",
                ),
                questionary.Choice(
                    "Enter current round results",
                    value="match_results",
                ),
                questionary.Choice(
                    "End current round",
                    value="end_round",
                ),
                questionary.Choice(
                    "← Back",
                    value="back",
                )
            ],
            instruction="Use ↑ ↓ and 'Enter' to navigate",
            style=self.QUESTIONARY_STYLE,
            qmark="",
        ).ask()
