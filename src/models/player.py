from datetime import date


class Player:
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
        if not isinstance(value, str) or not value.strip():
            raise ValueError(
                "'first_name' must be a non empty string"
                )

        self._first_name = value.strip()

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
        if not isinstance(value, str) or not value.strip():
            raise ValueError(
                "'last_name' must be a non empty string"
                )

        self._last_name = value.strip()

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

    def correct_first_name(self, new_first_name: str):
        """
        Updates the player's first name to correct a data entry error.

        This method applies the same validation rules as the 'first_name'
        setter.

        Args:
            new_first_name (str): The corrected first name.
        """
        self.first_name = new_first_name

    def correct_last_name(self, new_last_name: str):
        self.last_name = new_last_name

    def correct_birth_date(self, new_birth_date: date):
        self.birth_date = new_birth_date

    def correct_elo_rating(self, new_elo_rating: int):
        self.elo_rating = new_elo_rating

    def correct_chess_national_id(self, new_chess_national_id):
        self.chess_national_id = new_chess_national_id

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
