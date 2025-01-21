from sqlalchemy import Column, Integer, String
from app.db.base_class import Base

class Type(Base):
    __tablename__ = "type"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False) 