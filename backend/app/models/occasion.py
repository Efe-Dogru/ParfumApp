from sqlalchemy import Column, Integer, String
from app.db.base_class import Base

class Occasion(Base):
    __tablename__ = "occasions"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False) 