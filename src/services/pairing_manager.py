"""Player pairing helpers for tournament rounds."""

import random

from src.models.player import Player
from src.models.round import Round
from src.models.tournament import Tournament
from src.services.ranking_manager import (
    get_players_ranked,
    group_players_by_score,
)


def create_random_pairs(
        list_of_players: list[Player]
) -> list[tuple[Player, Player]]:
    """Create random player pairs for a tournament round."""
    if len(list_of_players) % 2 != 0:
        raise ValueError(
            "An even number of players is required to create pairs."
        )

    shuffled_players = list_of_players.copy()
    random.shuffle(shuffled_players)

    pairs = []

    for index in range(0, len(shuffled_players), 2):
        pair = (shuffled_players[index], shuffled_players[index + 1])
        pairs.append(pair)

    return pairs


def have_players_been_opposed(
        player_1: Player,
        player_2: Player,
        rounds: list[Round]
) -> bool:
    """Check whether two players have already played each other.

    Args:
        player_1: First player to compare.
        player_2: Second player to compare.
        rounds: Rounds whose matches must be checked.

    Returns:
        True if the players have already been opposed, otherwise False.
    """
    for round in rounds:
        for match in round.matches:
            if (
                (player_1 == match.player_1 and player_2 == match.player_2)
                or
                (player_1 == match.player_2 and player_2 == match.player_1)
            ):
                return True

    return False


def find_valid_opponent(
        player_to_pair: Player,
        players_group: list[Player],
        tournament: Tournament) -> Player | None:
    """Find an opponent not already paired with the given player.

    Args:
        player_to_pair: Player needing an opponent.
        players_group: Candidate opponents from the current score group.
        tournament: Tournament whose previous rounds are checked.

    Returns:
        A valid opponent if one is found, otherwise None.
    """
    for opponent in players_group:
        if opponent == player_to_pair:
            continue

        if not have_players_been_opposed(
            player_to_pair,
            opponent,
            tournament.rounds
        ):
            return opponent

    return None


def pair_players_by_score(
        tournament: Tournament
) -> list[tuple[Player, Player]]:
    """Create score-based pairs while avoiding previous matchups."""
    ranked_players = get_players_ranked(tournament)
    players_grouped_by_score = group_players_by_score(ranked_players)
    players_groups = list(players_grouped_by_score.values())

    pairs = []
    leftover_players = []

    for index, players_group in enumerate(players_groups):
        is_last_group = index == len(players_groups) - 1

        players_to_pair = leftover_players + players_group
        random.shuffle(players_to_pair)

        leftover_players = []

        while len(players_to_pair) >= 2:
            player_to_pair = players_to_pair.pop(0)

            opponent = find_valid_opponent(
                player_to_pair,
                players_to_pair,
                tournament
            )

            if opponent is None:
                if is_last_group:
                    # Last fallback: force a rematch.
                    opponent = players_to_pair.pop(0)
                else:
                    # Move player down to the next score group.
                    leftover_players.append(player_to_pair)
                    continue
            else:
                players_to_pair.remove(opponent)

            pairs.append((player_to_pair, opponent))

        leftover_players.extend(players_to_pair)

    return pairs
