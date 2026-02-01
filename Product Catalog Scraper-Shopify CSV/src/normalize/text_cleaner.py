import re
from bs4 import BeautifulSoup


class TextCleaner:
    """
    Handles:
    - HTML cleaning
    - text normalization
    - whitespace normalization
    - encoding cleanup
    - emoji removal
    - Shopify-safe text
    """

    @staticmethod
    def clean_html(html: str) -> str:
        if not html:
            return ""

        soup = BeautifulSoup(html, "lxml")

        # Remove scripts and styles
        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()

        text = soup.get_text(separator=" ")

        return TextCleaner.clean_text(text)

    @staticmethod
    def clean_text(text: str) -> str:
        if not text:
            return ""

        # Normalize whitespace
        text = re.sub(r"\s+", " ", text)

        # Remove weird unicode chars
        text = re.sub(r"[\u200b-\u200f\u202a-\u202e]", "", text)

        # Remove emojis (safe generic range)
        emoji_pattern = re.compile(
            "["
            u"\U0001F600-\U0001F64F"
            u"\U0001F300-\U0001F5FF"
            u"\U0001F680-\U0001F6FF"
            u"\U0001F700-\U0001F77F"
            u"\U0001F780-\U0001F7FF"
            u"\U0001F800-\U0001F8FF"
            u"\U0001F900-\U0001F9FF"
            u"\U0001FA00-\U0001FAFF"
            "]+",
            flags=re.UNICODE
        )
        text = emoji_pattern.sub("", text)

        return text.strip()
