from typing import Dict, List


class ImageMapper:
    """
    Maps product images to Shopify CSV image rows.
    """

    @staticmethod
    def map(handle: str, images: List[str]) -> List[Dict]:
        """
        Returns list of Shopify image rows
        """

        rows = []

        for idx, img in enumerate(images, start=1):
            rows.append({
                "Handle": handle,
                "Image Src": img,
                "Image Position": idx,
                "Image Alt Text": handle.replace("-", " ").title()
            })

        return rows
