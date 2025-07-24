from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
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
