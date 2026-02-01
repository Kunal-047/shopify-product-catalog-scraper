from typing import Dict, List
from .base_parser import BaseParser


class AmazonParser(BaseParser):
    """
    Amazon product page parser
    Supports:
    - JSON-LD schema
    - DOM fallback
    """

    def parse(self) -> Dict:
        jsonld = self._extract_json_ld()
        product_schema = self._find_schema_product(jsonld)

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
            "vendor": "Amazon",
            "brand": None
        }

        # -----------------------------
        # JSON-LD Primary Extraction
        # -----------------------------
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
        # DOM Fallback Extraction
        # -----------------------------
        # Title
        if not data["title"]:
            title_el = self.soup.select_one("#productTitle")
            if title_el:
                data["title"] = self._clean_text(title_el.text)

        # Price
        if not data["price"]:
            price_el = (
                self.soup.select_one(".a-price-whole") or
                self.soup.select_one("#priceblock_ourprice") or
                self.soup.select_one("#priceblock_dealprice")
            )
            if price_el:
                price_text = price_el.text.replace("₹", "").replace("$", "")
                data["price"] = self._safe_float(price_text)

        # Currency
        if not data["currency"]:
            if "₹" in self.html:
                data["currency"] = "INR"
            elif "$" in self.html:
                data["currency"] = "USD"

        # Images
        if not data["images"]:
            imgs = []
            for img in self.soup.select("#altImages img"):
                src = img.get("src")
                if src:
                    imgs.append(src)
            data["images"] = imgs

        # SKU / ASIN
        if not data["sku"]:
            asin = None
            for row in self.soup.select("#productDetails_detailBullets_sections1 tr"):
                th = row.select_one("th")
                td = row.select_one("td")
                if th and "ASIN" in th.text:
                    asin = td.text.strip()
                    break
            data["sku"] = asin

        # Category
        if not data["category"]:
            crumbs = self.soup.select("#wayfinding-breadcrumbs_container ul li a")
            if crumbs:
                data["category"] = self._clean_text(crumbs[-1].text)

        return data
