""""""

from utils.validators import (
    validate_non_empty_string,
    validate_date,
    validate_regex_match,
    validate_number,
    CHESS_NATIONAL_ID_PATTERN,
    CHESS_NATIONAL_ID_PATTERN_DESCRIPTION,
    ELO_MAXIMUM,
    ELO_MINIMUM
)

from datetime import date


class Player:
    """"""
    def __init__(
        self,
        first_name: str,
        last_name: str,
        birth_date: date,
        elo_rating: int,
        chess_national_id: str
    ) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.elo_rating = elo_rating
        self.chess_national_id = chess_national_id

    @property
    def first_name(self) -> str:
        """"""
        return self._first_name

    @first_name.setter
    def first_name(self, value) -> None:
        self._first_name = validate_non_empty_string(value, "first_name")

    @property
    def last_name(self) -> str:
        """"""
        return self._last_name

    @last_name.setter
    def last_name(self, value) -> None:
        self._last_name = validate_non_empty_string(value, "last_name")

    @property
    def birth_date(self) -> date:
        """"""
        return self._birth_date

    @birth_date.setter
    def birth_date(self, value) -> None:
        self._birth_date = validate_date(value, "birth_date")

    @property
    def elo_rating(self) -> int:
        """"""
        return self._elo_rating

    @elo_rating.setter
    def elo_rating(self, value) -> None:
        self._elo_rating = validate_number(
            value,
            "elo_rating",
            int,
            ELO_MINIMUM,
            ELO_MAXIMUM
            )

    @property
    def chess_national_id(self) -> str:
        """"""
        return self._chess_national_id

    @chess_national_id.setter
    def chess_national_id(self, value) -> None:
        self._chess_national_id = validate_regex_match(
            value,
            "chess_national_id",
            CHESS_NATIONAL_ID_PATTERN,
            CHESS_NATIONAL_ID_PATTERN_DESCRIPTION
            )

    def __str__(self):
        pass

    def __repr__(self):
        pass
