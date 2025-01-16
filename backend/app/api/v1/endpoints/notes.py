from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.models.note import Note
from app.schemas.note import NoteCreate, NoteResponse

router = APIRouter()

@router.get("/", response_model=List[NoteResponse])
async def get_notes(
    db: AsyncSession = Depends(get_db)
):
    """
    Get all notes.
    """
    query = select(Note)
    result = await db.execute(query)
    notes = result.scalars().all()
    return notes

@router.post("/", response_model=NoteResponse)
async def create_note(
    note: NoteCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new note.
    """
    db_note = Note(name=note.name)
    db.add(db_note)
    try:
        await db.commit()
        await db.refresh(db_note)
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Note with this name already exists"
        )
    return db_note

@router.delete("/{note_id}")
async def delete_note(
    note_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Delete a note.
    """
    query = select(Note).filter(Note.id == note_id)
    result = await db.execute(query)
    note = result.scalar_one_or_none()
    
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    
    await db.delete(note)
    await db.commit()
    return {"message": "Note deleted successfully"} 