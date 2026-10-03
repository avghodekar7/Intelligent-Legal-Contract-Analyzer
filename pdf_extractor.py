import fitz
import unicodedata
import re


def clean_extracted_text(text):

    # Normalize Unicode characters
    text = unicodedata.normalize("NFKC", text)

    # Fix common PDF ligatures
    replacements = {
        "ﬁ": "fi",
        "ﬂ": "fl",
        "ﬀ": "ff",
        "ﬃ": "ffi",
        "ﬄ": "ffl",
        "’": "'",
        "“": '"',
        "”": '"',
        "–": "-",
        "—": "-"
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    # Remove unnecessary trailing spaces
    text = re.sub(r"[ \t]+", " ", text)

    # Normalize excessive blank lines
    text = re.sub(r"\n\s*\n+", "\n\n", text)

    return text.strip()


def extract_text_from_pdf(pdf_path):

    text = ""

    document = fitz.open(pdf_path)

    for page in document:

        page_text = page.get_text(
            "text",
            sort=True
        )

        text += page_text + "\n"

    document.close()

    return clean_extracted_text(text)