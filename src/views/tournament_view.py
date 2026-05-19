""""""
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
    OptionalOrNot,
)
from src.views.player_view import PlayerView


class TournamentView:
    """"""
    def __init__(self):
        self.player_view = PlayerView()

    def prompt_for_tournament_data(self):
        """"""
        print("")
        name = prompt_until_valid(
            OptionalOrNot.NOT_OPTIONAL,
            "Enter the tournament name: ",
            validate_non_empty_string,
            "first_name"
        )

        street_number = prompt_until_valid(
            OptionalOrNot.NOT_OPTIONAL,
            "Enter the tournament street number: ",
            validate_regex_match,
            "street_number",
            Pattern.STREET_NUMBER,
            PatternDescription.STREET_NUMBER,
        )

        street_name = prompt_until_valid(
            OptionalOrNot.NOT_OPTIONAL,
            "Enter the tournament street name: ",
            validate_non_empty_string,
            "street_name"
        )

        postal_code = prompt_until_valid(
            OptionalOrNot.NOT_OPTIONAL,
            "Enter the tournament postal code: ",
            validate_regex_match,
            "postal_code",
            Pattern.POSTAL_CODE,
            PatternDescription.POSTAL_CODE,
        )

        city = prompt_until_valid(
            OptionalOrNot.NOT_OPTIONAL,
            "Enter the tournament city name: ",
            validate_non_empty_string,
            "city"
        )

        address = Address(street_number, street_name, postal_code, city)

        print("")
        start_datetime = prompt_until_valid(
                OptionalOrNot.NOT_OPTIONAL,
                "Enter the tournament starting date and time "
                "(YYYY-MM-DD HH:MM), or press'Enter' to skip: ",
                validate_datetime,
                "start_date"
            )

        while True:
            print("")
            end_datetime = prompt_until_valid(
                OptionalOrNot.NOT_OPTIONAL,
                "Enter the tournament end date and time "
                "(YYYY-MM-DD HH:MM), or press'Enter' to skip: ",
                validate_datetime,
                "end_date"
            )

            try:
                validate_date_order(start_datetime, end_datetime)
                break
            except ValueError as error:
                print(error)

        print("")
        max_number_of_players = prompt_until_valid(
            OptionalOrNot.OPTIONAL,
            "Enter the maximum number of players "
            "admitted to the tournament (or press 'Enter' to skip): ",
            validate_number,
            "max_number_of_players",
            int,
            1,
        )

        while True:
            print("")
            number_of_rounds_input = input(
                "Enter the tournament number of rounds "
                "(or press 'Enter' to set it by default (4 rounds)) : "
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

        print("")
        description = prompt_until_valid(
            OptionalOrNot.OPTIONAL,
            "Enter the tournament description (or press 'Enter' to skip) : ",
            validate_non_empty_string,
            "description",
            100
        )

        return {
            "name": name,
            "address": address,
            "start_datetime": start_datetime,
            "end_datetime": end_datetime,
            "max_number_of_players": max_number_of_players,
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

        print("\n - Existing tournaments -\n")

        for index, tournament in enumerate(tournaments, start=1):
            print(
                f"{index}. {tournament.name} - {tournament.address.city} - "
                f"{tournament.start_datetime.strftime("%Y-%m")}"
            )
        print("")

    def prompt_to_select_tournament_indices(
            self,
            tournaments: list[Tournament]
    ) -> list[int]:
        """"""
        raw_selected_tournament_index = prompt_until_valid(
            OptionalOrNot.NOT_OPTIONAL,
            "Select tournament by entering it's number (ex: 3): ",
            validate_index_selection,
            tournaments,
            1,
            1,
        )

        selected_tournament_index = raw_selected_tournament_index[0]

        return selected_tournament_index

    def display_tournament_players(self):
        """"""
        pass
