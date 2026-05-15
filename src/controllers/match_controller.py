""""""
from src.models.match import Match
from src.models.player import Player
from src.utils.id_generator import generate_next_id, IDPrefix
from src.repository.match_repository import save_matches


class MatchController:
    def create_match(
            self,
            player_1: Player,
            player_2: Player,
            matches: list[Match]
    ) -> Match:
        """"""
        match = Match(player_1, player_2)

        existing_ids = [
            existing_match.id
            for existing_match in matches
        ]

        match.id = generate_next_id(IDPrefix.MATCH, existing_ids)
        match.set_black_and_white_player()

        matches.append(match)
        save_matches(matches)

        return match
