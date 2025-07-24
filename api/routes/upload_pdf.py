from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime
import os
from pathlib import Path
from ingestion import pdf_parser, normalizer
from ingestion.utils import compute_sha256
from db.models import Document
from db.session import SessionLocal, engine

router = APIRouter(prefix="/upload", tags=["Upload"])

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/pdf")
async def upload_pdf(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(400, detail="Please upload a PDF file.")
    
    temp_dir = Path("tmp")
    temp_dir.mkdir(exist_ok=True)
    temp_path = temp_dir / file.filename

    # Save upload temporarily
    with open(temp_path, "wb") as buffer:
        buffer.write(await file.read())
    
    try:
        # Compute hash
        file_hash = compute_sha256(temp_path)
        # Extract and clean text
        raw_text = pdf_parser.extract_pdf_text(temp_path)
        clean_text = normalizer.normalize_text(raw_text)
        # Prepare metadata
        doc = Document(
            filename=file.filename,
            sha256=file_hash,
            filesize=os.path.getsize(temp_path),
            mime_type=file.content_type,
            upload_time=datetime.utcnow(),
            status="processed"
        )
        db.add(doc)
        db.commit()
        db.refresh(doc)
    finally:
        os.unlink(temp_path)

    return {
        "document_id": doc.id,
        "filename": doc.filename,
        "sha256": doc.sha256,
        "status": doc.status,
        "preview": clean_text[:200],
        "message": "PDF processed, extracted, and metadata saved."
    }
