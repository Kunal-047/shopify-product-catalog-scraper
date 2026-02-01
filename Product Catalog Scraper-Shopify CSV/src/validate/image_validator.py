import re
from typing import List, Dict
from urllib.parse import urlparse


class ImageValidator:
    """
    Validates Shopify image fields.
    """

    IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".webp")

    @staticmethod
    def is_valid_url(url: str) -> bool:
        try:
            parsed = urlparse(url)
            return parsed.scheme in ["http", "https"] and parsed.netloc != ""
        except:
            return False

    @staticmethod
    def validate(rows: List[Dict]) -> Dict:
        report = {
            "valid": True,
            "errors": [],
            "warnings": []
        }

        seen_images = set()

        for idx, row in enumerate(rows):
            img = row.get("Image Src", "").strip()

            if not img:
                continue  # images optional per row

            # URL format
            if not ImageValidator.is_valid_url(img):
                report["valid"] = False
                report["errors"].append({
                    "row": idx,
                    "field": "Image Src",
                    "error": "Invalid URL format"
                })
                continue

            # HTTPS enforcement
            if not img.startswith("https://"):
                report["warnings"].append({
                    "row": idx,
                    "field": "Image Src",
                    "warning": "Image not using HTTPS"
                })

            # Extension check
            if not img.lower().endswith(ImageValidator.IMAGE_EXTENSIONS):
                report["warnings"].append({
                    "row": idx,
                    "field": "Image Src",
                    "warning": "Non-standard image extension"
                })

            # Duplicate image detection
            if img in seen_images:
                report["warnings"].append({
                    "row": idx,
                    "field": "Image Src",
                    "warning": "Duplicate image URL"
                })
            else:
                seen_images.add(img)

        return report
