import json
from datetime import datetime
from typing import Dict, List


class ReportGenerator:
    """
    Generates client delivery reports and error logs
    """

    @staticmethod
    def generate_scrape_report(stats: Dict, path: str = "output/scrape_report.txt"):
        """
        stats example:
        {
            "total_urls": 120,
            "fetched_pages": 110,
            "failed_fetch": 10,
            "parsed_products": 95,
            "normalized_products": 95,
            "duplicates_removed": 7,
            "mapped_products": 88,
            "validated_rows": 120,
            "validation_errors": 3,
            "validation_warnings": 5,
            "exported_csv": True,
            "exported_json": True
        }
        """

        now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

        lines = []
        lines.append("SHOPIFY CATALOG SCRAPE REPORT")
        lines.append("=" * 40)
        lines.append(f"Generated: {now}")
        lines.append("")

        lines.append("PIPELINE SUMMARY")
        lines.append("-" * 40)
        lines.append(f"Total input URLs       : {stats.get('total_urls', 0)}")
        lines.append(f"Pages fetched          : {stats.get('fetched_pages', 0)}")
        lines.append(f"Failed fetches         : {stats.get('failed_fetch', 0)}")
        lines.append(f"Products parsed        : {stats.get('parsed_products', 0)}")
        lines.append(f"Products normalized    : {stats.get('normalized_products', 0)}")
        lines.append(f"Duplicates removed     : {stats.get('duplicates_removed', 0)}")
        lines.append(f"Products mapped        : {stats.get('mapped_products', 0)}")
        lines.append(f"Final Shopify rows     : {stats.get('validated_rows', 0)}")
        lines.append("")

        lines.append("VALIDATION")
        lines.append("-" * 40)
        lines.append(f"Validation errors      : {stats.get('validation_errors', 0)}")
        lines.append(f"Validation warnings    : {stats.get('validation_warnings', 0)}")
        lines.append("")

        lines.append("EXPORT STATUS")
        lines.append("-" * 40)
        lines.append(f"CSV Exported           : {stats.get('exported_csv', False)}")
        lines.append(f"JSON Exported          : {stats.get('exported_json', False)}")
        lines.append("")

        lines.append("FILES DELIVERED")
        lines.append("-" * 40)
        lines.append("output/shopify_catalog.csv")
        lines.append("output/catalog.json")
        lines.append("output/error_log.json")
        lines.append("output/scrape_report.txt")
        lines.append("")

        lines.append("SYSTEM STATUS")
        lines.append("-" * 40)
        if stats.get("validation_errors", 0) == 0:
            lines.append("STATUS: SUCCESS ✅")
        else:
            lines.append("STATUS: COMPLETED WITH ERRORS ⚠️")

        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

    @staticmethod
    def generate_error_log(report: Dict, path: str = "output/error_log.json"):
        """
        Stores full validation report for debugging & client transparency
        """
        with open(path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
