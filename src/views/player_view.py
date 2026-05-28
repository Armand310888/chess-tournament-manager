"""Player console view."""

from rich.panel import Panel
from rich.table import Table

from src.views.input_helpers import prompt_until_valid
from src.views.base_view import BaseView
from src.utils.validators import (
    validate_regex_match,
    validate_number,
    validate_date,
    validate_person_name,
    ELO_MAXIMUM,
    ELO_MINIMUM,
    Pattern,
    PatternDescription,
)
from src.models.player import Player
from src.views.input_helpers import (
    validate_index_selection,
    OptionalOrNot,
)


class PlayerView(BaseView):
    """Collect and display player-related console data."""

    def prompt_for_player_data(self) -> dict[str, str | int | date]:
        """Prompt for player data and return validated field values."""

        first_name = prompt_until_valid(
            OptionalOrNot.NOT_OPTIONAL,
            self.prompt_format("Enter player's first name: "),
            validate_person_name,
            "first_name",
            console=self.console
        )

        last_name = prompt_until_valid(
            OptionalOrNot.NOT_OPTIONAL,
            self.prompt_format("Enter player's last name: "),
            validate_person_name,
            "last_name",
            console=self.console
        )

        birth_date = prompt_until_valid(
            OptionalOrNot.NOT_OPTIONAL,
            self.prompt_format("Enter player's birth date: "),
            validate_date,
            "birth_date",
            console=self.console
        )

        elo_rating = prompt_until_valid(
            OptionalOrNot.NOT_OPTIONAL,
            self.prompt_format("Enter player's ELO rank: "),
            validate_number,
            "elo_rating",
            int,
            ELO_MINIMUM,
            ELO_MAXIMUM,
            console=self.console
        )

        while True:
            raw_chess_national_id = self.console.input(
                self.prompt_format("Enter player chess national ID: ")
            )

            try:
                chess_national_id = validate_regex_match(
                    raw_chess_national_id,
                    "chess_national_id",
                    Pattern.CHESS_NATIONAL_ID,
                    PatternDescription.CHESS_NATIONAL_ID,
                )
                break
            except ValueError as error:
                self.display_error(error)

        player_data = {
            "first_name": first_name,
            "last_name": last_name,
            "birth_date": birth_date,
            "elo_rating": elo_rating,
            "chess_national_id": chess_national_id
        }

        return player_data

    def display_created_player(self, player: Player) -> None:
        """Display a confirmation panel for a newly created player."""

        content = (
            f"\n{player.first_name.upper()} "
            f"[bold]{player.last_name.upper()}[/bold]\n\n"
            + self.content_format(
                "ELO rating",
                player.elo_rating
            )
            + self.content_format(
                "Birth date",
                player.birth_date
            )
            + self.content_format(
                "Chess National ID",
                player.chess_national_id
            )
        )

        self.console.print()

        self.console.print(
            Panel(
                content,
                title=self.results_title_format(
                    "[bold yellow]- New Player created "
                    "successfully -[/bold yellow]"
                ),
                border_style="yellow",
                width=self.APP_WIDTH
            )
        )

    def display_players(
            self,
            players: list[Player],
            type_of_player: str,
    ) -> None:
        """Display players in a numbered table."""

        if not isinstance(players, list):
            raise TypeError("'players' must be a list.")

        for player in players:
            if not isinstance(player, Player):
                raise TypeError("'players' must contain only Player objects.")

        if not isinstance(type_of_player, str):
            raise TypeError("'type_of_player' must be a string.")

        self.console.print("")

        table = Table(
            title=self.results_title_format(type_of_player),
            width=self.APP_WIDTH,
            show_lines=True,
        )

        table.add_column("Index", style="bold")
        table.add_column("Last name", style="bold")
        table.add_column("First name", style="bold")
        table.add_column("ELO rating", style="bold")

        for index, player in enumerate(players, start=1):
            table.add_row(
                str(index),
                player.last_name.upper(),
                player.first_name,
                str(player.elo_rating),
            )

        self.console.print(table)

    def display_players_details(
            self,
            players: list[Player],
            selected_indices: list[int]
    ) -> None:
        """Display detailed cards for selected players."""

        if not isinstance(players, list):
            raise TypeError("'players' must be a list.")

        for player in players:
            if not isinstance(player, Player):
                raise TypeError("'players' must contain only Player objects.")

        self.console.print()

        for index in selected_indices:
            player = players[index-1]

            content = (
                self.content_format(
                    "First name",
                    player.first_name
                )
                + self.content_format(
                    "Last name",
                    player.last_name
                )
                + self.content_format(
                    "Birth date",
                    player.birth_date
                )
                + self.content_format(
                    "ELO rating",
                    player.elo_rating
                )
                + self.content_format(
                    "Chess National ID",
                    player.chess_national_id
                )
            )

            self.console.print(
                Panel(
                    content,
                    title=self.results_title_format(f"- Player {index} -"),
                    border_style="yellow",
                    width=self.APP_WIDTH,
                )
            )

    def prompt_to_select_players_indices(
            self,
            selectable_players: list[Player],
    ) -> list[int]:
        """Prompt for player indices and return validated selections."""

        return prompt_until_valid(
            OptionalOrNot.NOT_OPTIONAL,
            self.prompt_format(
                "Select players by entering their numbers separated by commas "
                "(ex: 1,5,7): "
            ),
            validate_index_selection,
            selectable_players,
            1,
            console=self.console
        )
