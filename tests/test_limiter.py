import time

from moex_iss.limiter import RateLimiter


def test_rate_limiter():


    limiter = RateLimiter(
        rate=10
    )


    start=time.time()


    limiter.wait()

    limiter.wait()


    elapsed = (
        time.time()
        -
        start
    )


    assert elapsed >= 0.1