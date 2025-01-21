from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.models.note import TopNote as TopNoteModel, MiddleNote as MiddleNoteModel, BaseNote as BaseNoteModel
from app.schemas.note import NoteCreate, TopNote, MiddleNote, BaseNote

router = APIRouter()

# Top Notes
@router.get("/top", response_model=List[TopNote])
async def get_top_notes(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """
    Get all top notes.
    """
    query = select(TopNoteModel).offset(skip).limit(limit)
    result = await db.execute(query)
    notes = result.scalars().all()
    return notes

@router.post("/top", response_model=TopNote)
async def create_top_note(
    note: NoteCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new top note.
    """
    db_note = TopNoteModel(name=note.name)
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

# Middle Notes
@router.get("/middle", response_model=List[MiddleNote])
async def get_middle_notes(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """
    Get all middle notes.
    """
    query = select(MiddleNoteModel).offset(skip).limit(limit)
    result = await db.execute(query)
    notes = result.scalars().all()
    return notes

@router.post("/middle", response_model=MiddleNote)
async def create_middle_note(
    note: NoteCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new middle note.
    """
    db_note = MiddleNoteModel(name=note.name)
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

# Base Notes
@router.get("/base", response_model=List[BaseNote])
async def get_base_notes(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """
    Get all base notes.
    """
    query = select(BaseNoteModel).offset(skip).limit(limit)
    result = await db.execute(query)
    notes = result.scalars().all()
    return notes

@router.post("/base", response_model=BaseNote)
async def create_base_note(
    note: NoteCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new base note.
    """
    db_note = BaseNoteModel(name=note.name)
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

# Delete endpoints
@router.delete("/top/{note_id}")
async def delete_top_note(
    note_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Delete a top note.
    """
    query = select(TopNoteModel).filter(TopNoteModel.id == note_id)
    result = await db.execute(query)
    note = result.scalar_one_or_none()
    
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    
    await db.delete(note)
    await db.commit()
    return {"message": "Note deleted successfully"}

@router.delete("/middle/{note_id}")
async def delete_middle_note(
    note_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Delete a middle note.
    """
    query = select(MiddleNoteModel).filter(MiddleNoteModel.id == note_id)
    result = await db.execute(query)
    note = result.scalar_one_or_none()
    
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    
    await db.delete(note)
    await db.commit()
    return {"message": "Note deleted successfully"}

@router.delete("/base/{note_id}")
async def delete_base_note(
    note_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Delete a base note.
    """
    query = select(BaseNoteModel).filter(BaseNoteModel.id == note_id)
    result = await db.execute(query)
    note = result.scalar_one_or_none()
    
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    
    await db.delete(note)
    await db.commit()
    return {"message": "Note deleted successfully"} 