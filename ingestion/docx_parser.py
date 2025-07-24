from docx import Document

def extract_docx_text(file_path: str) -> str:
    """Extracts all text from a DOCX file."""
    doc = Document(file_path)
    texts = [para.text for para in doc.paragraphs if para.text]
    return "\n".join(texts)
