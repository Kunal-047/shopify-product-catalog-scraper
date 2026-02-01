from typing import List, Dict


class RequiredFieldsValidator:
    """
    Validates presence of required Shopify fields.
    """

    REQUIRED_FIELDS = [
        "Handle",
        "Title",
        "Variant SKU",
        "Variant Price"
    ]

    @staticmethod
    def validate(rows: List[Dict]) -> Dict:
        report = {
            "valid": True,
            "errors": []
        }

        for idx, row in enumerate(rows):
            for field in RequiredFieldsValidator.REQUIRED_FIELDS:
                value = row.get(field)

                if value is None or value == "":
                    report["valid"] = False
                    report["errors"].append({
                        "row": idx,
                        "field": field,
                        "error": "Missing required field"
                    })

            # Handle-specific rules
            handle = row.get("Handle")
            if handle and " " in handle:
                report["valid"] = False
                report["errors"].append({
                    "row": idx,
                    "field": "Handle",
                    "error": "Handle contains spaces (invalid Shopify handle)"
                })

        return report
