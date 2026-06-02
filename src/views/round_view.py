"""Round console view."""

from rich.console import Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from src.models.match import Match
from src.models.round import Round
from src.views.base_view import BaseView
from src.utils.input_helpers import (
    OptionalOrNot,
    prompt_until_valid,
    validate_yes_or_no_string,
)


class RoundView(BaseView):
    """Collect and display round-related console data."""

    def prompt_for_new_round(self) -> str:
        """Prompt for confirmation before creating a new round.

        Returns:
            Normalized confirmation answer, either ``"y"`` or ``"n"``.
        """
        choice = prompt_until_valid(
            OptionalOrNot.NOT_OPTIONAL,
            self.prompt_format(
                "Create round? (y/n) : "
            ),
            validate_yes_or_no_string,
            console=self.console,
        )

        return choice

    def display_created_round(self, new_round: Round) -> None:
        """Display a newly created round and its generated matches.

        Args:
            new_round: Round to display.
        """
        matches_table = Table(
            expand=True,
            show_lines=True,
        )

        matches_table.add_column(
            "White player",
            justify="left",
            ratio=1,
        )
        matches_table.add_column(
            "Black player",
            justify="left",
            ratio=1,
        )

        for match in new_round.matches:
            matches_table.add_row(
                (
                    f"{match.white_player.first_name} "
                    f"{match.white_player.last_name}"
                ),
                (
                    f"{match.black_player.first_name} "
                    f"{match.black_player.last_name}"
                )
            )

        round_data = (
            "\n"
            + self.content_format(
                "Round number",
                str(new_round.number),
            )
            + self.content_format(
                "Status",
                new_round.status.value,
            )
            + self.content_format(
                "Number of matches",
                str(len(new_round.matches)),
            )
        )

        matches_title = Text(
            "\nCreated matches for this round:\n",
            style="bold"
        )

        content = Group(
            round_data,
            matches_title,
            matches_table,
        )

        self.console.print(
            Panel(
                content,
                title=self.results_title_format(
                    "New round created successfully"
                ),
                border_style="orange3",
                width=self.APP_WIDTH,
            )
        )

    def display_unfinished_matches(
        self,
        unfinished_matches: list[Match],
    ) -> None:
        """Display unfinished matches for the current round.

        Args:
            unfinished_matches: Matches still waiting for a result.
        """
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

    def prompt_for_end_round(self) -> str:
        """Prompt for confirmation before ending the current round."""
        return prompt_until_valid(
            OptionalOrNot.NOT_OPTIONAL,
            self.prompt_format("End current round? (y/n): "),
            validate_yes_or_no_string,
            console=self.console,
        )
