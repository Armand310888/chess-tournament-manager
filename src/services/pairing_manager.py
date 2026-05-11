import random

from src.models.player import Player


def shuffle_a_list(list_to_shuffle: list):
    shuffled_list = list_to_shuffle[:]

    if len(shuffled_list) < 2:
        raise ValueError("A minimum of two players are required.")

    if len(shuffled_list) % 2 != 0:
        raise ValueError("Number of players must be pair.")

    random.shuffle(shuffled_list)

    return shuffled_list


def create_random_pairs(list_of_players: list[Player]):
    shuffled_players = shuffle_a_list(list_of_players)

    pairs = []

    for index in range(0, len(shuffled_players), 2):
        pair = (shuffled_players[index], shuffled_players[index + 1])
        pairs.append(pair)

    return pairs
