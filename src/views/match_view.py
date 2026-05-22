""""""
import questionary
from rich.table import Table

from src.models.match import Match
from src.views.base_view import BaseView


class MatchView(BaseView):
    """"""
    def prompt_for_match_result(
            self,
            match: Match
    ):
        """"""
        return questionary.select(
            "Select the match winner\n",
            choices=[
                questionary.Choice(
                    "White Player",
                    value="white_player"
                ),
                questionary.Choice(
                    "Black Player",
                    value="black_player"
                ),
                questionary.Choice(
                    "Draw",
                    value="draw"
                ),
                questionary.Choice(
                    "← Back",
                    value="back"
                )
            ],
            instruction="Use ↑ ↓ and 'Enter' to navigate",
            style=self.QUESTIONARY_STYLE,
            qmark=""
        ).ask()

    def prompt_to_select_match(
            self,
            unfinished_matches: list[Match]
    ) -> Match:
        """"""
        choices = []

        for index, match in enumerate(
            unfinished_matches,
            start=1
        ):
            white_player = (
                f"{match.white_player.first_name} "
                f"{match.white_player.last_name.upper()}"
            )

            black_player = (
                f"{match.black_player.first_name} "
                f"{match.black_player.last_name.upper()}"
            )

            choices.append(
                questionary.Choice(
                    title=(
                        f"{index:<3}"
                        f"{white_player:<35}"
                        "vs"
                        f"{black_player:>35}"
                    ),
                    value=match,
                )
            )

        choices.append(
            questionary.Choice(
                "← Back",
                value="back"
            )
        )

        return questionary.select(
            "Choose a match to enter it's result:\n",
            choices=choices,
            instruction="Use ↑ ↓ and 'Enter' to navigate",
            style=self.QUESTIONARY_STYLE,
            qmark=""
        ).ask()

    def display_unfinished_match(self, match: Match) -> None:
        """"""
        table = Table(
            title=self.results_title_format(
                "Slected match details"
            ),
            width=self.APP_WIDTH,
            show_lines=True,
        )

        table.add_column(
            "White Player",
            style="bold",
            ratio=1
        )
        table.add_column(
            "Black Player",
            style="bold",
            ratio=1
        )

        table.add_row(
            f"{match.white_player.first_name} "
            f"{match.white_player.last_name.upper()}",
            f"{match.black_player.first_name} "
            f"{match.black_player.last_name.upper()}",
        )

        self.console.print()
        self.console.print(table)
