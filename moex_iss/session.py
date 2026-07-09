from typing import Any

import requests
from requests import Response

from .config import ISSConfig


class ISSSession:
    def __init__(
        self,
        config: ISSConfig,
    ) -> None:

        self.config = config

        self.session = requests.Session()

        self.session.headers.update(
            {
                "User-Agent": config.user_agent
            }
        )

    def close(self) -> None:

        self.session.close()

    def get(
        self,
        url: str,
        **kwargs: Any,
    ) -> Response:

        return self.session.get(
            url,
            timeout=self.config.timeout,
            verify=self.config.verify_ssl,
            **kwargs,
        )