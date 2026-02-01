import json
from typing import List, Dict

from .schema_validator import SchemaValidator
from .required_fields import RequiredFieldsValidator
from .image_validator import ImageValidator


class Validator:
    """
    Orchestrates full validation pipeline:
    Shopify rows → validated_rows + error_report.json
    """

    def validate(self, rows: List[Dict]):
        full_report = {
            "valid": True,
            "schema": {},
            "required_fields": {},
            "images": {},
            "summary": {
                "total_rows": len(rows),
                "errors": 0,
                "warnings": 0
            }
        }

        # -----------------------------
        # Schema validation
        # -----------------------------
        schema_report = SchemaValidator.validate_schema(rows)
        full_report["schema"] = schema_report
        if not schema_report.get("valid"):
            full_report["valid"] = False

        # -----------------------------
        # Required fields validation
        # -----------------------------
        required_report = RequiredFieldsValidator.validate(rows)
        full_report["required_fields"] = required_report
        if not required_report.get("valid"):
            full_report["valid"] = False
            full_report["summary"]["errors"] += len(required_report.get("errors", []))

        # -----------------------------
        # Image validation
        # -----------------------------
        image_report = ImageValidator.validate(rows)
        full_report["images"] = image_report
        if not image_report.get("valid"):
            full_report["valid"] = False
            full_report["summary"]["errors"] += len(image_report.get("errors", []))
        full_report["summary"]["warnings"] += len(image_report.get("warnings", []))

        return rows, full_report

    @staticmethod
    def save_report(report: Dict, path: str = "output/error_report.json"):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)
