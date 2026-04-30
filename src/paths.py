""""""
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

PLAYERS_FILE = DATA_DIR / "players.json"
MATCHES_FILE = DATA_DIR / "matches.json"
ROUNDS_FILE = DATA_DIR / "rounds.json"
TOURNAMENTS_FILE = DATA_DIR / "tournaments.json"