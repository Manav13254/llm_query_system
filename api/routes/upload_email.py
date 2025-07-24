from fastapi import APIRouter, UploadFile, File, HTTPException
from ingestion import email_parser, normalizer
import os

router = APIRouter(prefix="/upload", tags=["Upload"])

@router.post("/email")
async def upload_email(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(('.eml', '.msg')):
        raise HTTPException(400, detail="Please upload an email file (.eml or .msg).")
    temp_path = f"tmp/{file.filename}"
    with open(temp_path, "wb") as buffer:
        buffer.write(await file.read())
    try:
        raw_text = email_parser.extract_email_text(temp_path)
        clean_text = normalizer.normalize_text(raw_text)
    finally:
        os.unlink(temp_path)
    return {
        "filename": file.filename,
        "chars": len(clean_text),
        "preview": clean_text[:200],
        "message": "Email processed and text extracted."
    }
