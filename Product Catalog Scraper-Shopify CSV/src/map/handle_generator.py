import re
from typing import Optional


class HandleGenerator:
    """
    Generates Shopify-safe product handles.
    """

    @staticmethod
    def generate(title: Optional[str]) -> Optional[str]:
        if not title:
            return None

        handle = title.lower()

        # Replace spaces with hyphens
        handle = re.sub(r"\s+", "-", handle)

        # Remove invalid characters
        handle = re.sub(r"[^a-z0-9\-]", "", handle)

        # Collapse multiple hyphens
        handle = re.sub(r"-{2,}", "-", handle)

        return handle.strip("-")
