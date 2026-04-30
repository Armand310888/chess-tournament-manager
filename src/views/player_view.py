import re

from src.utils.validators import (
    validate_regex_match,
    CHESS_NATIONAL_ID_PATTERN,
    CHESS_NATIONAL_ID_PATTERN_DESCRIPTION
)
from src.models.player import Player


# prévoir la validation des inputs à l'aide de mes validators
class PlayerView:
    def prompt_for_player(self):
        first_name = input(
            "Entrez le prénom du joueur: "
            )
        last_name = input(
            "Entrez le nom de famille du joueur: "
            )
        birth_date = input(
            "Entrez la date de naissance du joueur: "
            )
        elo_rating = input(
            "Entrez le classement ELO du joueur: "
            )
        while True:
            raw_chess_national_id = input(
                "Enter player chess national ID: "
            )

            try:
                chess_national_id = validate_regex_match(
                    raw_chess_national_id,
                    "chess_national_id",
                    CHESS_NATIONAL_ID_PATTERN,
                    CHESS_NATIONAL_ID_PATTERN_DESCRIPTION
                )
                break
            except ValueError as error:
                print(error)

        return {
            "first_name": first_name,
            "last_name": last_name,
            "birth_date": birth_date,
            "elo_rating": elo_rating,
            "chess_national_id": chess_national_id
        }
