import re

def normalize_text(text: str) -> str:
    """Normalizes whitespace, removes invisible characters, preserves paragraphs."""
    # Remove zero-width spaces, soft hyphens, etc.
    text = re.sub(r"[\u200B-\u200D\uFEFF]", "", text)
    text = re.sub(r" {2,}", " ", text)                 # Multiple spaces -> 1
    text = re.sub(r"\n{3,}", "\n\n", text)             # Many newlines -> 2
    text = "\n".join([line.strip() for line in text.splitlines()])
    return text
