import pdfplumber

def extract_pdf_text(file_path: str) -> str:
    """Extracts all text from a PDF file."""
    all_text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                all_text += text + "\n"
    return all_text
