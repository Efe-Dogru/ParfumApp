from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class NoteFamily(Base):
    __tablename__ = "note_families"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    notes = relationship("Note", back_populates="family")

class NoteMood(Base):
    __tablename__ = "note_moods"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    notes = relationship("Note", secondary="note_mood_relations", back_populates="moods")

class NoteMoodRelation(Base):
    __tablename__ = "note_mood_relations"
    
    note_id = Column(Integer, ForeignKey("notes.id"), primary_key=True)
    mood_id = Column(Integer, ForeignKey("note_moods.id"), primary_key=True)

class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    image_filename = Column(String(255))
    description = Column(Text)
    family_id = Column(Integer, ForeignKey("note_families.id"))
    source = Column(String(255))
    cultural_significance = Column(Text)
    normalized_name = Column(String(255), unique=True, nullable=False)

    # Relationships
    family = relationship("NoteFamily", back_populates="notes")
    moods = relationship("NoteMood", secondary="note_mood_relations", back_populates="notes")
    perfume_notes = relationship("PerfumeNote", back_populates="note") 