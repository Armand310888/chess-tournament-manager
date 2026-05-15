from src.models.player import Player
from src.models.tournament import Tournament
from src.services.lifecycle_manager import EventStatus


def get_player_score(player: Player, tournament: Tournament):
    """"""
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


def get_players_ranked(tournament: Tournament) -> list[Player]:
    """"""
    players_to_rank = []

    for player in tournament.players:
        total_score = get_player_score(player, tournament)
        players_to_rank.append((player, total_score))

    ranked_players = sorted(
        players_to_rank,
        key=lambda x: x[1],
        reverse=True
    )

    return ranked_players


def group_players_by_rank(ranked_players: list):
    players_grouped_by_ranks = {}

    for player, score in ranked_players:
        if score not in players_grouped_by_ranks:
            players_grouped_by_ranks[score] = []
        players_grouped_by_ranks[score].append(player)

    return dict(
        sorted(
            players_grouped_by_ranks,
            reverse=True
        )
    )
