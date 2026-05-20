""""""
from src.views.base_view import BaseView

import questionary


class MainView(BaseView):
    """"""
    def display_main_menu(self) -> str:
        """"""
        self.display_application_header()
        self.display_section_title("Main Menu")

        return questionary.select(
            "Choose an action\n",
            choices=[
                questionary.Choice(
                    "Manage Players",
                    value="manage_players"
                ),
                questionary.Choice(
                    "Manage Tournaments",
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

        return input("Enter your choice here: ")

    def invalid_choice_message(self) -> str:
        print(
            "Invalid choice.\n"
            "Please enter the digit corresponding to your choice."
        )
