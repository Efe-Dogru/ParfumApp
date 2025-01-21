from sqlalchemy import Column, Integer, String
from app.db.base_class import Base

class Perfumer(Base):
    __tablename__ = "perfumer"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False) 