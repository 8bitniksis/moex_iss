import threading
import time


class RateLimiter:
    def __init__(self, rate=5):
        """
        rate:
            requests per second
        """

        self.interval = 1 / rate

        self.lock = threading.Lock()

        self.last_request = 0

    def wait(self):

        with self.lock:
            now = time.time()

            delta = now - self.last_request

            if delta < self.interval:
                time.sleep(self.interval - delta)

            self.last_request = time.time()
