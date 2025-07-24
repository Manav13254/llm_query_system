from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from datetime import datetime
import os
from pathlib import Path
from ingestion import pdf_parser, normalizer
from ingestion.utils import compute_sha256
from db.models import Document
from db.session import SessionLocal
from tasks.process_and_embed import process_document

router = APIRouter(prefix="/upload", tags=["Upload"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/pdf")
async def upload_pdf(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(400, detail="Please upload a PDF file.")
    
    temp_dir = Path("tmp")
    temp_dir.mkdir(exist_ok=True)
    temp_path = temp_dir / file.filename

    with open(temp_path, "wb") as buffer:
        buffer.write(await file.read())
    temp_size = os.path.getsize(temp_path)
    if temp_size == 0:
        return {"error": "Uploaded file is empty"}

    try:
        file_hash = compute_sha256(temp_path)
        raw_text = pdf_parser.extract_pdf_text(temp_path)
        if not raw_text:
            return {"error": "PDF parser returned empty text"}
        clean_text = normalizer.normalize_text(raw_text)
        if not clean_text:
            return {"error": "Normalizer returned empty text"}

        existing_doc = db.query(Document).filter(Document.sha256 == file_hash).first()
        if existing_doc:
            return {
                "document_id": existing_doc.id,
                "filename": existing_doc.filename,
                "sha256": existing_doc.sha256,
                "status": existing_doc.status,
                "message": "This document was already uploaded. Not duplicated."
            }

        doc = Document(
            filename=file.filename,
            sha256=file_hash,
            filesize=temp_size,
            mime_type=file.content_type,
            upload_time=datetime.utcnow(),
            status="processed"
        )
        db.add(doc)
        db.commit()
        db.refresh(doc)

        background_tasks.add_task(
            process_document,
            doc.id,
            clean_text,
            {"page": None, "clause_id": None, "source_hash": file_hash}
        )

        return {
            "document_id": doc.id,
            "filename": doc.filename,
            "sha256": doc.sha256,
            "status": doc.status,
            "preview": clean_text[:200],
            "message": "PDF processed and metadata saved. Chunking & embedding started in background."
        }
    except Exception as e:
        return {"error": str(e)}
    finally:
        if os.path.exists(temp_path):
            os.unlink(temp_path)
