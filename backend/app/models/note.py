from sqlalchemy import Column, Integer, String, Text
from app.db.base_class import Base

class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    image_filename = Column(String(255))
    description = Column(Text)
    family = Column(String(255))
    source = Column(String(255))
    cultural_significance = Column(Text)
    mood = Column(String(255))
    normalized_name = Column(String(255), unique=True, nullable=False) 