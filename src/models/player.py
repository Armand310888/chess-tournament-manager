from utils.validators import (
    validate_non_empty_string,
    validate_date,
    validate_chess_id,
    validate_number
)

from datetime import date

ELO_MINIMUM = 0
ELO_MAXIMUM = 3000


class Player:
    """Represents a chess player."""
    def __init__(
        self,
        first_name: str,
        last_name: str,
        birth_date: date,
        elo_rating: int,
        chess_national_id: str
    ):
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.elo_rating = elo_rating
        self.chess_national_id = chess_national_id

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        self._first_name = validate_non_empty_string(value, "first_name")

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        self._last_name = validate_non_empty_string(value, "last_name")

    @property
    def birth_date(self):
        return self._birth_date

    @birth_date.setter
    def birth_date(self, value):
        self._birth_date = validate_date(value, "birth_date")

    @property
    def elo_rating(self):
        return self._elo_rating

    @elo_rating.setter
    def elo_rating(self, value):
        self._elo_rating = validate_number(
            value,
            "elo_rating",
            int,
            ELO_MINIMUM,
            ELO_MAXIMUM
            )

    @property
    def chess_national_id(self):
        return self._chess_national_id

    @chess_national_id.setter
    def chess_national_id(self, value):
        self._chess_national_id = validate_chess_id(value)

    def to_dict(self):
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "birth_date": self.birth_date.isoformat(),
            "elo_rating": self.elo_rating,
            "chess_national_id": self.chess_national_id
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            first_name=data["first_name"],
            last_name=data["last_name"],
            birth_date=date.fromisoformat(data["birth_date"]),
            elo_rating=data["elo_rating"],
            chess_national_id=data["chess_national_id"]
        )

    def __str__(self):
        pass

    def __repr__(self):
        pass
