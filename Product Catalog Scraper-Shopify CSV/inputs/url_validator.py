from urllib.parse import urlparse, urlunparse, parse_qsl, urlencode
import re

TRACKING_PARAM_PREFIXES = (
    "utm_",
)

TRACKING_PARAM_EXACT = {
    "ref",
    "fbclid",
    "gclid",
    "yclid",
}


# -----------------------------
# Core helpers
# -----------------------------

def is_valid_url(url: str) -> bool:
    """Basic URL validation (scheme + netloc)."""
    try:
        parsed = urlparse(url)
        return parsed.scheme in {"http", "https"} and bool(parsed.netloc)
    except Exception:
        return False


def normalize_url(url: str) -> str | None:
    """
    Normalize a URL by:
    - forcing https
    - stripping fragments
    - removing tracking query params
    - normalizing trailing slash
    """
    url = url.strip()
    if not url:
        return None

    # If scheme missing, assume https
    if not re.match(r"^https?://", url):
        url = "https://" + url

    if not is_valid_url(url):
        return None

    parsed = urlparse(url)

    # Force https
    scheme = "https"

    # Clean query params
    clean_params = []
    for key, value in parse_qsl(parsed.query, keep_blank_values=True):
        if key.lower().startswith(TRACKING_PARAM_PREFIXES):
            continue
        if key.lower() in TRACKING_PARAM_EXACT:
            continue
        clean_params.append((key, value))

    query = urlencode(clean_params, doseq=True)

    # Normalize path (remove trailing slash except root)
    path = parsed.path or "/"
    if path != "/" and path.endswith("/"):
        path = path[:-1]

    normalized = urlunparse(
        (
            scheme,
            parsed.netloc.lower(),
            path,
            "",        # params (unused)
            query,
            "",        # fragment removed
        )
    )

    return normalized


# -----------------------------
# Public API
# -----------------------------

def load_and_validate(product_file: str, category_file: str):
    """
    Load URLs from text files, normalize, validate, and deduplicate.

    Returns:
        validated_product_urls (list[str])
        validated_category_urls (list[str])
    """

    def read_lines(path: str) -> list[str]:
        try:
            with open(path, "r", encoding="utf-8") as f:
                return [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            return []

    raw_product_urls = read_lines(product_file)
    raw_category_urls = read_lines(category_file)

    normalized_product_urls = []
    normalized_category_urls = []

    seen = set()

    for url in raw_product_urls:
        normalized = normalize_url(url)
        if not normalized:
            continue
        if normalized in seen:
            continue
        seen.add(normalized)
        normalized_product_urls.append(normalized)

    for url in raw_category_urls:
        normalized = normalize_url(url)
        if not normalized:
            continue
        if normalized in seen:
            continue
        seen.add(normalized)
        normalized_category_urls.append(normalized)

    return normalized_product_urls, normalized_category_urls


# -----------------------------
# CLI / debug usage
# -----------------------------

if __name__ == "__main__":
    products, categories = load_and_validate(
        "inputs/product_urls.txt",
        "inputs/category_urls.txt",
    )

    print(f"Validated product URLs: {len(products)}")
    for u in products:
        print(u)

    print(f"\nValidated category URLs: {len(categories)}")
    for u in categories:
        print(u)
