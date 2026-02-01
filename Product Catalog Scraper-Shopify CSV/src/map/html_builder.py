from typing import Optional
from ..normalize.text_cleaner import TextCleaner


class HTMLBuilder:
    """
    Builds Shopify-safe HTML bodies.
    """

    @staticmethod
    def build(description: Optional[str], features: Optional[list] = None) -> str:
        body = ""

        if description:
            clean_desc = TextCleaner.clean_text(description)
            body += f"<p>{clean_desc}</p>"

        if features:
            body += "<ul>"
            for feat in features:
                feat_clean = TextCleaner.clean_text(feat)
                if feat_clean:
                    body += f"<li>{feat_clean}</li>"
            body += "</ul>"

        return body.strip()
