from urllib.parse import urlparse

from .amazon_parser import AmazonParser
from .shopify_parser import ShopifyParser
from .generic_parser import GenericParser


class ParserRouter:
    """
    Detects site type and routes HTML to correct parser.
    """

    def __init__(self):
        pass

    def _get_domain(self, url: str) -> str:
        return urlparse(url).netloc.replace("www.", "")

    def _is_amazon(self, domain: str) -> bool:
        return "amazon." in domain

    def _is_shopify(self, html: str) -> bool:
        """
        Shopify detection heuristics:
        - Shopify CDN
        - Shopify globals
        - Shopify product JSON
        """
        indicators = [
            "cdn.shopify.com",
            "Shopify.theme",
            "Shopify.shop",
            "ShopifyAnalytics",
            "id=\"ProductJson\"",
            "var meta = Shopify"
        ]
        return any(indicator in html for indicator in indicators)

    def route(self, html: str, url: str):
        domain = self._get_domain(url)

        # Amazon
        if self._is_amazon(domain):
            return AmazonParser(html, url)

        # Shopify
        if self._is_shopify(html):
            return ShopifyParser(html, url)

        # Fallback
        return GenericParser(html, url)

    def parse(self, html: str, url: str) -> dict:
        """
        High-level API:
        input: raw html + url
        output: structured product dict
        """
        parser = self.route(html, url)
        return parser.parse()

    def parse_pages(self, raw_pages: list[dict]) -> list[dict]:
        """
        Parse multiple raw pages.
        """
        parsed_data = []
        for page in raw_pages:
            parsed_data.append(self.parse(page["html"], page["url"]))
        return parsed_data
