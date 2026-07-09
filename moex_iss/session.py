import requests

from .config import ISSConfig


class ISSSession:
    def __init__(self, config: ISSConfig):

        self.config = config

        self.session = requests.Session()

        self.session.headers.update({"User-Agent": config.user_agent})

    def close(self):

        self.session.close()

    def get(self, url, **kwargs):

        return self.session.get(
            url, timeout=self.config.timeout, verify=self.config.verify_ssl, **kwargs
        )
