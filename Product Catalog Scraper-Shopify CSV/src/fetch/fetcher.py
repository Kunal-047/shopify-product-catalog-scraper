import time
from datetime import datetime
from urllib.parse import urlparse
from typing import List, Dict

from src.fetch.http_client import HTTPClient
from src.fetch.session_manager import SessionManager
from src.fetch.retry import RetryHandler


class Fetcher:
    """
    Orchestrates:
    - input URLs
    - session management
    - HTTP client
    - retry handling
    - raw page output formatting
    """

    def __init__(
        self,
        timeout: int = 15,
        max_retries: int = 3,
        base_delay: float = 1.0,
        max_delay: float = 15.0,
    ):
        self.http_client = HTTPClient(timeout=timeout)
        self.session_manager = SessionManager()
        self.retry_handler = RetryHandler(
            max_retries=max_retries,
            base_delay=base_delay,
            max_delay=max_delay,
        )

    def _get_domain(self, url: str) -> str:
        return urlparse(url).netloc.replace("www.", "")

    def fetch_urls(self, urls: List[str]) -> List[Dict]:
        raw_pages = []

        for url in urls:
            domain = self._get_domain(url)
            session = self.session_manager.get_session(domain)

            try:
                response = self.retry_handler.run(
                    self.http_client.get,
                    url,
                    session=session
                )

                raw_pages.append({
                    "url": url,
                    "html": response.text,
                    "status": response.status_code,
                    "timestamp": datetime.utcnow().isoformat()
                })

            except Exception as e:
                raw_pages.append({
                    "url": url,
                    "html": None,
                    "status": "error",
                    "error": str(e),
                    "timestamp": datetime.utcnow().isoformat()
                })

            # polite crawling delay
            time.sleep(0.5)

        return raw_pages

    def shutdown(self):
        self.session_manager.close_all()

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

urls = ['https://www.amazon.in/OnePlus-15R-Snapdragon%C2%AE-Personalised-Game-changing/dp/B0FZT1D63F/ref=sr_1_1_sspa?dib=eyJ2IjoiMSJ9.WgfR5wZxVWLfDlOLJfW12NupS-IkUjs93t4PfMC28eXeQBDO2VZrE3qU4fOAK7pOQ9k3ZcjqHLIYiJWvlkjsF9yBmNH9ZWzAoWoBUY4wVobDwveQ-s2cGuta1eRxntzMIRh1iw5oWo5U-pTG2-vzQpzCHHvjZsSahadi2TIvenUzRbgu9SSakQWgoEud26SgZzGKBLiRE8eSMvjTzn_xH8P4OKQmA8hNr19I8WDF0to.GRdzGlMyuCNCHKh7CYI6KznXCGBOllLusO5sQhnjWgk&dib_tag=se&keywords=smartphone&qid=1769616374&sr=8-1-spons&aref=RE8VEh6UYM&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&psc=1', 'https://www.flipkart.com/motorola-g06-power-pantone-tendril-64-gb/p/itm042f1f6d04b3a?pid=MOBHFSCEDQXXDXUQ&lid=LSTMOBHFSCEDQXXDXUQ5OORZ3&marketplace=FLIPKART&store=tyy%2F4io&srno=b_1_4&otracker=browse&fm=organic&iid=f0b56565-ab8c-409e-b208-2563f0576b71.MOBHFSCEDQXXDXUQ.SEARCH&ppt=None&ppn=None&ssid=7px9fgvvjk0000001769616185717', 'https://www.myntra.com/shirts/hancock/hancock-men-black-slim-fit-formal-shirt/1849875/buy', 'https://www.ajio.com/the-bear-house-men-checked-slim-fit-shirt-with-patch-pocket/p/463633516_grey?']
if __name__ == "__main__":
    fetcher = Fetcher()
    raw_pages = fetcher.fetch_urls(urls)
    print(raw_pages)