""""""
from datetime import datetime

from src.models.match import Match
from src.models.round import Round
from src.models.tournament import Tournament
from src.controllers.match_controller import MatchController
from src.utils.id_generator import generate_next_id, IDPrefix
from src.utils.exceptions import RoundNotFinishedError
from src.services.lifecycle_manager import EventStatus
from src.repository.round_repository import save_rounds
from src.repository.tournament_repository import save_tournaments
from src.services.pairing_manager import (
    create_random_pairs,
    pair_players_by_score
)


class RoundController:
    """"""
    def __init__(
            self,
            matches: list[Match],
            rounds: list[Round],
            tournaments: list[Tournament],
    ) -> None:
        """"""
        self.matches = matches
        self.rounds = rounds
        self.tournaments = tournaments
        self.match_controller = MatchController(
            self.matches,
            self.rounds,
            self.tournaments
        )

    def create_new_round(
            self,
            tournament: Tournament,
    ) -> Round:
        """"""
        current_round = tournament.current_round

        if (
            current_round is not None
            and current_round.status != EventStatus.FINISHED
        ):
            raise RoundNotFinishedError()

        round_number = (
            1
            if tournament.current_round is None
            else tournament.current_round.number + 1
        )

        new_round = Round(round_number)
        if tournament.current_round is None:
            tournament.current_round = new_round

        existing_ids = [
            existing_round.id
            for existing_round in self.rounds
        ]

        new_round.id = generate_next_id(IDPrefix.ROUND, existing_ids)
        new_round.start_datetime = datetime.now()

        tournament.rounds.append(new_round)
        save_tournaments(self.tournaments)

        self.rounds.append(new_round)
        save_rounds(self.rounds)

        return new_round

    def create_match_for_round(
            self,
            round: Round,
            tournament: Tournament,
    ) -> None:
        """"""
        if round.number == 1:
            pairs = create_random_pairs(tournament.players)

        if round.number != 1:
            pairs = pair_players_by_score(tournament)

        for player_1, player_2 in pairs:
            match = self.match_controller.create_match(
                player_1,
                player_2,
                self.matches
            )

            round.matches.append(match)
            save_rounds(self.rounds)

