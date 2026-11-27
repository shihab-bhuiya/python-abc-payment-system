from abc import ABC, abstractmethod
from collections import deque
from time import monotonic


# 1. Interface
class RateLimiter(ABC):

    @abstractmethod
    def allow_request(self, user_id: str) -> bool:
        pass


# 2. Fixed Window Algorithm
class FixedWindowLimiter(RateLimiter):

    def __init__(self, limit, window):
        self.limit = limit
        self.window = window
        self.requests = {}

    def allow_request(self, user_id):

        now = monotonic()

        start, count = self.requests.get(
            user_id, (now, 0)
        )

        if now - start >= self.window:
            start, count = now, 0

        if count >= self.limit:
            return False

        self.requests[user_id] = (start, count + 1)

        return True


# 3. Sliding Window Algorithm
class SlidingWindowLimiter(RateLimiter):

    def __init__(self, limit, window):
        self.limit = limit
        self.window = window
        self.requests = {}

    def allow_request(self, user_id):

        now = monotonic()

        timestamps = self.requests.setdefault(
            user_id, deque()
        )

        while timestamps and now - timestamps[0] >= self.window:
            timestamps.popleft()

        if len(timestamps) >= self.limit:
            return False

        timestamps.append(now)

        return True


# 4. Token Bucket Algorithm
class TokenBucketLimiter(RateLimiter):

    def __init__(self, capacity, refill_rate):
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.buckets = {}

    def allow_request(self, user_id):

        now = monotonic()

        tokens, last_update = self.buckets.get(
            user_id, (self.capacity, now)
        )

        elapsed = now - last_update

        tokens = min(
            self.capacity,
            tokens + elapsed * self.refill_rate
        )

        if tokens < 1:
            self.buckets[user_id] = (tokens, now)
            return False

        self.buckets[user_id] = (tokens - 1, now)

        return True


# 5. Application depends on the interface
class APIService:

    def __init__(self, limiter: RateLimiter):
        self.limiter = limiter

    def handle_request(self, user_id):

        if not self.limiter.allow_request(user_id):
            return "429 - Too Many Requests"

        return "200 - Request Successful"


# 6. Switch implementation without changing APIService
limiter = TokenBucketLimiter(
    capacity=5,
    refill_rate=1
)

api = APIService(limiter)


# 7. Simulate requests
for i in range(8):

    result = api.handle_request("user_101")

    print(f"Request {i + 1}: {result}")