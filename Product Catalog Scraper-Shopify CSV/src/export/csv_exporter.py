import csv
from typing import List, Dict
from ..map.shopify_schema import SHOPIFY_COLUMNS


class CSVExporter:
    """
    Exports Shopify rows to import-ready CSV
    """

    @staticmethod
    def export(rows: List[Dict], path: str = "output/shopify_catalog.csv"):
        if not rows:
            raise ValueError("No rows provided for CSV export")

        with open(path, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=SHOPIFY_COLUMNS,
                extrasaction="ignore",
                quoting=csv.QUOTE_MINIMAL
            )

            writer.writeheader()

            for row in rows:
                safe_row = {}
                for col in SHOPIFY_COLUMNS:
                    val = row.get(col, "")

                    # CSV safety
                    if isinstance(val, str):
                        val = val.replace("\n", " ").replace("\r", " ").strip()

                    safe_row[col] = val

                writer.writerow(safe_row)
