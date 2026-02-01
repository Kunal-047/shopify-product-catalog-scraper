from typing import Dict, List


class VariantBuilder:
    """
    Builds Shopify variant rows.
    Supports:
    - single-variant products
    - future multi-variant expansion
    """

    @staticmethod
    def build(product: Dict) -> List[Dict]:
        """
        Returns list of variant dicts (Shopify row format partial)
        """

        price = product.get("price")
        sku = product.get("sku")

        variant = {
            "Option1 Name": "Title",
            "Option1 Value": "Default Title",
            "Variant SKU": sku,
            "Variant Price": price,
            "Variant Inventory Qty": 999,   # default stock buffer
            "Variant Inventory Policy": "continue",
            "Variant Fulfillment Service": "manual",
            "Variant Requires Shipping": True,
            "Variant Taxable": True,
            "Variant Barcode": "",
            "Variant Weight": "",
            "Variant Weight Unit": "kg"
        }

        return [variant]
