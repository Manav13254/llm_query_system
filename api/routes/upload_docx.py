from fastapi import APIRouter, UploadFile, File, HTTPException
from ingestion import docx_parser, normalizer
import os

router = APIRouter(prefix="/upload", tags=["Upload"])

@router.post("/docx")
async def upload_docx(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(('.docx', '.doc')):
        raise HTTPException(400, detail="Please upload a DOCX file.")
    temp_path = f"tmp/{file.filename}"
    with open(temp_path, "wb") as buffer:
        buffer.write(await file.read())
    try:
        raw_text = docx_parser.extract_docx_text(temp_path)
        clean_text = normalizer.normalize_text(raw_text)
    finally:
        os.unlink(temp_path)
    return {
        "filename": file.filename,
        "chars": len(clean_text),
        "preview": clean_text[:200],
        "message": "DOCX processed and text extracted."
    }
