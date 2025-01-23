from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, and_, join
from sqlalchemy.orm import selectinload

from app.db.session import get_db
from app.models.perfume import Perfume as PerfumeModel, PerfumeNote as PerfumeNoteModel
from app.models.note import Note as NoteModel
from app.models.main_accord import MainAccord as MainAccordModel
from app.schemas.perfume import Perfume, PerfumeCreate, PerfumeUpdate
from app.models.brand import Brand as BrandModel
from app.models.country import Country as CountryModel
from app.models.type import Type as TypeModel
from app.models.family import Family as FamilyModel
from app.models.perfumer import Perfumer as PerfumerModel
from app.models.concentration import Concentration as ConcentrationModel

router = APIRouter()

@router.get("/", response_model=List[Perfume])
async def read_perfumes(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """
    Retrieve perfumes.
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
            selectinload(PerfumeModel.notes).selectinload(PerfumeNoteModel.note)
        )
        .offset(skip)
        .limit(limit)
    )
    result = await db.execute(query)
    perfumes = result.scalars().all()
    return perfumes

@router.post("/", response_model=Perfume)
async def create_perfume(
    *,
    db: AsyncSession = Depends(get_db),
    perfume_in: PerfumeCreate
):
    """
    Create new perfume.
    """
    query = select(PerfumeModel).filter(PerfumeModel.name == perfume_in.name)
    result = await db.execute(query)
    db_perfume = result.scalar_one_or_none()
    
    if db_perfume:
        raise HTTPException(
            status_code=400,
            detail="Perfume with this name already exists."
        )
    
    # Create perfume
    db_perfume = PerfumeModel(**perfume_in.dict(exclude={'notes', 'main_accord_ids'}))
    db.add(db_perfume)
    await db.commit()
    await db.refresh(db_perfume)

    # Add notes
    if perfume_in.notes:
        for note_data in perfume_in.notes:
            perfume_note = PerfumeNoteModel(
                perfume_id=db_perfume.id,
                note_id=note_data.note_id,
                note_type=note_data.note_type
            )
            db.add(perfume_note)

    # Add main accords
    if perfume_in.main_accord_ids:
        main_accords = await get_related_items(db, MainAccordModel, perfume_in.main_accord_ids)
        db_perfume.main_accords = main_accords

    await db.commit()
    await db.refresh(db_perfume)
    return db_perfume

@router.get("/{perfume_id}", response_model=Perfume)
async def read_perfume(
    *,
    db: AsyncSession = Depends(get_db),
    perfume_id: int
):
    """
    Get perfume by ID.
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
            selectinload(PerfumeModel.notes).selectinload(PerfumeNoteModel.note)
        )
        .filter(PerfumeModel.id == perfume_id)
    )
    result = await db.execute(query)
    perfume = result.scalar_one_or_none()
    
    if not perfume:
        raise HTTPException(
            status_code=404,
            detail="Perfume not found"
        )
    return perfume

@router.put("/{perfume_id}", response_model=Perfume)
async def update_perfume(
    *,
    db: AsyncSession = Depends(get_db),
    perfume_id: int,
    perfume_in: PerfumeUpdate
):
    """
    Update perfume.
    """
    query = select(PerfumeModel).filter(PerfumeModel.id == perfume_id)
    result = await db.execute(query)
    db_perfume = result.scalar_one_or_none()
    
    if not db_perfume:
        raise HTTPException(
            status_code=404,
            detail="Perfume not found"
        )
    
    # Update basic fields
    update_data = perfume_in.dict(exclude_unset=True, exclude={'notes', 'main_accord_ids'})
    for field, value in update_data.items():
        setattr(db_perfume, field, value)
    
    # Update notes if provided
    if perfume_in.notes is not None:
        # Remove existing notes
        await db.execute(
            select(PerfumeNoteModel)
            .filter(PerfumeNoteModel.perfume_id == perfume_id)
            .delete()
        )
        
        # Add new notes
        for note_data in perfume_in.notes:
            perfume_note = PerfumeNoteModel(
                perfume_id=db_perfume.id,
                note_id=note_data.note_id,
                note_type=note_data.note_type
            )
            db.add(perfume_note)

    # Update main accords if provided
    if perfume_in.main_accord_ids is not None:
        main_accords = await get_related_items(db, MainAccordModel, perfume_in.main_accord_ids)
        db_perfume.main_accords = main_accords
    
    await db.commit()
    await db.refresh(db_perfume)
    return db_perfume

@router.delete("/{perfume_id}")
async def delete_perfume(
    *,
    db: AsyncSession = Depends(get_db),
    perfume_id: int
):
    """
    Delete perfume by ID.
    """
    query = select(PerfumeModel).filter(PerfumeModel.id == perfume_id)
    result = await db.execute(query)
    perfume = result.scalar_one_or_none()
    
    if not perfume:
        raise HTTPException(
            status_code=404,
            detail="Perfume not found"
        )
    
    await db.delete(perfume)
    await db.commit()
    return {"message": "Perfume deleted successfully"}

async def get_related_items(db: AsyncSession, model, ids: List[int]):
    if not ids:
        return []
    query = select(model).filter(model.id.in_(ids))
    result = await db.execute(query)
    return result.scalars().all()

@router.get("/search/", response_model=List[Perfume])
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
    skip: int = 0,
    limit: int = 100
):
    """
    Search and filter perfumes with various criteria:
    - q: Search query for perfume name or brand name
    - country: Filter by country name
    - gender: Filter by gender (Male, Female, or Unisex)
    - brand: Filter by brand name
    - type: Filter by perfume type name
    - family: Filter by perfume family name
    - category: Filter by perfume category
    - concentration: Filter by concentration name
    - perfumer: Filter by perfumer name
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
            selectinload(PerfumeModel.notes).selectinload(PerfumeNoteModel.note)
        )
    )
    
    filters = []
    
    if q:
        filters.append(
            or_(
                PerfumeModel.name.ilike(f"%{q}%"),
                PerfumeModel.brand.has(BrandModel.name.ilike(f"%{q}%"))
            )
        )
    
    # Country filter
    if country:
        filters.append(PerfumeModel.country.has(CountryModel.name.ilike(f"%{country}%")))
    
    if gender:
        filters.append(PerfumeModel.gender.ilike(gender))
    
    # Brand filter
    if brand:
        filters.append(PerfumeModel.brand.has(BrandModel.name.ilike(f"%{brand}%")))
    
    # Type filter
    if type:
        filters.append(PerfumeModel.type.has(TypeModel.name.ilike(f"%{type}%")))
    
    # Family filter
    if family:
        filters.append(PerfumeModel.family.has(FamilyModel.name.ilike(f"%{family}%")))
    
    # Category filter
    if category:
        filters.append(PerfumeModel.category.ilike(f"%{category}%"))
    
    # Concentration filter
    if concentration:
        filters.append(PerfumeModel.concentration.has(ConcentrationModel.name.ilike(f"%{concentration}%")))
    
    # Perfumer filter
    if perfumer:
        filters.append(PerfumeModel.perfumer.has(PerfumerModel.name.ilike(f"%{perfumer}%")))
    
    if filters:
        query = query.filter(and_(*filters))
    
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    perfumes = result.scalars().all()
    return perfumes 