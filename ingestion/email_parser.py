import mailparser

def extract_email_text(file_path: str) -> str:
    """Extracts text body from an email file (.eml, .msg)."""
    mail = mailparser.parse_from_file(file_path)
    return mail.body or ""
