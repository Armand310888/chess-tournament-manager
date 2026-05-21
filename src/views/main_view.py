""""""
import questionary

from src.views.base_view import BaseView
from src.views.tournament_view import TournamentView
from src.models.tournament import Tournament


class MainView(BaseView):
    """"""
    def __init__(self) -> None:
        super().__init__()
        self.tournament_view = TournamentView()

    def display_main_menu(self) -> str:
        """"""
        self.display_application_header()
        self.display_section_title("Main Menu")

        return questionary.select(
            "Choose a menu\n",
            choices=[
                questionary.Choice(
                    "Players Menu",
                    value="manage_players"
                ),
                questionary.Choice(
                    "Tournaments Menu",
                    value="manage_tournaments"
                ),
                questionary.Choice(
                    "Exit",
                    value="exit"
                ),
            ],
            instruction="Use ↑ ↓ and 'Enter' to navigate",
            style=self.QUESTIONARY_STYLE,
            qmark=""
        ).ask()

    def display_player_menu(self) -> str:
        """"""
        self.display_application_header()
        self.display_section_title("Player Menu")

        return questionary.select(
            "Choose an action\n",
            choices=[
                questionary.Choice(
                    "Add Player",
                    value="add_player"
                ),
                questionary.Choice(
                    "List Players",
                    value="list_players"
                ),
                questionary.Choice(
                    "Back",
                    value="back"
                ),
            ],
            instruction="Use ↑ ↓ and 'Enter' to navigate",
            style=self.QUESTIONARY_STYLE,
            qmark=""
        ).ask()

    def display_list_players_menu(self) -> str:
        """"""
        self.display_section_title("Player Menu")
        return questionary.select(
            "Choose an action\n",
            choices=[
                questionary.Choice(
                    "Show Player(s) details",
                    value="players_details"
                ),
                questionary.Choice(
                    "Back",
                    value="back"
                )
            ],
            instruction="Use ↑ ↓ and 'Enter' to navigate",
            style=self.QUESTIONARY_STYLE,
            qmark=""
        ).ask()

    def display_tournaments_menu(self) -> str:
        """"""
        print("")
        print("\n=== Tournaments Menu ===\n")
        print(
            "1. Create Tournament\n"
            "2. List Tournaments\n"
            "3. Run Tournaments\n"
            "0. Back\n"
        )

        return input("Enter your choice here: ")

    def display_list_tournaments_menu(self) -> str:
        """"""
        print("--- Choices ---\n")
        print(
            "1. Add players to the Tournament\n"
            "2. List Tournament's Players\n"
            "3. List Tournament's Rounds and Matches\n"
            "0. Back\n"
        )

        return questionary.select(
            "Choose an action\n",
            choices=[
                questionary.Choice(
                    "Select a Tournament",
                    value="select_tournament"
                ),
                questionary.Choice(
                    "Back",
                    value="back"
                )
            ],
            instruction="Use ↑ ↓ and 'Enter' to navigate",
            style=self.QUESTIONARY_STYLE,
            qmark=""
        ).ask()

    def display_select_tournament_menu(
            self,
            selected_tournament: Tournament
    ) -> str:
        """"""
        self.display_section_title(
            f"Tournament: {selected_tournament.name}"
        )

        self.tournament_view.display_tournament_details(
            selected_tournament
        )
