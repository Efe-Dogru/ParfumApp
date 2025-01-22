from sqlalchemy import Column, Integer, String, Text, ForeignKey, Table, ARRAY, JSON, Enum
from sqlalchemy.orm import relationship
from app.db.base_class import Base

perfume_main_accords = Table(
    'perfume_main_accords',
    Base.metadata,
    Column('perfume_id', Integer, ForeignKey('perfumes.id'), primary_key=True),
    Column('accord_id', Integer, ForeignKey('main_accords.id'), primary_key=True)
)

class PerfumeNote(Base):
    __tablename__ = "perfume_notes"

    perfume_id = Column(Integer, ForeignKey('perfumes.id'), primary_key=True)
    note_id = Column(Integer, ForeignKey('notes.id'), primary_key=True)
    note_type = Column(Enum('top', 'middle', 'base', name='note_type'), primary_key=True)

    note = relationship("Note")

class Perfume(Base):
    __tablename__ = "perfumes"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    brand_id = Column(Integer, ForeignKey('brands.id'))
    concentration_id = Column(Integer, ForeignKey('concentration.id'))
    local_image_path = Column(String(255))
    gender = Column(String(50))
    type_id = Column(Integer, ForeignKey('type.id'))
    family_id = Column(Integer, ForeignKey('family.id'))
    release_year = Column(Integer)
    country_id = Column(Integer, ForeignKey('country.id'))
    description = Column(Text)
    longevity = Column(String(255))
    sillage = Column(String(255))
    occasion = Column(ARRAY(String))
    season = Column(ARRAY(String))
    perfumer_id = Column(Integer, ForeignKey('perfumer.id'))
    inspiration = Column(Text)
    istrend = Column(JSON)

    # Relationships
    brand = relationship("Brand")
    concentration = relationship("Concentration")
    type = relationship("Type")
    family = relationship("Family")
    country = relationship("Country")
    perfumer = relationship("Perfumer")
    notes = relationship("PerfumeNote")
    main_accords = relationship("MainAccord", secondary=perfume_main_accords) 