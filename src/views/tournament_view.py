from utils.validators import (
    validate_non_empty_string,
    validate_date_order,
    validate_regex_match,
    STREET_NUMBER_PATTERN,
    STREET_NUMBER_PATTERN_DESCRIPTION,
    POSTAL_CODE_PATTERN,
    POSTAL_CODE_PATTERN_DESCRIPTION,
)
from models.tournament import Address
from views.input_helpers import (
    prompt_until_valid,
    validate_datetime_string,
    validate_int_string,
    validate_player_selection
)
from utils.storage import load_all_players


class TournamentView:
    def prompt_for_tournament(self):
        name = prompt_until_valid(
            "Enter the tournament name: ",
            validate_non_empty_string,
            "first_name"
        )

        street_number = prompt_until_valid(
            "Enter the tournament street number: ",
            validate_regex_match,
            "street_number",
            STREET_NUMBER_PATTERN,
            STREET_NUMBER_PATTERN_DESCRIPTION
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
            POSTAL_CODE_PATTERN,
            POSTAL_CODE_PATTERN_DESCRIPTION
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

        place = Address(street_number, street_name, postal_code, city)

        return {
            "name": name,
            "place": place,
            "start_date": start_date,
            "end_date": end_date,
            "number_of_players": number_of_players,
            "number_of_rounds": number_of_rounds,
            "description": description
        }
