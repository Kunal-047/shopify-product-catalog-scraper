from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from bs4 import BeautifulSoup
import json
import re


class BaseParser(ABC):
    """
    Abstract base class for all site parsers.
    Provides:
    - common helpers
    - JSON-LD extraction
    - text cleaning
    - schema utilities
    """

    def __init__(self, html: str, url: str):
        self.html = html
        self.url = url
        self.soup = BeautifulSoup(html, "lxml")

    # -----------------------------
    # Abstract contract
    # -----------------------------
    @abstractmethod
    def parse(self) -> Dict:
        pass

    # -----------------------------
    # Helpers
    # -----------------------------

    def _clean_text(self, text: Optional[str]) -> Optional[str]:
        if not text:
            return None
        text = re.sub(r"\s+", " ", text)
        return text.strip()

    def _extract_json_ld(self) -> List[Dict]:
        """
        Extract JSON-LD structured data blocks
        """
        data = []
        scripts = self.soup.find_all("script", type="application/ld+json")

        for script in scripts:
            try:
                content = script.string
                if not content:
                    continue

                parsed = json.loads(content.strip())
                if isinstance(parsed, list):
                    data.extend(parsed)
                else:
                    data.append(parsed)
            except Exception:
                continue

        return data

    def _find_schema_product(self, jsonld_blocks: List[Dict]) -> Optional[Dict]:
        """
        Find Product schema from JSON-LD
        """
        for block in jsonld_blocks:
            if isinstance(block, dict):
                if block.get("@type") == "Product":
                    return block
                if isinstance(block.get("@graph"), list):
                    for item in block["@graph"]:
                        if item.get("@type") == "Product":
                            return item
        return None

    def _safe_float(self, value) -> Optional[float]:
        try:
            if value is None:
                return None
            return float(str(value).replace(",", "").strip())
        except Exception:
            return None

    def _safe_list(self, value) -> List:
        if value is None:
            return []
        if isinstance(value, list):
            return value
        return [value]
