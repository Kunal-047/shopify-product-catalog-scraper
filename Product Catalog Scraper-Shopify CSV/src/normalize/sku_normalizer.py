import re
from typing import Optional


class SKUNormalizer:
    """
    Handles:
    - SKU cleaning
    - formatting
    - consistency
    - Shopify-safe SKU format
    """

    @staticmethod
    def normalize(sku: Optional[str]) -> Optional[str]:
        if not sku:
            return None

        sku = str(sku).strip().upper()

        # Replace spaces with hyphen
        sku = re.sub(r"\s+", "-", sku)

        # Remove invalid characters (Shopify-safe)
        sku = re.sub(r"[^A-Z0-9\-_]", "", sku)

        # Collapse multiple hyphens
        sku = re.sub(r"-{2,}", "-", sku)

        return sku
