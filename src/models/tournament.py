from datetime import date

from models.round import Round
from models.player import Player
from utils.validators import (
    validate_non_empty_string,
    validate_street_number,
    validate_postal_code,
    validate_date,
    validate_date_order,
    validate_number
)

DEFAULT_ROUND_NUMBER = 4

class Address:
    def __init__(
        self,
        street_number: str,
        street_name: str,
        postal_code: str,
        city: str
    ):
        self.street_number = validate_street_number(street_number)
        self.street_name = validate_non_empty_string(street_name, "street_name")
        self.postal_code = validate_postal_code(postal_code)
        self.city = validate_non_empty_string(city, "city")


class Tournament:
    def __init__(
            self,
            name: str,
            place: Address,
            start_date: date,
            end_date: date,
            number_of_players: int,
            number_of_rounds: int = DEFAULT_ROUND_NUMBER,
            description: str | None = None
            ):
        self.name = name
        self.place = place
        self.start_date = start_date
        self.end_date = end_date
        self.number_of_players = number_of_players
        self.number_of_rounds = number_of_rounds
        self.description = description
        self.id: int | None = None
        self.list_of_players: list[Player] | None = None
        self.list_of_rounds: list[Round] | None = None
        self.actual_round: Round | None = None

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = validate_non_empty_string(value, "name")

    @property
    def place(self):
        return self._place

    @place.setter
    def place(self, value):
        if not isinstance(value, Address):
            raise ValueError("Place must be an Address object")

    @property
    def start_date(self):
        return self._start_date

    @start_date.setter
    def start_date(self, value):
        validated_date = validate_date(value, "start_date")

        if hasattr(self, "_end_date") and self._end_date is not None:
            validate_date_order(validated_date, self._end_date)

        self._start_date = validated_date

    @property
    def end_date(self):
        return self._end_date

    @end_date.setter
    def end_date(self, value):
        validated_date = validate_date(value, "end_date")

        if hasattr(self, "_start_date") and self._start_date is not None:
            validate_date_order(self._start_date, validated_date)

        self._end_date = validated_date

    @property
    def number_of_players(self):
        return self._number_of_players

    @number_of_players.setter
    def number_of_players(self, value):
        self._number_of_players = validate_number(
            value,
            "number_of_players",
            int,
            2
        )

    @property
    def number_of_rounds(self):
        return self._number_of_rounds

    @number_of_rounds.setter
    def number_of_rounds(self, value):
        self._number_of_rounds = validate_number(
            value,
            "number_of_rounds",
            int,
            1
        )

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = validate_non_empty_string(value, "description")

    def add_round(self, round: Round):
        if not isinstance(round, Round):
            raise ValueError(f"'{round}' must be a Round object.")

        if len(self.list_of_rounds) >= self.number_of_rounds:
            raise ValueError(
                "Maximum number of rounds set for this tournament "
                "has already been reached."
                )

        self.list_of_rounds.append(round)

    def add_player(self, player: Player):
        if not isinstance(player, Player):
            raise ValueError(f"'{player} must be a Player object.")

        if len(self.list_of_players) >= self.number_of_players:
            raise ValueError(
                "Maximum number of players set for this tournament "
                "has already been reached."
            )

        self.list_of_players.append(player)

    def set_actual_round(self, round: Round, list_of_rounds: list[Round]):
        if not isinstance(round, Round):
            raise TypeError("'round' must be a Round class object.")

        if not isinstance(list_of_rounds, list[Round]):
            raise TypeError(
                "'list_of_rounds' must be a list of Round class objects."
                )

        if round in list_of_rounds:
            self.actual_round = round.number

    def delete_round(self):
        pass

    def delete_player(self):
        pass

