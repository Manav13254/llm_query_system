from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import BigInteger
from datetime import datetime

Base = declarative_base()

class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    sha256 = Column(String, unique=True, nullable=False)
    filesize = Column(Integer)
    mime_type = Column(String)
    upload_time = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="pending") # e.g., pending, processed, failed
    chunks = relationship("DocumentChunk", back_populates="document")


class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id = Column(Integer, primary_key=True, index=True)
    doc_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    chunk_index = Column(Integer, nullable=False)
    token_start = Column(Integer, nullable=False)
    token_end = Column(Integer, nullable=False)

    page = Column(Integer, nullable=True)
    clause_id = Column(String, nullable=True)
    source_hash = Column(String, nullable=True)

    text = Column(String, nullable=False)

    embedded = Column(Boolean, default=False)

    document = relationship("Document", back_populates="chunks")