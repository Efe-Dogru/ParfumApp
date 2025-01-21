from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, and_, join
from sqlalchemy.orm import selectinload

from app.db.session import get_db
from app.models.perfume import Perfume as PerfumeModel
from app.models.note import TopNote, MiddleNote, BaseNote
from app.models.main_accord import MainAccord as MainAccordModel
from app.schemas.perfume import Perfume, PerfumeCreate, PerfumeUpdate

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
            selectinload(PerfumeModel.top_notes),
            selectinload(PerfumeModel.middle_notes),
            selectinload(PerfumeModel.base_notes)
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
    
    db_perfume = PerfumeModel(
        name=perfume_in.name,
        brand_id=perfume_in.brand_id,
        type_id=perfume_in.type_id,
        family_id=perfume_in.family_id,
        concentration_id=perfume_in.concentration_id,
        country_id=perfume_in.country_id,
        perfumer_id=perfume_in.perfumer_id,
        description=perfume_in.description,
        year=perfume_in.year,
        price=perfume_in.price,
        image_url=perfume_in.image_url
    )
    db.add(db_perfume)
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
            selectinload(PerfumeModel.top_notes),
            selectinload(PerfumeModel.middle_notes),
            selectinload(PerfumeModel.base_notes)
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
    
    update_data = perfume_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_perfume, field, value)
    
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
    skip: int = 0,
    limit: int = 100
):
    """
    Search perfumes by name or brand name.
    - q: Search query for perfume name or brand name
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
            selectinload(PerfumeModel.top_notes),
            selectinload(PerfumeModel.middle_notes),
            selectinload(PerfumeModel.base_notes)
        )
    )
    
    if q:
        query = (
            query
            .join(PerfumeModel.brand)
            .filter(
                or_(
                    PerfumeModel.name.ilike(f"%{q}%"),
                    PerfumeModel.brand.has(name=q)
                )
            )
        )
    
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    perfumes = result.scalars().all()
    return perfumes 