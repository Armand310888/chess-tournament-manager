"""Controller for round creation and tournament progression."""

from datetime import datetime

from src.controllers.match_controller import MatchController
from src.models.match import Match
from src.models.round import Round
from src.models.tournament import Tournament
from src.repository.round_repository import save_rounds
from src.repository.tournament_repository import save_tournaments
from src.services.event_status_manager import EventStatus
from src.services.pairing_manager import (
    create_random_pairs,
    pair_players_by_score,
)
from src.utils.exceptions import RoundNotFinishedError
from src.utils.id_generator import IDPrefix, generate_next_id


class RoundController:
    """Coordinate round creation and associated match generation."""
    def __init__(
        self,
        matches: list[Match],
        rounds: list[Round],
        tournaments: list[Tournament],
    ) -> None:
        """Initialize the controller with loaded rounds and tournaments."""
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
        """Create, register, and return a new tournament round.

        The round is added to the tournament, assigned a generated ID,
        persisted to storage, and set as the current round.

        For the first round, the tournament must satisfy all player-count
        requirements before it can start. For subsequent rounds, the current
        round must be finished before a new one can be created.

        Args:
            tournament: Tournament receiving the new round.

        Returns:
            Created round.

        Raises:
            TypeError: If tournament is not a Tournament object.
            RoundNotFinishedError: If the current round is still in progress.
            ValueError: If the tournament does not satisfy the requirements
                needed to start.
        """
        if not isinstance(tournament, Tournament):
            raise TypeError("'tournament' must be a Tournament object.")

        current_round = tournament.current_round

        if (
            current_round is not None
            and current_round.status != EventStatus.FINISHED
        ):
            raise RoundNotFinishedError()

        if tournament.current_round is None:
            tournament.validate_ready_to_start()

        round_number = (
            1
            if tournament.current_round is None
            else tournament.current_round.number + 1
        )

        new_round = Round(round_number)

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

    def create_matches_for_round(
        self,
        round: Round,
        tournament: Tournament,
    ) -> list[Match]:
        """Generate and persist matches for a tournament round.

        The first round uses random pairings. Subsequent rounds use score-
        based pairings while attempting to avoid repeated matchups.

        Args:
            tournament: Tournament containing participating players.
            round: Round receiving generated matches.
        """
        if round.number == 1:
            pairs = create_random_pairs(tournament.players)

        else:
            pairs = pair_players_by_score(tournament)

        for player_1, player_2 in pairs:
            match = self.match_controller.create_match(
                player_1,
                player_2,
            )

            round.matches.append(match)

        save_rounds(self.rounds)
        return round.matches

    def get_round_unfinished_matches(
            self,
            round: Round
    ) -> list[Match]:
        """Return unfinished matches for a given round.

        Args:
            round: Round whose matches must be inspected.

        Returns:
            Matches that are not finished yet.
        """
        return [
            match
            for match in round.matches
            if match.status != EventStatus.FINISHED
        ]
