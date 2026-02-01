from typing import Dict

from src.normalize.text_cleaner import TextCleaner
from src.normalize.price_normalizer import PriceNormalizer
from src.normalize.image_normalizer import ImageNormalizer
from src.normalize.sku_normalizer import SKUNormalizer


class Normalizer:
    """
    Orchestrates full product normalization:
    raw_product → clean_product
    """

    def normalize(self, raw_product: Dict) -> Dict:
        product = raw_product.copy()

        # -----------------------------
        # Text Fields
        # -----------------------------
        for item in product:
            item["title"] = TextCleaner.clean_text(item.get("title"))
            item["description"] = TextCleaner.clean_html(item.get("description"))

        # -----------------------------
        # Price + Currency
        # -----------------------------
        for item in product:
            item["price"] = PriceNormalizer.normalize_price(item.get("price"))
            item["currency"] = PriceNormalizer.normalize_currency(item.get("currency"), str(item.get("price")))

        # -----------------------------
        # Images
        # -----------------------------
        for item in product:
            item["images"] = ImageNormalizer.normalize_images(item.get("images", []))

        # -----------------------------
        # SKU
        # -----------------------------
        for item in product:
            item["sku"] = SKUNormalizer.normalize(item.get("sku"))

        # -----------------------------
        # Category Standardization
        # -----------------------------
        for item in product:
            if item.get("category"):
                item["category"] = TextCleaner.clean_text(item.get("category"))

        # -----------------------------
        # Vendor / Brand
        # -----------------------------
        for item in product:
            if item.get("vendor"):
                item["vendor"] = TextCleaner.clean_text(item.get("vendor"))

            if item.get("brand"):
                item["brand"] = TextCleaner.clean_text(item.get("brand"))

        # -----------------------------
        # Availability Normalization
        # -----------------------------
        for item in product:
            availability = item.get("availability")
            if availability:
                av = availability.lower()
                if "in" in av:
                    item["availability"] = "InStock"
                elif "out" in av:
                    item["availability"] = "OutOfStock"
            else:
                item["availability"] = "Unknown"

        return product
