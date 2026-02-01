from typing import List, Dict

from .handle_generator import HandleGenerator
from .html_builder import HTMLBuilder
from .variant_builder import VariantBuilder
from .image_mapper import ImageMapper
from .shopify_schema import SHOPIFY_COLUMNS, DEFAULT_VALUES


class ShopifyMapper:
    """
    Orchestrates Shopify mapping:
    normalized_product → Shopify CSV rows
    """

    def map(self, products: List[Dict]) -> List[Dict]:
        rows = []

        for product in products:
            rows.extend(self.map_product(product))

        return rows

    def map_product(self, product: Dict) -> List[Dict]:
        rows = []

        handle = HandleGenerator.generate(product.get("title"))
        if not handle:
            return []

        title = product.get("title")
        body_html = HTMLBuilder.build(product.get("description"))
        vendor = product.get("vendor") or product.get("brand") or "Generic"
        product_type = product.get("category") or "General"
        tags = product.get("brand") or ""

        base_row = {
            "Handle": handle,
            "Title": title,
            "Body (HTML)": body_html,
            "Vendor": vendor,
            "Product Type": product_type,
            "Tags": tags,
            **DEFAULT_VALUES
        }

        # -----------------------------
        # Variants
        # -----------------------------
        variants = VariantBuilder.build(product)

        for idx, variant in enumerate(variants):
            row = base_row.copy()
            row.update(variant)

            # -----------------------------
            # Images (first image on first variant row)
            # -----------------------------
            images = product.get("images", [])
            if idx == 0 and images:
                row["Image Src"] = images[0]
                row["Image Position"] = 1
            else:
                row["Image Src"] = ""
                row["Image Position"] = ""

            rows.append(row)

        # -----------------------------
        # Additional image rows
        # -----------------------------
        images = product.get("images", [])
        if len(images) > 1:
            image_rows = ImageMapper.map(handle, images[1:])
            for img_row in image_rows:
                row = {
                    "Handle": handle,
                    "Image Src": img_row["Image Src"],
                    "Image Position": img_row["Image Position"],
                }

                # Fill empty columns
                for col in SHOPIFY_COLUMNS:
                    if col not in row:
                        row[col] = ""

                row["Status"] = DEFAULT_VALUES.get("Status", "active")
                rows.append(row)

        # -----------------------------
        # Column order enforcement
        # -----------------------------
        ordered_rows = []
        for row in rows:
            ordered = {}
            for col in SHOPIFY_COLUMNS:
                ordered[col] = row.get(col, "")
            ordered_rows.append(ordered)

        return ordered_rows
