from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Concentration(Base):
    __tablename__ = "concentration"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    
    perfumes = relationship("Perfume", back_populates="concentration") 