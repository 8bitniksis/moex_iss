import base64

from moex_iss.config import ISSConfig
from moex_iss.sessions.session import ISSSession
from moex_iss.utils.exceptions import ISSAuthenticationError


class ISSAuthenticator:
    COOKIE_NAME = "MicexPassportCert"

    def __init__(
        self,
        session: ISSSession,
        config: ISSConfig,
    ) -> None:

        self.session = session
        self.config = config

    def authenticate(self) -> bool:

        if not self.config.authenticated:
            return False

        token = base64.b64encode(
            (f"{self.config.username}:{self.config.password}").encode()
        ).decode()

        headers: dict[str, str] = {"Authorization": f"Basic {token}"}

        response = self.session.get(
            self.config.auth_url,
            headers=headers,
        )

        if response.status_code != 200:
            raise ISSAuthenticationError(response.text)

        cookie = self.session.session.cookies.get(self.COOKIE_NAME)

        if not cookie:
            raise ISSAuthenticationError("MicexPassportCert cookie not found")

        return True
