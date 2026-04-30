""""""


class NoPlayersAvailableError(Exception):
    """"""
    def __init__(self):
        super().__init__(
            "No players available. Create players first."
        )
