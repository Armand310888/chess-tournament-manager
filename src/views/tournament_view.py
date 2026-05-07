""""""
from src.utils.validators import (
    validate_non_empty_string,
    validate_date_order,
    validate_regex_match,
    validate_date_or_datetime,
    validate_number,
    Pattern,
    PatternDescription,
)
from src.models.tournament import Address
from src.models.tournament import Tournament
from src.models.player import Player
from src.views.input_helpers import (
    prompt_until_valid,
    validate_index_selection,
)
from src.views.player_view import PlayerView


class TournamentView:
    """"""
    def __init__(self):
        self.player_view = PlayerView()

    def prompt_for_tournament_data(self):
        """"""
        name = prompt_until_valid(
            "Enter the tournament name: ",
            validate_non_empty_string,
            "first_name"
        )

        street_number = prompt_until_valid(
            "Enter the tournament street number: ",
            validate_regex_match,
            "street_number",
            Pattern.STREET_NUMBER,
            PatternDescription.STREET_NUMBER,
        )

        street_name = prompt_until_valid(
            "Enter the tournament street name: ",
            validate_non_empty_string,
            "street_name"
        )

        postal_code = prompt_until_valid(
            "Enter the tournament postal code: ",
            validate_regex_match,
            "postal_code",
            Pattern.POSTAL_CODE,
            PatternDescription.POSTAL_CODE,
        )

        city = prompt_until_valid(
            "Enter the tournament city name: ",
            validate_non_empty_string,
            "city"
        )

        start_datetime = prompt_until_valid(
                "Enter the tournament starting date and time "
                "(YYYY-MM-DD HH:MM): ",
                validate_date_or_datetime,
                "start_date"
            )

        while True:
            end_datetime = prompt_until_valid(
                "Enter the tournament end date and time "
                "(YYYY-MM-DD HH:MM): ",
                validate_date_or_datetime,
                "end_date"
            )

            try:
                validate_date_order(start_datetime, end_datetime)
                break
            except ValueError as error:
                print(error)

        number_of_players = prompt_until_valid(
            "Enter the maximum number of players "
            "admitted to the tournament : ",
            validate_number,
            "number_of_players",
            int,
            1,
        )

        while True:
            number_of_rounds_input = input(
                "Enter the tournament number of rounds "
                "or Enter to set it by default (4 rounds) : "
            )

            if number_of_rounds_input == "":
                number_of_rounds = 4
            else:
                number_of_rounds = validate_number(
                    number_of_rounds_input,
                    "number_of_rounds",
                    int,
                    1
                )
            break

        description = prompt_until_valid(
            "Enter the tournament description : ",
            validate_non_empty_string,
            "description"
        )

        address = Address(street_number, street_name, postal_code, city)

        return {
            "name": name,
            "address": address,
            "start_datetime": start_datetime,
            "end_datetime": end_datetime,
            "number_of_players": number_of_players,
            "number_of_rounds": number_of_rounds,
            "description": description
        }

    def display_created_tournament(self, tournament: Tournament) -> None:
        """"""
        print(
            "\nNew tournament created with success:\n"
            f"{tournament.name} - {tournament.address.city} - "
            f"{tournament.start_datetime.strftime("%Y-%m")}"
        )

    def display_tournaments(self, tournaments: list[Tournament]) -> None:
        """"""
        if not tournaments:
            print("No tournament have been created yet.")

        print("Existing tournaments:")

        for index, tournament in enumerate(tournaments, start=1):
            print(
                f"{index}. {tournament.name} - {tournament.address.city} - "
                f"{tournament.start_datetime.strftime("%Y-%m")}"
            )

    def prompt_to_select_players(
            self,
            tournament: Tournament,
            players: list[Player]
    ) -> list[int]:
        """"""
        self.player_view.display_selectable_players(tournament, players)

        selected_players_indices = prompt_until_valid(
            "Select players by entering their numbers separated by comas "
            "(ex: 1,5,7): ",
            validate_index_selection,
            players,
            1,
        )

        return selected_players_indices

    def prompt_to_select_tournament(
            self,
            tournaments: list[Tournament]
    ) -> list[int]:
        """"""
        self.display_tournaments(tournaments)

        selected_tournament_index = prompt_until_valid(
            "Select tournament by entering it's number (ex: 3): ",
            validate_index_selection,
            tournaments,
            1,
            1,
        )

        return selected_tournament_index

    def display_players_added_to_tournament(
            self,
            selected_players: list[Player]
    ) -> None:
        """"""

    def display_tournament_players(self):
        """"""
        pass
