from sqlalchemy import Column, Integer, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from app.models.note import NoteType

class PerfumeNote(Base):
    __tablename__ = "perfume_notes"

    id = Column(Integer, primary_key=True, index=True)
    perfume_id = Column(Integer, ForeignKey("perfumes.id", ondelete="CASCADE"))
    note_id = Column(Integer, ForeignKey("notes.id", ondelete="CASCADE"))
    note_type = Column(Enum(NoteType), nullable=False)

    # Relationships
    perfume = relationship("Perfume", back_populates="notes")
    note = relationship("Note", back_populates="perfumes") 