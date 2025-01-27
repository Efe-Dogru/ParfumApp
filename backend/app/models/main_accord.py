from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class MainAccord(Base):
    __tablename__ = "main_accords"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    
    perfumes = relationship("Perfume", secondary="perfume_main_accords", back_populates="main_accords") 