""""""
from src.models.match import Match, MatchResult
from src.models.player import Player
from src.models.round import Round
from src.models.tournament import Tournament
from src.utils.id_generator import generate_next_id, IDPrefix
from src.repository.match_repository import save_matches
from src.repository.round_repository import save_rounds
from src.repository.tournament_repository import save_tournaments


class MatchController:
    def __init__(
            self,
            matches: list[Match],
            rounds: list[Round],
            tournaments: list[Tournament],
    ) -> None:
        self.matches = matches
        self.rounds = rounds
        self.tournaments = tournaments

    def create_match(
            self,
            player_1: Player,
            player_2: Player,
    ) -> Match:
        """"""
        match = Match(player_1, player_2)

        existing_ids = [
            existing_match.id
            for existing_match in self.matches
        ]

        match.id = generate_next_id(IDPrefix.MATCH, existing_ids)
        match.set_black_and_white_player()

        self.matches.append(match)
        save_matches(self.matches)

        return match

    def enter_match_results(
            self,
            match: Match,
            result: MatchResult
    ) -> None:
        """"""
        if not isinstance(match, Match):
            raise TypeError("'match' must be a Match object.")

        if not isinstance(result, MatchResult):
            raise TypeError("'result' must be a MatchResult object")

        match.end_match(result)

        save_matches(self.matches)
        save_rounds(self.rounds)
        save_tournaments(self.tournaments)
