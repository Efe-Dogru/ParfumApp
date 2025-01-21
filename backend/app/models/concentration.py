from sqlalchemy import Column, Integer, String
from app.db.base_class import Base

class Concentration(Base):
    __tablename__ = "concentration"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False) 