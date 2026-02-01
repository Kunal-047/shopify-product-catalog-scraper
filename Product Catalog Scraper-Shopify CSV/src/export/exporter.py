from typing import List, Dict

from .csv_exporter import CSVExporter
from .json_exporter import JSONExporter
from .report_generator import ReportGenerator


class Exporter:
    """
    Master export controller
    """

    def __init__(self, output_dir="output"):
        self.output_dir = output_dir

    def export_all(self, rows: List[Dict], validation_report: Dict, stats: Dict):
        results = {
            "csv": False,
            "json": False,
            "report": False,
            "error_log": False
        }

        # CSV
        CSVExporter.export(rows, f"{self.output_dir}/shopify_catalog.csv")
        results["csv"] = True

        # JSON
        JSONExporter.export(rows, f"{self.output_dir}/catalog.json")
        results["json"] = True

        # Reports
        ReportGenerator.generate_scrape_report(stats, f"{self.output_dir}/scrape_report.txt")
        results["report"] = True

        ReportGenerator.generate_error_log(validation_report, f"{self.output_dir}/error_log.json")
        results["error_log"] = True

        return results
