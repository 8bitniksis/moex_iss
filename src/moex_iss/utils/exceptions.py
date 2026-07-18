class ISSException(Exception):
    """
    Base exception for MOEX ISS client
    """

    pass


class ISSConnectionError(ISSException):
    """
    Network problems
    """

    pass


class ISSAuthenticationError(ISSException):
    """
    Authentication failed
    """

    pass


class ISSResponseError(ISSException):
    """
    Invalid response from ISS
    """

    pass


class ISSServerError(ISSException):
    """
    HTTP 5xx errors from MOEX ISS
    """

    def __init__(
        self,
        status_code: int,
        message: str | None = None,
    ) -> None:

        self.status_code = status_code

        self.message = message or f"MOEX ISS server error {status_code}"

        super().__init__(self.message)


class ISSRateLimitError(ISSException):
    """
    HTTP 429 Too Many Requests
    """

    pass


class ISSPaginationError(ISSException):
    pass
