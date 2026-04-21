from datetime import date
import re

ELO_MINIMUM = 0
ELO_MAXIMUM = 3000
CHESS_NATIONAL_ID_PATTERN = r"^[A-Z]{2}\d{5}$"


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

    @staticmethod
    def _validate_non_empty_string(value: str, field_name: str):
        if not isinstance(value, str):
            raise TypeError(f"'{field_name}' must be a string")

        cleaned_value = value.strip()
        if not value.strip():
            raise ValueError(f"'{field_name}' must be a non-empty string")

        return cleaned_value

    @property
    def first_name(self):
        """
        Player's first name.

        Must be a non-empty string. Leading and trailing whitespace
        are removed when setting the value.

        Raises:
            ValueError: If the value is not a non-empty string.
        """
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        self._first_name = self._validate_non_empty_string(value, "first_name")

    @property
    def last_name(self):
        """
        Player's last name.

        Must be a non-empty string. Leading and trailing whitespace
        are removed when setting the value.

        Raises:
            ValueError: If the value is not a non-empty string.
        """
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        self._last_name = self._validate_non_empty_string(value, "last_name")

    @property
    def birth_date(self):
        """
        Player's birth name.

        Must be a date.

        Raises:
            TypeError: If the value is not a date.
        """
        return self._birth_date

    @birth_date.setter
    def birth_date(self, value):
        if not isinstance(value, date):
            raise TypeError(
                "'birth_date' doit être une date"
            )
        self._birth_date = value

    @property
    def elo_rating(self):
        return self._elo_rating

    @elo_rating.setter
    def elo_rating(self, value):
        if not isinstance(value, int):
            raise TypeError("'elo_rating' must be an integer")

        if not ELO_MINIMUM <= value <= ELO_MAXIMUM:
            raise ValueError(
                f"'elo_rating' must be between {ELO_MINIMUM} and {ELO_MAXIMUM}"
                )

        self._elo_rating = value

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
