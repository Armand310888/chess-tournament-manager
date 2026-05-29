"""Player ranking helpers for tournament standings."""

from src.models.player import Player
from src.models.tournament import Tournament
from src.services.event_status_manager import EventStatus


def get_player_score(player: Player, tournament: Tournament) -> float:
    """Return a player's total score in a tournament.

    Only finished matches are counted. The player must belong to the
    tournament before their score can be computed.

    Args:
        player: Player whose score must be computed.
        tournament: Tournament containing the player and played rounds.

    Returns:
        Sum of the player's scores across finished matches.

    Raises:
        ValueError: If the player does not belong to the tournament.
    """
    if player not in tournament.players:
        raise ValueError("Player does not belong to this tournament.")

    total_score = 0

    for round in tournament.rounds:
        for match in round.matches:
            if match.status == EventStatus.FINISHED:
                if match.white_player == player:
                    total_score += match.white_player_score
                elif match.black_player == player:
                    total_score += match.black_player_score

    return total_score


def get_players_ranked(tournament: Tournament) -> list[tuple[Player, float]]:
    """Return tournament players sorted by descending score.

    Args:
        tournament: Tournament whose players must be ranked.

    Returns:
        List of ``(player, score)`` tuples sorted from highest to lowest
        score.
    """
    players_to_rank = []

    for player in tournament.players:
        total_score = get_player_score(player, tournament)
        players_to_rank.append((player, total_score))

    ranked_players = sorted(
        players_to_rank,
        key=lambda player_score: (
            -player_score[1],
            player_score[0].last_name.lower(),
            player_score[0].first_name.lower(),
        )
    )

    return ranked_players


def group_players_by_score(
        ranked_players: list[Player, float]
) -> dict[float, list[Player]]:
    """Group ranked players by identical tournament score.

    Args:
        ranked_players: ``(player, score)`` tuples sorted by score.

    Returns:
        Dictionary mapping each score to the players sharing that score,
        sorted from highest to lowest score.
    """
    players_grouped_by_score = {}

    for player, score in ranked_players:
        if score not in players_grouped_by_score:
            players_grouped_by_score[score] = []
        players_grouped_by_score[score].append(player)

    return dict(
        sorted(
            players_grouped_by_score.items(),
            reverse=True
        )
    )
