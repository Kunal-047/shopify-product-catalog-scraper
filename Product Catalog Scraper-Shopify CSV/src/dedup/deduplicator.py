from typing import List, Dict

from .hash import HashUtils
from .similarity import SimilarityUtils


class Deduplicator:
    """
    Orchestrates deduplication logic:
    - URL hash
    - SKU match
    - fuzzy title match
    - image hash match
    """

    def __init__(self, title_threshold: float = 0.92):
        self.title_threshold = title_threshold

    def deduplicate(self, products: List[Dict]) -> List[Dict]:
        unique = []

        seen_url_hashes = set()
        seen_skus = set()
        seen_image_hashes = set()

        for product in products:
            is_duplicate = False

            # -----------------------------
            # URL Hash Dedup
            # -----------------------------
            url = product.get("source_url")
            url_hash = HashUtils.hash_url(url)

            if url_hash and url_hash in seen_url_hashes:
                is_duplicate = True

            # -----------------------------
            # SKU Dedup
            # -----------------------------
            sku = product.get("sku")
            if sku:
                sku_norm = sku.strip().upper()
                if sku_norm in seen_skus:
                    is_duplicate = True

            # -----------------------------
            # Image Hash Dedup
            # -----------------------------
            for img in product.get("images", []):
                img_hash = HashUtils.hash_image(img)
                if img_hash and img_hash in seen_image_hashes:
                    is_duplicate = True
                    break

            # -----------------------------
            # Fuzzy Title Dedup
            # -----------------------------
            if not is_duplicate:
                for u in unique:
                    if SimilarityUtils.is_similar(
                        product.get("title"),
                        u.get("title"),
                        threshold=self.title_threshold
                    ):
                        is_duplicate = True
                        break

            # -----------------------------
            # Decision
            # -----------------------------
            if not is_duplicate:
                unique.append(product)

                if url_hash:
                    seen_url_hashes.add(url_hash)

                if sku:
                    seen_skus.add(sku.strip().upper())

                for img in product.get("images", []):
                    img_hash = HashUtils.hash_image(img)
                    if img_hash:
                        seen_image_hashes.add(img_hash)

        return unique
