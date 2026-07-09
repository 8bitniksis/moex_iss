import threading
import time


class RateLimiter:
    def __init__(self, rate: int = 5):
        """
        rate:
            requests per second
        """

        self.interval: float = 1 / rate

        self.lock = threading.Lock()

        self.last_request: float = 0.0

    def wait(self) -> None:

        with self.lock:
            now: float = time.time()

            delta = now - self.last_request

            if delta < self.interval:
                time.sleep(self.interval - delta)

            self.last_request = time.time()
