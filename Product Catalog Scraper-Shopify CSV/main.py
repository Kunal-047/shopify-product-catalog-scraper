from inputs.input_loader import InputLoader
from src.fetch.fetcher import Fetcher
from datetime import datetime
from src.parse.parser_router import ParserRouter
from src.normalize.normalizer import Normalizer
from src.dedup.deduplicator import Deduplicator
from src.map.mapper import ShopifyMapper
from src.validate.validator import Validator
from src.export.exporter import Exporter

stats = {
    "start_time": datetime.utcnow().isoformat(),
    "total_urls": 0,
    "fetched_pages": 0,
    "failed_fetch": 0,
    "parsed_products": 0,
    "normalized_products": 0,
    "duplicates_removed": 0,
    "mapped_products": 0,
    "validated_rows": 0,
    "validation_errors": 0,
    "validation_warnings": 0,
    "exported_csv": False,
    "exported_json": False
}

# 
inputs = InputLoader()
products = inputs.load_product_urls()

fetcher = Fetcher()
raw_pages = fetcher.fetch_urls(products)
# 
from src.parse.parser_router import ParserRouter

parser = ParserRouter()
parsed_data = parser.parse_pages(raw_pages)
# 
from src.normalize.normalizer import Normalizer

normalizer = Normalizer()
normalized_data = normalizer.normalize(parsed_data)
# 
from src.dedup.deduplicator import Deduplicator

deduplicator = Deduplicator()
unique_products = deduplicator.deduplicate(normalized_data)
# 
from src.map.mapper import ShopifyMapper

mapper = ShopifyMapper()
shopify_rows = mapper.map(unique_products)
# 
from src.validate.validator import Validator
validator = Validator()
validated_rows, report = validator.validate(shopify_rows)
validator.save_report(report)
# 
stats["total_urls"] = len(products)
stats["fetched_pages"] = len([p for p in raw_pages if p["status"] == 200])
stats["failed_fetch"] = len([p for p in raw_pages if p["status"] != 200])
stats["parsed_products"] = len(parsed_data)
stats["normalized_products"] = len(normalized_data)
stats["duplicates_removed"] = len(normalized_data) - len(unique_products)
stats["mapped_products"] = len(unique_products)
stats["validated_rows"] = len(validated_rows)
stats["validation_errors"] = report["summary"]["errors"]
stats["validation_warnings"] = report["summary"]["warnings"]
# 
from src.export.exporter import Exporter
exporter = Exporter("output")
export_results = exporter.export_all(validated_rows, report, stats)

stats["exported_csv"] = export_results["csv"]
stats["exported_json"] = export_results["json"]
stats["end_time"] = datetime.utcnow().isoformat()
# 
print("Total URLs: "+str(stats["total_urls"]))
print("Fetched Pages: "+str(stats["fetched_pages"]))
print("Failed Fetch: "+str(stats["failed_fetch"]))
print("Parsed Products: "+str(stats["parsed_products"]))
print("Normalized Products: "+str(stats["normalized_products"]))
print("Duplicates Removed: "+str(stats["duplicates_removed"]))
print("Mapped Products: "+str(stats["mapped_products"]))
print("Validated Rows: "+str(stats["validated_rows"]))
print("Validation Errors: "+str(stats["validation_errors"]))
print("Validation Warnings: "+str(stats["validation_warnings"]))
print("Exported CSV: "+str(stats["exported_csv"]))
print("Exported JSON: "+str(stats["exported_json"]))
print("Start Time: "+str(stats["start_time"]))
print("End Time: "+str(stats["end_time"]))
# 
