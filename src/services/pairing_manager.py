import random

from src.models.player import Player
from src.models.round import Round
from src.models.tournament import Tournament
from src.services.ranking_manager import (
    get_players_ranked,
    group_players_by_rank,
)


def shuffle_a_list(list_to_shuffle: list):
    shuffled_list = list_to_shuffle[:]

    if len(shuffled_list) < 2:
        raise ValueError("A minimum of two players are required.")

    random.shuffle(shuffled_list)

    return shuffled_list


def create_random_pairs(list_of_players: list[Player]):
    shuffled_players = shuffle_a_list(list_of_players)

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
    """"""
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
    """"""
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
    """Pair players according to their tournament scores.

    Players are grouped by score and paired within their own score
    group whenever possible. Players without a valid opponent are
    moved to the next lower score group.

    In the final score group, rematches may be forced to avoid
    leaving players unpaired.

    Args:
        tournament: Tournament containing players and played rounds.

    Returns:
        A list of paired players.
    """
    ranked_players = get_players_ranked(tournament)
    players_grouped_by_ranks = group_players_by_rank(ranked_players)
    players_groups = list(players_grouped_by_ranks.values())

    pairs = []
    leftover_players = []

    for index, players_group in enumerate(players_groups):
        is_last_group = index == len(players_groups) - 1

        players_to_pair = shuffle_a_list(
            leftover_players + players_group
        )
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
