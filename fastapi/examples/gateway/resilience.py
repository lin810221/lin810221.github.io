import asyncio
import math
import httpx


async def fetch_json(client, path, *, attempts=2, deadline=2, sleep=asyncio.sleep):
    if not path.startswith('/') or path.startswith('//') or '://' in path or not 1 <= attempts <= 3 or not math.isfinite(deadline) or deadline <= 0:
        raise ValueError('relative path and finite bounded policy required')
    async with asyncio.timeout(deadline):
        for attempt in range(attempts):
            try:
                response = await client.get(path)
                if response.status_code not in {429, 502, 503, 504}:
                    response.raise_for_status()
                    return response.json()
                response.raise_for_status()
            except (httpx.TimeoutException, httpx.NetworkError, httpx.HTTPStatusError) as error:
                transient = not isinstance(error, httpx.HTTPStatusError) or error.response.status_code in {429, 502, 503, 504}
                if not transient or attempt + 1 == attempts:
                    raise
                await sleep(.01 * 2 ** attempt)


class TokenBucket:
    """Single-threaded teaching model; not a distributed service limiter."""
    def __init__(self, rate, capacity, now=0):
        if any(not math.isfinite(x) for x in (rate, capacity, now)) or rate <= 0 or capacity < 1 or now < 0:
            raise ValueError('invalid bucket')
        self.rate, self.capacity, self.tokens, self.last = rate, capacity, capacity, now

    def take(self, now):
        if not math.isfinite(now) or now < self.last:
            raise ValueError('monotonic finite clock required')
        self.tokens = min(self.capacity, self.tokens + (now - self.last) * self.rate)
        self.last = now
        if self.tokens < 1:
            return False
        self.tokens -= 1
        return True


def nearest_rank(samples, quantile):
    if not samples or not 0 < quantile <= 1 or any(not math.isfinite(x) or x < 0 for x in samples):
        raise ValueError('nonempty finite observations required')
    values = sorted(samples)
    return values[math.ceil(quantile * len(values)) - 1]
