from datetime import datetime

from src.models.player import Player
from src.models.match import Match
from src.models.round import Round
from src.models.tournament import Tournament
from src.views.round_view import RoundView
from src.utils.id_generator import generate_next_id, IDPrefix
from src.services.lifecycle_manager import EventStatus
from src.repository.round_repository import save_rounds
from src.repository.tournament_repository import save_tournaments
from src.services.pairing_manager import create_random_pairs
from src.services.ranking_manager import get_players_ranked


class RoundController:
    def __init__(self):
        self.round_view = RoundView()

    def create_list_of_matchs(self, current_round: Round):
        pass

    def create_new_round(
            self,
            tournament: Tournament,
            rounds: list[Round],
            tournaments: list[Tournament]
    ) -> Round:
        """"""
        round_number = (
            1
            if tournament.current_round is None
            else tournament.current_round.number + 1
        )

        new_round = Round(round_number)
        if tournament.current_round is None:
            tournament.current_round = new_round

        existing_ids = [
            round.id
            for round in rounds
        ]

        new_round.id = generate_next_id(IDPrefix.ROUND, existing_ids)
        new_round.start_datetime = datetime.now()
        new_round.status = EventStatus.IN_PROGRESS

        tournament.rounds.append(new_round)
        save_tournaments(tournaments)

        rounds.append(new_round)
        save_rounds(rounds)

        return new_round

    def create_match_for_round(
            tournament: Tournament,
    ) -> None:
        if tournament.current_round.number == 1:
            pairs = create_random_pairs(tournament.players)

            for pair in pairs:
                player_1 = pair[0]
                player_2 = pair[1]
                new_match = Match(player_1, player_2)
                tournament.current_round.matches.append(new_match)

        if tournament.current_round.number != 1:
            players_ranked = get_players_ranked(tournament)








      