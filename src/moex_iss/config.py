from dataclasses import dataclass


@dataclass(slots=True)
class ISSConfig:
    """
    MOEX ISS configuration
    """

    username: str | None = None
    password: str | None = None

    base_url: str = "https://iss.moex.com"

    auth_url: str = "https://passport.moex.com/authenticate"

    timeout: float = 10.0

    retries: int = 5

    verify_ssl: bool = True

    user_agent: str = "moex-iss-python-client/1.0"

    debug: bool = False

    @property
    def authenticated(self) -> bool:
        return bool(self.username and self.password)
