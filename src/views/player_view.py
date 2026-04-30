from src.views.input_helpers import prompt_until_valid

from src.utils.validators import (
    validate_regex_match,
    validate_non_empty_string,
    validate_number,
    validate_date_or_datetime,
    ELO_MAXIMUM,
    ELO_MINIMUM,
    Pattern,
    PatternDescription,
)
from src.models.player import Player


class PlayerView:
    def prompt_for_player_data(self):
        first_name = prompt_until_valid(
            "Enter player's first name: ",
            validate_non_empty_string,
            "first_name",
        )

        last_name = prompt_until_valid(
            "Enter player's last name: ",
            validate_non_empty_string,
            "last_name"
        )

        birth_date = prompt_until_valid(
            "Enter player's birth date: ",
            validate_date_or_datetime,
            "birth_date",
        )

        elo_rating = prompt_until_valid(
            "Enter player's ELO rank: ",
            validate_number,
            "elo_rating",
            int,
            ELO_MINIMUM,
            ELO_MAXIMUM,
        )

        while True:
            raw_chess_national_id = input(
                "Enter player chess national ID: "
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
                print(error)

        player_data = {
            "first_name": first_name,
            "last_name": last_name,
            "birth_date": birth_date,
            "elo_rating": elo_rating,
            "chess_national_id": chess_national_id
        }

        return player_data

    def display_created_player(self, player: Player) -> None:
        print(
            "\nNew player created with success\n"
            f"{player}\n"
            f"Birth date    : {player.birth_date}\n"
            f"Chess n. ID   : {player.chess_national_id}\n"
        )
