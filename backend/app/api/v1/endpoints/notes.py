from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, and_
from sqlalchemy.orm import selectinload

from app.db.session import get_db
from app.models.note import Note as NoteModel, NoteFamily as NoteFamilyModel, NoteMood as NoteMoodModel
from app.schemas.note import Note, NoteFamily, NoteMood, NoteList

router = APIRouter()

@router.get("/families/", response_model=List[NoteFamily])
async def get_note_families(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """
    Get all note families.
    """
    query = select(NoteFamilyModel).offset(skip).limit(limit)
    result = await db.execute(query)
    families = result.scalars().all()
    return families

@router.get("/moods/", response_model=List[NoteMood])
async def get_note_moods(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """
    Get all note moods.
    """
    query = select(NoteMoodModel).offset(skip).limit(limit)
    result = await db.execute(query)
    moods = result.scalars().all()
    return moods

@router.get("/", response_model=List[NoteList])
async def get_notes(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    family: Optional[str] = None,
    mood: Optional[str] = None
):
    """
    Get all notes with optional filtering by family and mood names.
    Returns only id, name, and image_filename.
    """
    query = (
        select(
            NoteModel.id,
            NoteModel.name,
            NoteModel.image_filename
        )
    )
    
    filters = []
    
    if family:
        query = query.join(NoteFamilyModel)
        filters.append(NoteFamilyModel.name.ilike(f"%{family}%"))
    
    if mood:
        query = query.join(NoteModel.moods)
        filters.append(NoteMoodModel.name.ilike(f"%{mood}%"))
    
    if filters:
        query = query.filter(and_(*filters))
    
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return [{"id": id, "name": name, "image_filename": image_filename} for id, name, image_filename in result]

@router.get("/search/", response_model=List[NoteList])
async def search_notes(
    db: AsyncSession = Depends(get_db),
    q: Optional[str] = None,
    family: Optional[str] = None,
    mood: Optional[str] = None,
    limit: int = 100
):
    """
    Search notes by name and filter by family and mood names.
    Returns only id, name, and image_filename.
    """
    query = (
        select(
            NoteModel.id,
            NoteModel.name,
            NoteModel.image_filename
        )
    )
    
    filters = []
    
    if q:
        filters.append(
            or_(
                NoteModel.name.ilike(f"%{q}%"),
                NoteModel.normalized_name.ilike(f"%{q}%")
            )
        )
    
    if family:
        query = query.join(NoteFamilyModel)
        filters.append(NoteFamilyModel.name.ilike(f"%{family}%"))
    
    if mood:
        query = query.join(NoteModel.moods)
        filters.append(NoteMoodModel.name.ilike(f"%{mood}%"))
    
    if filters:
        query = query.filter(and_(*filters))
    
    query = query.limit(limit)
    result = await db.execute(query)
    return [{"id": id, "name": name, "image_filename": image_filename} for id, name, image_filename in result]

@router.get("/{note_id}", response_model=Note)
async def get_note(
    note_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Get a specific note by ID.
    Returns full note details.
    """
    query = (
        select(NoteModel)
        .options(
            selectinload(NoteModel.family),
            selectinload(NoteModel.moods)
        )
        .filter(NoteModel.id == note_id)
    )
    result = await db.execute(query)
    note = result.scalar_one_or_none()
    
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    
    return note 