from models.round import Round
from models.player import Player


class Tournament:
    def __init__(
            self,
            name: str,
            place: str,
            list_of_rounds: list[Round],
            list_of_players: list[Player],
            number_of_rounds: int = 4,
            actual_round: int = 1,
            description: str = None
            ):

        self.name = name
        self.place = place,
        self.number_of_rounds = number_of_rounds
        self.actual_round = actual_round
        self.list_of_rounds = list_of_rounds
        self.list_of_players = list_of_players
        self.description = description
