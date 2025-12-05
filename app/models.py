from datetime import datetime
from sqlalchemy import  Column, Integer, String, DateTime, BigInteger, Text
from app.core import Base


class FileRecord(Base):
    __tablename__ = "files"
    
    id = Column(Integer, primary_key=True, index=True)
    original_name = Column(String, nullable=False)
    version = Column(Integer, default=1)
    path = Column(String, nullable=False)
    file_size = Column(BigInteger)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    uploaded_by = Column(Integer, default=1)


class AnalysisRecord(Base):
    __tablename__ = "analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    file_id = Column(Integer, nullable=False)
    analysis_result = Column(Text)
    analyzed_at = Column(DateTime, default=datetime.utcnow)