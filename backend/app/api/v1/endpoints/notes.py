from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from sqlalchemy.sql import func

from app.db.session import get_db
from app.models.note import Note as NoteModel
from app.schemas.note import NoteCreate, NoteResponse

router = APIRouter()

@router.get("", response_model=List[NoteResponse])
async def get_notes(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """
    Get all notes.
    """
    query = select(NoteModel).offset(skip).limit(limit)
    result = await db.execute(query)
    notes = result.scalars().all()
    return notes

@router.get("/search", response_model=List[NoteResponse])
async def search_notes(
    query: str,
    db: AsyncSession = Depends(get_db),
    limit: int = 100
):
    """
    Search notes by name.
    """
    search_query = f"%{query}%"
    stmt = select(NoteModel).filter(
        or_(
            NoteModel.name.ilike(search_query),
            NoteModel.normalized_name.ilike(search_query)
        )
    ).limit(limit)
    
    result = await db.execute(stmt)
    notes = result.scalars().all()
    return notes

@router.post("", response_model=NoteResponse)
async def create_note(
    note: NoteCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new note.
    """
    # Create normalized name (lowercase version)
    normalized_name = note.name.lower()
    
    # Check if note with this normalized name already exists
    query = select(NoteModel).filter(NoteModel.normalized_name == normalized_name)
    result = await db.execute(query)
    existing_note = result.scalar_one_or_none()
    
    if existing_note:
        raise HTTPException(
            status_code=400,
            detail="Note with this name already exists"
        )
    
    db_note = NoteModel(
        name=note.name,
        normalized_name=normalized_name,
        image_filename=note.image_filename if hasattr(note, 'image_filename') else None
    )
    db.add(db_note)
    try:
        await db.commit()
        await db.refresh(db_note)
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Error creating note"
        )
    return db_note

@router.get("/{note_id}", response_model=NoteResponse)
async def get_note(
    note_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Get a specific note by ID.
    """
    query = select(NoteModel).filter(NoteModel.id == note_id)
    result = await db.execute(query)
    note = result.scalar_one_or_none()
    
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    
    return note

@router.delete("/{note_id}")
async def delete_note(
    note_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Delete a note.
    """
    query = select(NoteModel).filter(NoteModel.id == note_id)
    result = await db.execute(query)
    note = result.scalar_one_or_none()
    
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    
    await db.delete(note)
    await db.commit()
    return {"message": "Note deleted successfully"} 