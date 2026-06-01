"""Tournament console view."""

from rich.panel import Panel
from rich.table import Table
from datetime import date

from src.utils.validators import (
    validate_non_empty_string,
    validate_date_order,
    validate_regex_match,
    validate_datetime,
    validate_number,
    Pattern,
    PatternDescription,
)
from src.models.tournament import Address
from src.models.tournament import Tournament
from src.views.input_helpers import (
    prompt_until_valid,
    validate_index_selection,
    validate_yes_or_no_string,
    OptionalOrNot,
)
from src.views.player_view import PlayerView
from src.views.base_view import BaseView
from src.services.ranking_manager import get_players_ranked
from src.services.event_status_manager import EventStatus


class TournamentView(BaseView):
    """Collect and display tournament-related console data."""

    def __init__(self):
        """Initialize the tournament view and nested player view."""
        super().__init__()
        self.player_view = PlayerView()

    def prompt_for_tournament_data(
        self
    ) -> dict[str, str | int | date | object]:
        """Prompt for validated tournament data.

        Returns:
            Dictionary of validated values required to create a tournament.
        """
        self.console.print()

        name = prompt_until_valid(
            OptionalOrNot.NOT_OPTIONAL,
            self.prompt_format("Enter the tournament name: "),
            validate_non_empty_string,
            "name",
            console=self.console,
        )

        street_number = prompt_until_valid(
            OptionalOrNot.NOT_OPTIONAL,
            self.prompt_format("Enter the tournament street number: "),
            validate_regex_match,
            "street_number",
            Pattern.STREET_NUMBER,
            PatternDescription.STREET_NUMBER,
            console=self.console,
        )

        street_name = prompt_until_valid(
            OptionalOrNot.NOT_OPTIONAL,
            self.prompt_format("Enter the tournament street name: "),
            validate_non_empty_string,
            "street_name",
            console=self.console,
        )

        postal_code = prompt_until_valid(
            OptionalOrNot.NOT_OPTIONAL,
            self.prompt_format("Enter the tournament postal code: "),
            validate_regex_match,
            "postal_code",
            Pattern.POSTAL_CODE,
            PatternDescription.POSTAL_CODE,
            console=self.console,
        )

        city = prompt_until_valid(
            OptionalOrNot.NOT_OPTIONAL,
            self.prompt_format("Enter the tournament city name: "),
            validate_non_empty_string,
            "city",
            console=self.console,
        )

        address = Address(street_number, street_name, postal_code, city)

        start_datetime = prompt_until_valid(
            OptionalOrNot.NOT_OPTIONAL,
            self.prompt_format(
                "Enter the tournament starting date "
                "and time (YYYY-MM-DD HH:MM): "
            ),
            validate_datetime,
            "start_datetime",
            console=self.console,
            )

        while True:
            end_datetime = prompt_until_valid(
                OptionalOrNot.NOT_OPTIONAL,
                self.prompt_format(
                    "Enter the tournament end date and time "
                    "(YYYY-MM-DD HH:MM): "
                ),
                validate_datetime,
                "end_datetime",
                console=self.console,
            )

            try:
                validate_date_order(start_datetime, end_datetime)
                break
            except ValueError as error:
                self.display_error(error)

        min_number_of_players = None
        max_number_of_players = None
        exact_number_of_players = None

        use_exact_number = prompt_until_valid(
            OptionalOrNot.NOT_OPTIONAL,
            self.prompt_format(
                "Do you want to define an exact number of players? "
                "Enter 'y' for YES or 'n' for NO: "
            ),
            validate_yes_or_no_string,
            console=self.console,
        )

        if use_exact_number == "y":
            exact_number_of_players = prompt_until_valid(
                OptionalOrNot.NOT_OPTIONAL,
                self.prompt_format("Enter the exact number of players: "),
                validate_number,
                "exact_number_of_players",
                int,
                2,
                console=self.console,
            )

        else:
            use_min_number = prompt_until_valid(
                OptionalOrNot.NOT_OPTIONAL,
                self.prompt_format(
                    "Do you want to define a minimum number of players? "
                    "Enter 'y' for YES or 'n' for NO: "
                ),
                validate_yes_or_no_string,
                console=self.console,
            )

            if use_min_number == "y":
                min_number_of_players = prompt_until_valid(
                    OptionalOrNot.NOT_OPTIONAL,
                    self.prompt_format(
                        "Enter the minimum number of players: "
                    ),
                    validate_number,
                    "min_number_of_players",
                    int,
                    2,
                    console=self.console,
                )

            use_max_number = prompt_until_valid(
                OptionalOrNot.NOT_OPTIONAL,
                self.prompt_format(
                    "Do you want to define a maximum number of players? "
                    "Enter 'y' for YES or 'n' for NO: "
                ),
                validate_yes_or_no_string,
                console=self.console,
            )

            if use_max_number == "y":
                max_number_of_players = prompt_until_valid(
                    OptionalOrNot.NOT_OPTIONAL,
                    self.prompt_format(
                        "Enter the maximum number of players: "
                    ),
                    validate_number,
                    "max_number_of_players",
                    int,
                    2,
                    console=self.console,
                )

        while True:
            number_of_rounds_input = self.console.input(
                self.prompt_format(
                    "Enter the tournament number of rounds\n"
                    "(or press 'Enter' to set it by default (4 rounds)) : "
                )
            )

            if number_of_rounds_input == "":
                number_of_rounds = 4
                break

            try:
                number_of_rounds = validate_number(
                    number_of_rounds_input,
                    "number_of_rounds",
                    int,
                    1
                )
                break

            except ValueError as error:
                self.display_error(error)

        description = prompt_until_valid(
            OptionalOrNot.OPTIONAL,
            self.prompt_format(
                "Enter the tournament description "
                "(or press 'Enter' to skip) : "
            ),
            validate_non_empty_string,
            "description",
            100,
            console=self.console,
        )

        return {
            "name": name,
            "address": address,
            "start_datetime": start_datetime,
            "end_datetime": end_datetime,
            "min_number_of_players": min_number_of_players,
            "max_number_of_players": max_number_of_players,
            "exact_number_of_players": exact_number_of_players,
            "number_of_rounds": number_of_rounds,
            "description": description
        }

    def display_created_tournament(self, tournament: Tournament) -> None:
        """Display a confirmation panel for a newly created tournament."""
        content = (
            "\n"
            + self.content_format(
                "Tournament name",
                tournament.name.upper(),
            )
            + self.content_format(
                "Place",
                tournament.address.city,
            )
            + self.content_format(
                "Start date and time",
                tournament.start_datetime,
            )
        )

        self.console.print()

        self.console.print(
            Panel(
                content,
                title=self.results_title_format(
                    "[bold yellow]- New Tournament created "
                    "successfully -[/bold yellow]"
                ),
                border_style="yellow",
                width=self.APP_WIDTH,
            )
        )

    def display_tournaments(self, tournaments: list[Tournament]) -> None:
        """Display existing tournaments in a numbered table."""
        if not tournaments:
            self.console.print("No tournament has been created yet.")
            return

        table = Table(
            title=self.results_title_format("Existing Tournaments"),
            width=self.APP_WIDTH,
            show_lines=True,
        )

        table.add_column("Index", style="bold")
        table.add_column("Name", style="bold")
        table.add_column("Place", style="bold")
        table.add_column("Start date", style="bold")
        table.add_column("End date", style="bold")

        for index, tournament in enumerate(tournaments, start=1):
            table.add_row(
                str(index),
                tournament.name.upper(),
                tournament.address.city,
                str(tournament.start_datetime.strftime("%Y-%m")),
                str(tournament.end_datetime.strftime("%Y-%m")),
            )

        self.console.print(table)

    def prompt_to_select_tournament_index(
        self,
        tournaments: list[Tournament]
    ) -> list[int]:
        """Prompt for one tournament index and return it."""
        raw_selected_tournament_index = prompt_until_valid(
            OptionalOrNot.NOT_OPTIONAL,
            self.prompt_format(
                "Select tournament by entering its number (ex: 3): "
            ),
            validate_index_selection,
            tournaments,
            1,
            1,
            console=self.console,
        )

        selected_index = raw_selected_tournament_index[0]

        return selected_index

    def display_tournament_players_and_ranks(
        self,
        selected_tournament: Tournament
    ):
        """Display tournament players ordered by descending score.

        Args:
            selected_tournament: Tournament whose player scores are displayed.

        Raises:
            TypeError: If selected_tournament is not a Tournament.
        """
        if not isinstance(selected_tournament, Tournament):
            raise TypeError(
                "'selected_tournament' must be a Tournament object."
            )
        ranked_players = get_players_ranked(selected_tournament)

        table = Table(
            title=self.results_title_format(
                f"'{selected_tournament.name}' tournament players and scores"
            ),
            width=self.APP_WIDTH,
            show_lines=True,
        )

        table.add_column("Last name", style="bold")
        table.add_column("First name", style="bold")
        table.add_column("Total score", style="bold")

        for player, total_score in ranked_players:
            table.add_row(
                player.last_name.upper(),
                player.first_name,
                f"{total_score:g}",
            )

        self.console.print()
        self.console.print(table)

    def display_tournament_details(
        self,
        selected_tournament: Tournament
    ) -> str:
        """Display detailed information about a tournament.

        Args:
            selected_tournament: Tournament to display.
        """
        self.console.print()

        table = Table(
            title=None,
            width=self.APP_WIDTH,
            show_lines=True,
            show_header=False,
        )

        table.add_column(style="bold")
        table.add_column()

        table.add_row(
            "Start date and time",
            str(selected_tournament.start_datetime)
        )

        table.add_row(
            "End date and time",
            str(selected_tournament.end_datetime)
        )

        table.add_row(
            "Address",
            f"{selected_tournament.address.street_number} "
            f"{selected_tournament.address.street_name}, "
            f"{selected_tournament.address.postal_code}, "
            f"{selected_tournament.address.city}."
        )

        if selected_tournament.min_number_of_players is not None:
            table.add_row(
                "Minimum number of players",
                str(selected_tournament.min_number_of_players),
            )

        if selected_tournament.max_number_of_players is not None:
            table.add_row(
                "Maximum number of players",
                str(selected_tournament.max_number_of_players),
            )

        if selected_tournament.exact_number_of_players is not None:
            table.add_row(
                "Exact number of players required",
                str(selected_tournament.exact_number_of_players)
            )

        table.add_row(
            "Current number of players",
            str(len(selected_tournament.players)),
        )

        table.add_row(
            "Number of rounds",
            str(selected_tournament.number_of_rounds),
        )

        table.add_row(
            "Current round",
            str(selected_tournament.current_round),
        )

        table.add_row(
            "Tournament status",
            f"{selected_tournament.status.value}"
        )

        self.console.print(table)

    def display_tournament_rounds_and_matches(
        self,
        selected_tournament: Tournament
    ) -> None:
        """Display tournament rounds and their matches.

        Args:
            selected_tournament: Tournament whose rounds and matches are shown.

        Raises:
            TypeError: If selected_tournament is not a Tournament.
        """
        if not isinstance(selected_tournament, Tournament):
            raise TypeError(
                "'selected_tournament' must be a Tournament object."
            )

        for round in selected_tournament.rounds:
            current_round_text = (
                " -> CURRENT ROUND"
                if round == selected_tournament.current_round
                else ""
            )

            table = Table(
                title=self.results_title_format(
                    f"Round n°{round.number}{current_round_text}"
                ),
                width=self.APP_WIDTH,
                show_lines=True,
            )

            table.add_column("Match ID", style="bold")
            table.add_column("White Player", style="bold")
            table.add_column("Black Player", style="bold")
            table.add_column("Status", style="bold")
            table.add_column("Result", style="bold")
            table.add_column("Score", style="bold")

            for match in round.matches:
                is_finished = (
                    match.status == EventStatus.FINISHED
                )

                result = (
                    match.result.value
                    if is_finished else "-"
                )

                score = (
                    f"{match.white_player.last_name.upper()}: "
                    f"{match.white_player_score:g}\n"
                    f"{match.black_player.last_name.upper()}: "
                    f"{match.black_player_score:g}"
                    if is_finished
                    else "-"
                )

                table.add_row(
                    str(match.id),
                    f"{match.white_player.first_name} "
                    f"{match.white_player.last_name.upper()}",
                    f"{match.black_player.first_name} "
                    f"{match.black_player.last_name.upper()}",
                    match.status.value,
                    result,
                    score,
                )

            self.console.print(table)

    def prompt_to_end_tournament(self, selected_tournament: Tournament) -> str:
        """"""
        return prompt_until_valid(
            OptionalOrNot.NOT_OPTIONAL,
            self.prompt_format(
                f"End '{selected_tournament.name}' tournament? (y/n): "
            ),
            validate_yes_or_no_string,
            console=self.console,
        )

    def display_ended_tournament(self, selected_tournament: Tournament):
        """"""
        self.display_success(
            f"Tournament {selected_tournament.name} "
            "has been ended successfully."
        )

        self.display_section_title("Final scores")
        self.display_tournament_players_and_ranks(selected_tournament)
