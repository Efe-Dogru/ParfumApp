from sqlalchemy import Column, Integer, String
from app.db.base_class import Base

class TopNote(Base):
    __tablename__ = "top_notes"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)

class MiddleNote(Base):
    __tablename__ = "middle_notes"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)

class BaseNote(Base):
    __tablename__ = "base_notes"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False) 