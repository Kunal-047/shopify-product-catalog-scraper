from typing import Dict
from .base_parser import BaseParser


class GenericParser(BaseParser):
    """
    Site-agnostic fallback parser.
    Used when no specific site parser is available.
    """

    def parse(self) -> Dict:
        data = {
            "source_url": self.url,
            "title": None,
            "description": None,
            "price": None,
            "currency": None,
            "images": [],
            "sku": None,
            "availability": None,
            "category": None,
            "vendor": None,
            "brand": None
        }

        # -----------------------------
        # JSON-LD first
        # -----------------------------
        jsonld = self._extract_json_ld()
        product_schema = self._find_schema_product(jsonld)

        if product_schema:
            data["title"] = self._clean_text(product_schema.get("name"))
            data["description"] = self._clean_text(product_schema.get("description"))

            offers = product_schema.get("offers", {})
            if isinstance(offers, dict):
                data["price"] = self._safe_float(offers.get("price"))
                data["currency"] = offers.get("priceCurrency")
                data["availability"] = offers.get("availability")

            data["images"] = self._safe_list(product_schema.get("image"))

            brand = product_schema.get("brand")
            if isinstance(brand, dict):
                data["brand"] = brand.get("name")
            elif isinstance(brand, str):
                data["brand"] = brand

            data["sku"] = product_schema.get("sku")

        # -----------------------------
        # Meta fallback
        # -----------------------------
        if not data["title"]:
            og_title = self.soup.find("meta", property="og:title")
            if og_title:
                data["title"] = self._clean_text(og_title.get("content"))

        if not data["description"]:
            og_desc = self.soup.find("meta", property="og:description")
            if og_desc:
                data["description"] = self._clean_text(og_desc.get("content"))

        if not data["images"]:
            og_img = self.soup.find("meta", property="og:image")
            if og_img:
                data["images"] = [og_img.get("content")]

        # -----------------------------
        # DOM heuristics fallback
        # -----------------------------
        if not data["price"]:
            price_candidates = self.soup.select(
                "[class*='price'], [id*='price'], meta[itemprop='price']"
            )
            for el in price_candidates:
                text = el.get("content") or el.text
                if text:
                    val = self._safe_float(text.replace("₹", "").replace("$", "").replace("€", ""))
                    if val:
                        data["price"] = val
                        break

        # -----------------------------
        # Currency detection
        # -----------------------------
        if not data["currency"]:
            if "₹" in self.html:
                data["currency"] = "INR"
            elif "$" in self.html:
                data["currency"] = "USD"
            elif "€" in self.html:
                data["currency"] = "EUR"

        return data
