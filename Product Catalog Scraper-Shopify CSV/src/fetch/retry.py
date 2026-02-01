import time
import random
from typing import Callable, Any, Tuple
import requests


class RetryHandler:
    """
    Handles:
    - retry logic
    - exponential backoff
    - jitter
    - network failure recovery
    - status-code based retry
    """

    def __init__(
        self,
        max_retries: int = 3,
        base_delay: float = 1.0,
        max_delay: float = 15.0,
        retry_statuses: Tuple[int, ...] = (429, 500, 502, 503, 504),
    ):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.retry_statuses = retry_statuses

    def _backoff(self, attempt: int) -> float:
        """
        Exponential backoff with jitter
        """
        delay = min(self.base_delay * (2 ** attempt), self.max_delay)
        jitter = random.uniform(0, delay * 0.2)
        return delay + jitter

    def run(self, func: Callable, *args, **kwargs) -> requests.Response:
        """
        Executes a function with retry logic.
        func should return requests.Response
        """
        last_exception = None

        for attempt in range(self.max_retries + 1):
            try:
                response = func(*args, **kwargs)

                if response.status_code in self.retry_statuses:
                    raise requests.HTTPError(
                        f"Retryable status code: {response.status_code}"
                    )

                return response

            except Exception as e:
                last_exception = e

                if attempt >= self.max_retries:
                    break

                sleep_time = self._backoff(attempt)
                time.sleep(sleep_time)

        raise last_exception
