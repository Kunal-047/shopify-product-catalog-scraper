from urllib.parse import urlparse, urlunparse, parse_qs
from typing import List


class ImageNormalizer:
    """
    Handles:
    - image URL cleaning
    - tracking param removal
    - CDN normalization
    - https enforcement
    - deduplication
    - Shopify compatibility
    """

    @staticmethod
    def clean_url(url: str) -> str:
        if not url:
            return None

        parsed = urlparse(url)

        # Force https
        scheme = "https"

        # Remove query params (tracking, resizing, tokens)
        clean_query = ""

        clean_parsed = parsed._replace(scheme=scheme, query=clean_query)

        return urlunparse(clean_parsed)

    @staticmethod
    def normalize_images(images: List[str]) -> List[str]:
        if not images:
            return []

        cleaned = []
        seen = set()

        for img in images:
            try:
                clean = ImageNormalizer.clean_url(img)
                if clean and clean not in seen:
                    seen.add(clean)
                    cleaned.append(clean)
            except Exception:
                continue

        return cleaned
