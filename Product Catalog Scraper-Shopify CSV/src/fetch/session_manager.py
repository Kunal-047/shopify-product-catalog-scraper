import requests
from typing import Dict


class SessionManager:
    """
    Manages HTTP sessions:
    - session pooling
    - cookie persistence
    - connection reuse
    - domain-level isolation
    """

    def __init__(self):
        self.sessions: Dict[str, requests.Session] = {}

    def get_session(self, domain: str) -> requests.Session:
        """
        Returns a pooled session per domain.
        Creates one if not exists.
        """
        if domain not in self.sessions:
            session = requests.Session()

            # Default session headers (can be overridden per request)
            session.headers.update({
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.9",
                "Connection": "keep-alive",
            })

            self.sessions[domain] = session

        return self.sessions[domain]

    def close_all(self):
        """Gracefully close all sessions"""
        for session in self.sessions.values():
            session.close()
        self.sessions.clear()
