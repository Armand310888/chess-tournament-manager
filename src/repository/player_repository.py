
def get_player_by_id():
    pass


def load_players():
    pass


def save_players():
    pass


def load_all_players() -> list[Player]:
    if not DATA_DIR.exists():
        DATA_DIR.mkdir()

    if not PLAYERS_FILE.exists():
        return []

    with open(PLAYERS_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    all_players = []

    for player_data in data:
        player = player_from_dict(player_data)
        all_players.append(player)

    return all_players
# quid gestion erreur?

def save_all_players(all_players: list[Player]):
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    all_players_data = []

    for player in all_players:
        player_data = player_to_dict(player)
        all_players_data.append(player_data)

    with open(PLAYERS_FILE, "w", encoding="utf-8") as file:
        json.dump(all_players_data, file, indent=4)
# quid gestion erreur?