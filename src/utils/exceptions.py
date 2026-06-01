"""Custom exceptions used by application flows."""


class NoPlayersAvailableError(ValueError):
    """Raised when an action requires existing players."""

    def __init__(self) -> None:
        """Initialize the exception with a user-facing message."""
        super().__init__(
            "No players available. Create players first."
        )


class RoundNotFinishedError(ValueError):
    """Raised when creating a round before ending the current one."""

    def __init__(self) -> None:
        """Initialize the exception with a user-facing message."""
        super().__init__(
            "Current round still in progress. "
            "Current round must be finished before "
            "creating a new round."
        )


class TournamentFinishedError(ValueError):
    """Raised when an action requires a tournament still in progress."""
