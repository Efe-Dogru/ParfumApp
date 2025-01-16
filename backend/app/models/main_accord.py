from sqlalchemy import Column, Integer, String
from app.db.base_class import Base

class MainAccord(Base):
    __tablename__ = "main_accords"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False) 