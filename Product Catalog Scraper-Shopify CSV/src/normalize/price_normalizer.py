import re
from typing import Optional


class PriceNormalizer:
    """
    Handles:
    - price cleaning
    - currency normalization
    - number formatting
    - Shopify price compatibility
    """

    CURRENCY_SYMBOLS = {
        "₹": "INR",
        "$": "USD",
        "€": "EUR",
        "£": "GBP",
        "¥": "JPY"
    }

    @staticmethod
    def extract_currency(raw_text: str) -> Optional[str]:
        if not raw_text:
            return None

        for symbol, code in PriceNormalizer.CURRENCY_SYMBOLS.items():
            if symbol in raw_text:
                return code
        return None

    @staticmethod
    def normalize_price(value) -> Optional[float]:
        if value is None:
            return None

        if isinstance(value, (int, float)):
            return float(value)

        # Remove currency symbols and text
        text = str(value)

        for symbol in PriceNormalizer.CURRENCY_SYMBOLS.keys():
            text = text.replace(symbol, "")

        # Remove non-numeric except dot and comma
        text = re.sub(r"[^\d.,]", "", text)

        # Handle thousand separators
        if text.count(",") > 1:
            text = text.replace(",", "")
        else:
            # Convert comma decimal to dot
            if "," in text and "." not in text:
                text = text.replace(",", ".")

        try:
            return float(text)
        except Exception:
            return None

    @staticmethod
    def normalize_currency(existing: Optional[str], raw_text: Optional[str]) -> Optional[str]:
        if existing:
            return existing

        if raw_text:
            return PriceNormalizer.extract_currency(raw_text)

        return None
