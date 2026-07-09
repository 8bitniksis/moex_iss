import base64

from .exceptions import ISSAuthenticationError



class ISSAuthenticator:


    COOKIE_NAME = (
        "MicexPassportCert"
    )


    def __init__(
        self,
        session,
        config
    ):

        self.session = session
        self.config = config



    def authenticate(self):

        if not self.config.authenticated:
            return False


        token = base64.b64encode(
            (
                f"{self.config.username}:"
                f"{self.config.password}"
            ).encode()
        ).decode()



        headers = {
            "Authorization":
                f"Basic {token}"
        }


        response = self.session.get(
            self.config.auth_url,
            headers=headers
        )


        if response.status_code != 200:
            raise ISSAuthenticationError(
                response.text
            )


        cookie = (
            self.session.session.cookies.get(
                self.COOKIE_NAME
            )
        )


        if not cookie:

            raise ISSAuthenticationError(
                "MicexPassportCert cookie not found"
            )


        return True