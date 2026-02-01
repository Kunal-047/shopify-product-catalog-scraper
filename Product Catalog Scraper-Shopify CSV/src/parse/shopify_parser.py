from typing import Dict
from .base_parser import BaseParser
import json


class ShopifyParser(BaseParser):
    """
    Shopify storefront product parser
    Uses:
    - JSON-LD
    - Shopify product JSON
    - Meta tags
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
        # JSON-LD Extraction
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

        # -----------------------------
        # Shopify Product JSON
        # -----------------------------
        product_json_script = self.soup.find("script", {"type": "application/json", "id": "ProductJson"})
        if product_json_script:
            try:
                product_data = json.loads(product_json_script.string)

                data["title"] = data["title"] or product_data.get("title")
                data["description"] = data["description"] or product_data.get("body_html")
                data["vendor"] = product_data.get("vendor")
                data["category"] = product_data.get("product_type")

                images = product_data.get("images", [])
                if images:
                    data["images"] = images

                variants = product_data.get("variants", [])
                if variants:
                    v = variants[0]
                    data["sku"] = v.get("sku")
                    data["price"] = self._safe_float(v.get("price"))
                    data["availability"] = "InStock" if v.get("available") else "OutOfStock"

            except Exception:
                pass

        # -----------------------------
        # Meta tag fallback
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
        # Currency fallback
        # -----------------------------
        if not data["currency"]:
            if "₹" in self.html:
                data["currency"] = "INR"
            elif "$" in self.html:
                data["currency"] = "USD"
            elif "€" in self.html:
                data["currency"] = "EUR"

        return data
