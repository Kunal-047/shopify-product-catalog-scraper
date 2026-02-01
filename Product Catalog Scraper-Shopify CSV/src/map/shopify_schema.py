"""
Defines Shopify CSV schema and defaults
"""

SHOPIFY_COLUMNS = [
    "Handle",
    "Title",
    "Body (HTML)",
    "Vendor",
    "Product Type",
    "Tags",
    "Published",

    "Option1 Name",
    "Option1 Value",

    "Variant SKU",
    "Variant Price",
    "Variant Inventory Qty",
    "Variant Inventory Policy",
    "Variant Fulfillment Service",
    "Variant Requires Shipping",
    "Variant Taxable",

    "Image Src",
    "Image Position",

    "Status"
]

DEFAULT_VALUES = {
    "Published": "TRUE",
    "Status": "active",
    "Tags": "",
}
