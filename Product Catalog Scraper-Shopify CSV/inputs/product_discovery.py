from __future__ import annotations

import re
import time
import logging
from typing import Iterable, Set, List
from urllib.parse import urljoin, urlparse, urlunparse

import requests
from bs4 import BeautifulSoup

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

REQUEST_TIMEOUT = 15
REQUEST_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0 Safari/537.36"
    )
}

REQUEST_DELAY_SEC = 0.5  # polite crawling
MAX_PAGINATION_PAGES = 50

PRODUCT_URL_HINTS = [
    "/product",
    "/products",
    "/item",
    "/p/",
]

EXCLUDE_URL_PATTERNS = re.compile(
    r"(blog|article|news|review|support|help|faq|contact|about)",
    re.IGNORECASE,
)

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Core Utilities
# ---------------------------------------------------------------------------


def fetch_html(url: str) -> str | None:
    """Fetch HTML content with basic error handling."""
    try:
        resp = requests.get(url, headers=REQUEST_HEADERS, timeout=REQUEST_TIMEOUT)
        if resp.status_code != 200:
            logger.warning(f"Non-200 response ({resp.status_code}): {url}")
            return None
        if "text/html" not in resp.headers.get("Content-Type", ""):
            logger.warning(f"Non-HTML content skipped: {url}")
            return None
        return resp.text
    except requests.RequestException as e:
        logger.warning(f"Request failed: {url} | {e}")
        return None


def canonicalize_url(url: str) -> str:
    """
    Canonicalize URL:
    - Strip fragments
    - Normalize trailing slash
    - Force lowercase hostname
    - Remove query parameters (Pipeline 0 already removed tracking params)
    """
    parsed = urlparse(url)

    parsed = parsed._replace(
        scheme=parsed.scheme.lower(),
        netloc=parsed.netloc.lower(),
        fragment="",
        query="",
    )

    # Normalize trailing slash
    path = parsed.path.rstrip("/")
    parsed = parsed._replace(path=path)

    return urlunparse(parsed)


def looks_like_product_url(url: str) -> bool:
    """
    Conservative filter to discard obvious non-product URLs.
    Does NOT attempt aggressive inference.
    """
    if EXCLUDE_URL_PATTERNS.search(url):
        return False
    return True

# ---------------------------------------------------------------------------
# Product Discovery
# ---------------------------------------------------------------------------


def discover_from_category(category_url: str) -> Set[str]:
    """
    Crawl a category/collection page and extract product URLs.
    Handles simple pagination patterns.
    """
    discovered: Set[str] = set()

    for page_num in range(1, MAX_PAGINATION_PAGES + 1):
        if page_num == 1:
            url = category_url
        else:
            # Generic page-based pagination strategy
            url = f"{category_url}?page={page_num}"

        logger.info(f"Fetching category page: {url}")
        html = fetch_html(url)
        if not html:
            break

        soup = BeautifulSoup(html, "lxml")

        page_links = set()
        for a in soup.select("a[href]"):
            href = a.get("href")
            if not href:
                continue
            abs_url = urljoin(url, href)
            page_links.add(abs_url)

        product_links_on_page = {
            canonicalize_url(link)
            for link in page_links
            if looks_like_product_url(link)
        }

        # Stop pagination if no new URLs are found
        new_links = product_links_on_page - discovered
        if not new_links:
            break

        discovered.update(new_links)
        time.sleep(REQUEST_DELAY_SEC)

    return discovered

# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def resolve_product_urls(
    validated_product_urls: Iterable[str],
    validated_category_urls: Iterable[str],
) -> List[str]:
    """
    Main entry point for Pipeline 1.
    Returns a deduplicated, canonical list of product URLs.
    """

    resolved: Set[str] = set()

    # 1. Direct product URLs
    for url in validated_product_urls:
        canon = canonicalize_url(url)
        if looks_like_product_url(canon):
            resolved.add(canon)

    # 2. Category discovery
    for category_url in validated_category_urls:
        canon_category = canonicalize_url(category_url)
        discovered = discover_from_category(canon_category)
        resolved.update(discovered)

    logger.info(f"Resolved {len(resolved)} unique product URLs")
    return sorted(resolved)


# ---------------------------------------------------------------------------
# Example CLI usage (optional, removable for library-only usage)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # Example placeholders
    validated_product_urls = []
    validated_category_urls = []

    product_urls = resolve_product_urls(
        validated_product_urls,
        validated_category_urls,
    )

    for url in product_urls:
        print(url)
