class Error(Exception):
    pass

class LoginError(Error):
    """Raise when non-HTTP(S) error occurs during login."""

class NotRecognized(Error):
    """Raise when a problem url is not recognized."""

class SubmissionError(Error):
    """Raise when non-HTTP(S) error occurs during submission."""
