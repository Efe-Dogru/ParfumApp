from sqlalchemy import Column, Integer, String
from app.db.base_class import Base

class Season(Base):
    __tablename__ = "seasons"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False) 