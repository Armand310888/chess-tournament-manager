"""Controller for match creation and result entry."""

from src.models.match import Match, MatchResult
from src.models.player import Player
from src.models.round import Round
from src.models.tournament import Tournament
from src.repository.match_repository import save_matches
from src.repository.round_repository import save_rounds
from src.repository.tournament_repository import save_tournaments
from src.utils.id_generator import IDPrefix, generate_next_id


class MatchController:
    """Coordinate match creation, scoring, and persistence."""

    def __init__(
        self,
        matches: list[Match],
        rounds: list[Round],
        tournaments: list[Tournament],
    ) -> None:
        """Initialize the controller with loaded domain objects."""
        self.matches = matches
        self.rounds = rounds
        self.tournaments = tournaments

    def create_match(
        self,
        player_1: Player,
        player_2: Player,
    ) -> Match:
        """Create, register, persist, and return a new match.

        Args:
            player_1: First player assigned to the match.
            player_2: Second player assigned to the match.

        Returns:
            Created match with generated ID and assigned colors.
        """
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
        result: MatchResult,
    ) -> None:
        """Record a match result and persist impacted entities.

        Ending a match updates its lifecycle status, scores, and persistence
        state. Rounds and tournaments are also saved because they reference
        matches through their own serialized state.

        Args:
            match: Match whose result must be entered.
            result: Final match result.

        Raises:
            TypeError: If match or result has an invalid type.
            ValueError: If the match cannot be ended.
        """
        if not isinstance(match, Match):
            raise TypeError("'match' must be a Match object.")

        if not isinstance(result, MatchResult):
            raise TypeError("'result' must be a MatchResult object.")

        match.end_match(result)

        save_matches(self.matches)
        save_rounds(self.rounds)
        save_tournaments(self.tournaments)
