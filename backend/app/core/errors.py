class DomainError(Exception):
    """A business rule was broken. main.py maps each subclass to an HTTP status."""


class EmailAlreadyRegisteredError(DomainError):
    def __init__(self, email: str) -> None:
        super().__init__(f"Email already registered: {email}")
        self.email = email
