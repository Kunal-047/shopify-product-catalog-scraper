from typing import Optional
import re
from difflib import SequenceMatcher


class SimilarityUtils:
    """
    Fuzzy matching utilities
    """

    @staticmethod
    def normalize_text(text: Optional[str]) -> str:
        if not text:
            return ""
        text = text.lower()
        text = re.sub(r"[^a-z0-9\s]", "", text)
        text = re.sub(r"\s+", " ", text)
        return text.strip()

    @staticmethod
    def similarity_ratio(a: Optional[str], b: Optional[str]) -> float:
        if not a or not b:
            return 0.0

        a_n = SimilarityUtils.normalize_text(a)
        b_n = SimilarityUtils.normalize_text(b)

        return SequenceMatcher(None, a_n, b_n).ratio()

    @staticmethod
    def is_similar(a: Optional[str], b: Optional[str], threshold: float = 0.9) -> bool:
        return SimilarityUtils.similarity_ratio(a, b) >= threshold
