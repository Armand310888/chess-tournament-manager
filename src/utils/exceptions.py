"""Custom exceptions used by application flows."""


class NoPlayersAvailableError(Exception):
    """Raised when an action requires existing players."""
    def __init__(self) -> None:
        """Initialize the exception with a user-facing message."""
        super().__init__(
            "No players available. Create players first."
        )


class RoundNotFinishedError(Exception):
    """Raised when creating a round before ending the current one."""
    def __init__(self) -> None:
        """Initialize the exception with a user-facing message."""
        super().__init__(
            "Current round still in progress. "
            "Current round must be finished before "
            "creating a new round."
        )


class TournamentFinishedError(Exception):
    """"""
