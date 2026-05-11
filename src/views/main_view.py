
class MainView:
    def prompt_main_menu_choice(self) -> str:
        print("\n--- Main Menu --- ")
        print(
            "\n0. Quit\n"
            "1. Create player\n"
            "2. List players\n"
            "3. Create tournament\n"
            "4. List tournaments\n"
            "5. Add players to tournament\n"
            "6. Start next round\n"
            "7. Enter match results\n"
            "8. Save and quit\n"
        )

        return input("Choice: ")
