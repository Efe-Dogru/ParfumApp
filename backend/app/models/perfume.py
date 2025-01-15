from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from app.db.base_class import Base

class Perfume(Base):
    __tablename__ = "perfumes"

    id = Column(Integer, primary_key=True, index=True)
    brand = Column(Text)
    brand_line = Column(Text)
    name = Column(Text)
    image_url = Column(Text)
    geurnoot = Column(Text)
    topnoot = Column(Text)
    hartnoot = Column(Text)
    basisnoot = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow) 