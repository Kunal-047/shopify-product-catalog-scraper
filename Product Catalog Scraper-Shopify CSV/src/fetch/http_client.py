import random
import requests
from typing import Dict, Optional


# -----------------------------
# User Agent Pool
# -----------------------------
USER_AGENTS = [
    # Chrome
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",

    # Firefox
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) "
    "Gecko/20100101 Firefox/122.0",

    # Edge
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",

    # Mobile
    "Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"
]


# -----------------------------
# Default Headers Template
# -----------------------------
BASE_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
    "DNT": "1",
    "Upgrade-Insecure-Requests": "1",
}


class HTTPClient:
    """
    Low-level HTTP client abstraction.
    Handles:
    - header building
    - user-agent rotation
    - timeout config
    - proxy support (future ready)
    """

    def __init__(
        self,
        timeout: int = 15,
        base_headers: Optional[Dict[str, str]] = None,
        proxies: Optional[Dict[str, str]] = None,
    ):
        self.timeout = timeout
        self.base_headers = base_headers or BASE_HEADERS.copy()
        self.proxies = proxies

    def _build_headers(self) -> Dict[str, str]:
        headers = self.base_headers.copy()
        headers["User-Agent"] = random.choice(USER_AGENTS)
        return headers

    def get(self, url: str, session: Optional[requests.Session] = None) -> requests.Response:
        headers = self._build_headers()

        client = session if session else requests

        response = client.get(
            url,
            headers=headers,
            timeout=self.timeout,
            proxies=self.proxies,
            allow_redirects=True,
        )

        return response