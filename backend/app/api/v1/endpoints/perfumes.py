from typing import List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, and_
from sqlalchemy.orm import selectinload, joinedload

from app.db.session import get_db
from app.models.perfume import Perfume as PerfumeModel
from app.models.perfume import Tag as TagModel
from app.models.perfume import PerfumeNote as PerfumeNoteModel
from app.models.note import Note as NoteModel
from app.models.main_accord import MainAccord as MainAccordModel
from app.schemas.perfume import Perfume, PerfumeList, Tag
from app.models.brand import Brand as BrandModel
from app.models.country import Country as CountryModel
from app.models.type import Type as TypeModel
from app.models.family import Family as FamilyModel
from app.models.perfumer import Perfumer as PerfumerModel
from app.models.concentration import Concentration as ConcentrationModel

router = APIRouter()

@router.get("/tags/", response_model=List[Tag])
async def get_tags(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """
    Get all tags.
    """
    query = select(TagModel).offset(skip).limit(limit)
    result = await db.execute(query)
    tags = result.scalars().all()
    return tags

@router.get("/", response_model=List[PerfumeList])
async def read_perfumes(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """
    Retrieve perfumes with only id, name, brand name, and image path.
    """
    query = (
        select(
            PerfumeModel.id,
            PerfumeModel.name,
            BrandModel.name.label('brand_name'),
            PerfumeModel.local_image_path
        )
        .join(BrandModel)
        .offset(skip)
        .limit(limit)
    )
    result = await db.execute(query)
    return [{"id": id, "name": name, "brand_name": brand_name, "local_image_path": local_image_path} 
            for id, name, brand_name, local_image_path in result]

@router.get("/search/", response_model=List[PerfumeList])
async def search_perfumes(
    db: AsyncSession = Depends(get_db),
    q: Optional[str] = None,
    country: Optional[str] = None,
    gender: Optional[str] = Query(None, regex="^(Male|Female|Unisex)$"),
    brand: Optional[str] = None,
    type: Optional[str] = None,
    family: Optional[str] = None,
    category: Optional[str] = None,
    concentration: Optional[str] = None,
    perfumer: Optional[str] = None,
    tag: Optional[str] = None,
    skip: int = 0,
    limit: int = 100
):
    """
    Search and filter perfumes with various criteria, returning only id, name, brand name, and image path.
    """
    query = (
        select(
            PerfumeModel.id,
            PerfumeModel.name,
            BrandModel.name.label('brand_name'),
            PerfumeModel.local_image_path
        )
        .join(BrandModel)
    )

    filters = []
    
    if q:
        filters.append(
            or_(
                PerfumeModel.name.ilike(f"%{q}%"),
                BrandModel.name.ilike(f"%{q}%")
            )
        )
    
    # Country filter
    if country:
        query = query.join(CountryModel)
        filters.append(CountryModel.name.ilike(f"%{country}%"))
    
    if gender:
        filters.append(PerfumeModel.gender.ilike(gender))
    
    # Brand filter
    if brand:
        filters.append(BrandModel.name.ilike(f"%{brand}%"))
    
    # Type filter
    if type:
        query = query.join(TypeModel)
        filters.append(TypeModel.name.ilike(f"%{type}%"))
    
    # Family filter
    if family:
        query = query.join(FamilyModel)
        filters.append(FamilyModel.name.ilike(f"%{family}%"))
    
    # Category filter
    if category:
        filters.append(PerfumeModel.category.ilike(f"%{category}%"))
    
    # Concentration filter
    if concentration:
        query = query.join(ConcentrationModel)
        filters.append(ConcentrationModel.name.ilike(f"%{concentration}%"))
    
    # Perfumer filter
    if perfumer:
        query = query.join(PerfumerModel)
        filters.append(PerfumerModel.name.ilike(f"%{perfumer}%"))

    # Tag filter
    if tag:
        query = query.join(PerfumeModel.tags).filter(TagModel.name.ilike(f"%{tag}%"))
    
    if filters:
        query = query.filter(and_(*filters))
    
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return [{"id": id, "name": name, "brand_name": brand_name, "local_image_path": local_image_path} 
            for id, name, brand_name, local_image_path in result]

@router.get("/{perfume_id}", response_model=Perfume)
async def get_perfume(
    perfume_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Get a specific perfume by ID.
    Returns full perfume details including all relationships.
    """
    query = (
        select(PerfumeModel)
        .options(
            selectinload(PerfumeModel.brand),
            selectinload(PerfumeModel.type),
            selectinload(PerfumeModel.family),
            selectinload(PerfumeModel.concentration),
            selectinload(PerfumeModel.country),
            selectinload(PerfumeModel.perfumer),
            selectinload(PerfumeModel.main_accords),
            selectinload(PerfumeModel.perfume_notes).selectinload(PerfumeNoteModel.note),
            selectinload(PerfumeModel.perfume_notes).selectinload(PerfumeNoteModel.note).selectinload(NoteModel.family),
            selectinload(PerfumeModel.perfume_notes).selectinload(PerfumeNoteModel.note).selectinload(NoteModel.moods),
            selectinload(PerfumeModel.tags)
        )
        .filter(PerfumeModel.id == perfume_id)
    )
    result = await db.execute(query)
    perfume = result.scalar_one_or_none()
    
    if perfume is None:
        raise HTTPException(status_code=404, detail="Perfume not found")
    
    # Create a dict with the concentration name instead of the object
    perfume_data = {
        "id": perfume.id,
        "name": perfume.name,
        "local_image_path": perfume.local_image_path,
        "gender": perfume.gender,
        "category": perfume.category,
        "release_year": perfume.release_year,
        "description": perfume.description,
        "longevity": perfume.longevity,
        "sillage": perfume.sillage,
        "occasion": perfume.occasion,
        "season": perfume.season,
        "inspiration": perfume.inspiration,
        "brand": perfume.brand.name if perfume.brand else None,
        "concentration": perfume.concentration.name if perfume.concentration else None,
        "type": perfume.type.name if perfume.type else None,
        "family": perfume.family.name if perfume.family else None,
        "country": perfume.country.name if perfume.country else None,
        "perfumer": perfume.perfumer.name if perfume.perfumer else None,
        "perfume_notes": [
            {
                "note_type": note.note_type,
                "note": note.note.name
            }
            for note in perfume.perfume_notes
        ] if perfume.perfume_notes else [],
        "main_accords": [accord.name for accord in perfume.main_accords] if perfume.main_accords else [],
        "tags": [tag.name for tag in perfume.tags] if perfume.tags else []
    }
    
    return Perfume.model_validate(perfume_data) 