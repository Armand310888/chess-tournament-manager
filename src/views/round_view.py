""""""
from rich.table import Table

from src.views.base_view import BaseView
from src.views.input_helpers import (
    prompt_until_valid,
    validate_yes_or_no_string,
    OptionalOrNot,
)
from src.models.round import Round
from src.models.match import Match


class RoundView(BaseView):
    """"""
    def prompt_for_new_round(self):
        choice = prompt_until_valid(
            OptionalOrNot.NOT_OPTIONAL,
            self.prompt_format(
                "Create round? (y/n) : "
            ),
            validate_yes_or_no_string,
            console=self.console
        )

        return choice

    def display_created_round(self, new_round: Round) -> None:
        """"""
        content = (
            self.results_title_format("New Round created successfully")
            + self.content_format("Round number", new_round.number)
        )

        self.console.print(content)

    def display_unfinished_matches(
            self,
            unfinished_matches: list[Match],
    ) -> None:
        """"""
        table = Table(
            title=self.results_title_format(
                "Current Round unfinished matches"
            ),
            width=self.APP_WIDTH,
            show_lines=True,
        )

        table.add_column("N°", style="bold")
        table.add_column("White Player", style="bold")
        table.add_column("Black Player", style="bold")

        for index, match in enumerate(unfinished_matches, start=1):
            table.add_row(
                str(index),
                f"{match.white_player.first_name} "
                f"{match.white_player.last_name.upper()}",
                f"{match.black_player.first_name} "
                f"{match.black_player.last_name.upper()}",
            )

        self.console.print(table)
