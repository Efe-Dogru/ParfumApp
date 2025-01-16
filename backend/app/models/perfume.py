from sqlalchemy import Column, Integer, String, Text, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.db.base_class import Base

# Junction tables
perfume_top_notes = Table(
    'perfume_top_notes',
    Base.metadata,
    Column('perfume_id', Integer, ForeignKey('perfumes.id'), primary_key=True),
    Column('note_id', Integer, ForeignKey('notes.id'), primary_key=True)
)

perfume_middle_notes = Table(
    'perfume_middle_notes',
    Base.metadata,
    Column('perfume_id', Integer, ForeignKey('perfumes.id'), primary_key=True),
    Column('note_id', Integer, ForeignKey('notes.id'), primary_key=True)
)

perfume_base_notes = Table(
    'perfume_base_notes',
    Base.metadata,
    Column('perfume_id', Integer, ForeignKey('perfumes.id'), primary_key=True),
    Column('note_id', Integer, ForeignKey('notes.id'), primary_key=True)
)

perfume_main_accords = Table(
    'perfume_main_accords',
    Base.metadata,
    Column('perfume_id', Integer, ForeignKey('perfumes.id'), primary_key=True),
    Column('accord_id', Integer, ForeignKey('main_accords.id'), primary_key=True)
)

perfume_occasions = Table(
    'perfume_occasions',
    Base.metadata,
    Column('perfume_id', Integer, ForeignKey('perfumes.id'), primary_key=True),
    Column('occasion_id', Integer, ForeignKey('occasions.id'), primary_key=True)
)

perfume_seasons = Table(
    'perfume_seasons',
    Base.metadata,
    Column('perfume_id', Integer, ForeignKey('perfumes.id'), primary_key=True),
    Column('season_id', Integer, ForeignKey('seasons.id'), primary_key=True)
)

class Perfume(Base):
    __tablename__ = "perfumes"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    brand = Column(String(255), nullable=False)
    type = Column(String(50))
    gender = Column(String(50))
    family = Column(String(100))
    release_year = Column(Integer)
    concentration = Column(String(50))
    description = Column(Text)
    longevity = Column(String(50))
    sillage = Column(String(50))
    image_url = Column(Text)
    perfumer = Column(String(255))
    inspiration = Column(Text)

    # Relationships
    top_notes = relationship("Note", secondary=perfume_top_notes, backref="perfumes_as_top")
    middle_notes = relationship("Note", secondary=perfume_middle_notes, backref="perfumes_as_middle")
    base_notes = relationship("Note", secondary=perfume_base_notes, backref="perfumes_as_base")
    main_accords = relationship("MainAccord", secondary=perfume_main_accords, backref="perfumes")
    occasions = relationship("Occasion", secondary=perfume_occasions, backref="perfumes")
    seasons = relationship("Season", secondary=perfume_seasons, backref="perfumes") 