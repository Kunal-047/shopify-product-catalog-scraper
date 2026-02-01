import json
from typing import List, Dict


class JSONExporter:
    """
    Exports structured catalog JSON
    """

    @staticmethod
    def export(rows: List[Dict], path: str = "output/catalog.json"):
        if not rows:
            raise ValueError("No rows provided for JSON export")

        with open(path, "w", encoding="utf-8") as f:
            json.dump(rows, f, indent=2, ensure_ascii=False)
