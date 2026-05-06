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
from src.views.input_helpers import (
    prompt_until_valid,
    validate_player_selection
)
from src.views.player_view import PlayerView
from src.repository.tournament_repository import load_tournaments


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

        start_date = prompt_until_valid(
                "Enter the tournament starting date and time: ",
                validate_datetime_string,
                "start_date"
            )

        while True:
            end_date = prompt_until_valid(
                "Enter the tournament end date and time : ",
                validate_datetime_string,
                "end_date"
            )

            try:
                validate_date_order(start_date, end_date)
                break
            except ValueError as error:
                print(error)

        number_of_players = prompt_until_valid(
            "Enter the maximum number of players admitted to the tournament : ",
            validate_int_string,
            "number_of_players",
            1,
        )

        number_of_rounds = prompt_until_valid(
            "Enter the tournament number of rounds (by default: 4) : ",
            validate_int_string,
            "number_of_rounds",
            1
        )

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

    def display_tournaments(self, players: list, rounds: list):
        """"""
        all_tournaments = load_tournaments(players, rounds)

        if not all_tournaments:
            print("No ")

        print("Existing tournaments:")

        for index, tournament in enumerate(all_tournaments, start=1):
            print(
                f"{index}. {tournament.name} - {tournament.address.city} - "
                f"{tournament.start_datetime.strftime("%Y-%m")}"
            )

    def display_created_tournament(self, tournament: Tournament) -> None:
        """"""
        print(
            "\nNew tournament created with success:\n"
            f"{tournament.name} - {tournament.address.city} - "
            f"{tournament.start_datetime.strftime("%Y-%m")}"
        )

    def prompt_to_select_players(self):
        """"""
        self.player_view.display_players()

        selected_players = prompt_until_valid(
            "Select players by entering their numbers separataed by comas "
            "(ex: 1,5,7)",
            validate_player_selection
        )

        return selected_players
