import hashlib
from typing import Optional


class HashUtils:
    """
    Hash utilities for deduplication:
    - URL hash
    - image hash
    - text hash
    """

    @staticmethod
    def hash_text(text: Optional[str]) -> Optional[str]:
        if not text:
            return None
        return hashlib.md5(text.strip().lower().encode("utf-8")).hexdigest()

    @staticmethod
    def hash_url(url: Optional[str]) -> Optional[str]:
        if not url:
            return None
        return hashlib.md5(url.strip().lower().encode("utf-8")).hexdigest()

    @staticmethod
    def hash_image(url: Optional[str]) -> Optional[str]:
        """
        Image URL hash (not perceptual hash — CDN-safe)
        """
        if not url:
            return None
        clean = url.split("?")[0]
        return hashlib.md5(clean.encode("utf-8")).hexdigest()
