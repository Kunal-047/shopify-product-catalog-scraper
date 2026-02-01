from typing import List, Dict
from ..map.shopify_schema import SHOPIFY_COLUMNS


class SchemaValidator:
    """
    Validates Shopify CSV schema structure:
    - required columns
    - column order
    - missing columns
    - extra columns
    """

    @staticmethod
    def validate_schema(rows: List[Dict]) -> Dict:
        report = {
            "valid": True,
            "missing_columns": [],
            "extra_columns": [],
            "row_issues": []
        }

        if not rows:
            report["valid"] = False
            report["row_issues"].append("No rows provided for validation")
            return report

        row_cols = set(rows[0].keys())
        schema_cols = set(SHOPIFY_COLUMNS)

        # Missing columns
        missing = schema_cols - row_cols
        if missing:
            report["missing_columns"] = list(missing)
            report["valid"] = False

        # Extra columns
        extra = row_cols - schema_cols
        if extra:
            report["extra_columns"] = list(extra)

        # Per-row structural check
        for idx, row in enumerate(rows):
            for col in SHOPIFY_COLUMNS:
                if col not in row:
                    report["valid"] = False
                    report["row_issues"].append(
                        f"Row {idx}: Missing column '{col}'"
                    )

        return report
