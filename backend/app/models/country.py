from sqlalchemy import Column, Integer, String
from app.db.base_class import Base

class Country(Base):
    __tablename__ = "country"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False) 