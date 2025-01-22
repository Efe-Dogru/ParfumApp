from sqlalchemy import Column, Integer, String
from app.db.base_class import Base

class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    normalized_name = Column(String(255), unique=True, nullable=False)
    image_filename = Column(String(255)) 