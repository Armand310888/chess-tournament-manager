
class MainView:
    def display_main_menu(self) -> str:
        print("\n=== Chess Tournament Manager ===\n")
        print(
            "1. Players Menu\n"
            "2. Tournaments Menu\n"
            "0. Quit\n"
        )

        return input("Enter your choice here: ")

    def display_player_menu(self) -> str:
        """"""
        print("")
        print("\n=== Player Menu ===\n")
        print(
            "1. Add Player\n"
            "2. List Players\n"
            "0. Back\n"
        )

        return input("Enter your choice here: ")

    def display_list_players_menu(self) -> str:
        """"""
        print("--- Choices ---\n")
        print(
            "1. Show Player(s) details\n"
            "0. Back\n"
        )

        return input("Enter your choice here: ")

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
            "1. Select a Tournament"
            "0. Back"
        )

    def display_select_a_tournament_menu(self) -> str:
        """"""
        print("--- Choices ---\n")
        print(
            "1. Add players to the Tournament"
            "2. List Tournament's Players"
            "3. List Tournament's Rounds and Matches"
            "0. Back"
        )

        return input("Enter your choice here: ")

    def invalid_choice_message(self) -> str:
        print(
            "Invalid choice.\n"
            "Please enter the digit corresponding to your choice."
        )
