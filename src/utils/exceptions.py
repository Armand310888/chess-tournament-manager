""""""


class NoPlayersAvailableError(Exception):
    """"""
    def __init__(self):
        super().__init__(
            "No players available. Create players first."
        )


class RoundNotFinishedError(Exception):
    """"""
    def __init__(self):
        super().__init__(
            "Current round still in progress. "
            "Current round must be finished before "
            "creating a new round."
        )
