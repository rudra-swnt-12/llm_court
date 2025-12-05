from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime
from sqlalchemy.sql import func
from pgvector.sqlalchemy import Vector
from app.db.base import Base

class Case(Base):
    __tablename__ = "cases"

    id = Column(Integer, primary_key=True, index=True)
    query = Column(Text, nullable=False)
    status = Column(String, default="pending")  # pending, closed
    
    # The Verdict
    verdict = Column(Text, nullable=True)
    solution = Column(Text, nullable=True)
    is_guilty = Column(Boolean, default=False)

    # Memory
    embedding = Column(Vector(384))
    
    # Metadata
    rounds = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())