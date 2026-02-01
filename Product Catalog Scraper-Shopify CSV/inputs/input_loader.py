import os
import yaml
from urllib.parse import urlparse


from pathlib import Path
from typing import List, Dict
import yaml


class InputLoader:
    """
    Loads category URLs, product URLs, and vendor mappings
    from structured text / yaml configuration files.
    """

    def __init__(self, base_path: str | Path = "inputs"):
        self.base_path = Path(base_path)

    # ----------------------------
    # Public API
    # ----------------------------
    def load_category_urls(self, filename: str = "category_urls.txt") -> List[str]:
        return self._load_url_file(filename)

    def load_product_urls(self, filename: str = "product_urls.txt") -> List[str]:
        return self._load_url_file(filename)

    def load_vendor_map(self, filename: str = "vendor_map.yaml") -> Dict[str, str]:
        path = self.base_path / filename
        if not path.exists():
            raise FileNotFoundError(f"Vendor map file not found: {path}")

        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}

        # Normalize keys (domains) to lowercase
        return {str(k).lower(): str(v) for k, v in data.items()}

    # ----------------------------
    # Internal helpers
    # ----------------------------
    def _load_url_file(self, filename: str) -> List[str]:
        path = self.base_path / filename
        if not path.exists():
            raise FileNotFoundError(f"URL file not found: {path}")

        urls: List[str] = []

        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()

                # Skip empty lines
                if not line:
                    continue

                # Skip comments (#) and disabled lines (;)
                if line.startswith("#") or line.startswith(";"):
                    continue

                # Strip inline comments
                if "#" in line:
                    line = line.split("#", 1)[0].strip()

                urls.append(line)

        return urls


# ----------------------------
# Example usage
# ----------------------------
if __name__ == "__main__":
    loader = InputLoader()

    categories = loader.load_category_urls()
    products = loader.load_product_urls()
    vendor_map = loader.load_vendor_map()

    print("Categories:", len(categories))
    print("Products:", len(products))
    print("Vendors:", len(vendor_map))

    print("\nCategories:", categories)
    print("\nProducts:", products)
    print("\nVendors:", vendor_map)
