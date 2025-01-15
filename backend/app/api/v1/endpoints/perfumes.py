from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_

from app.db.session import get_db
from app.models.perfume import Perfume
from app.schemas.perfume import PerfumeCreate, PerfumeUpdate, Perfume as PerfumeSchema

router = APIRouter()

@router.get("/", response_model=List[PerfumeSchema])
async def get_perfumes(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    brand: Optional[str] = None,
    search: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """
    Retrieve perfumes with pagination, optional brand filtering and name search.
    """
    query = select(Perfume)
    
    if brand:
        query = query.filter(Perfume.brand == brand)
    
    if search:
        search_filter = or_(
            Perfume.name.ilike(f"%{search}%"),
            Perfume.brand.ilike(f"%{search}%"),
            Perfume.brand_line.ilike(f"%{search}%")
        )
        query = query.filter(search_filter)
    
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    perfumes = result.scalars().all()
    return perfumes

@router.get("/brands", response_model=List[str])
async def get_brands(db: AsyncSession = Depends(get_db)):
    """
    Get a list of all unique brands.
    """
    query = select(Perfume.brand).distinct()
    result = await db.execute(query)
    brands = result.scalars().all()
    return brands

@router.get("/{perfume_id}", response_model=PerfumeSchema)
async def get_perfume(
    perfume_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Get a specific perfume by ID.
    """
    query = select(Perfume).filter(Perfume.id == perfume_id)
    result = await db.execute(query)
    perfume = result.scalar_one_or_none()
    
    if perfume is None:
        raise HTTPException(status_code=404, detail="Perfume not found")
    return perfume

@router.post("/", response_model=PerfumeSchema)
async def create_perfume(
    perfume: PerfumeCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new perfume.
    """
    db_perfume = Perfume(**perfume.model_dump())
    db.add(db_perfume)
    await db.commit()
    await db.refresh(db_perfume)
    return db_perfume

@router.put("/{perfume_id}", response_model=PerfumeSchema)
async def update_perfume(
    perfume_id: int,
    perfume: PerfumeUpdate,
    db: AsyncSession = Depends(get_db)
):
    """
    Update a perfume.
    """
    query = select(Perfume).filter(Perfume.id == perfume_id)
    result = await db.execute(query)
    db_perfume = result.scalar_one_or_none()
    
    if db_perfume is None:
        raise HTTPException(status_code=404, detail="Perfume not found")
    
    update_data = perfume.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_perfume, field, value)
    
    await db.commit()
    await db.refresh(db_perfume)
    return db_perfume

@router.delete("/{perfume_id}")
async def delete_perfume(
    perfume_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Delete a perfume.
    """
    query = select(Perfume).filter(Perfume.id == perfume_id)
    result = await db.execute(query)
    perfume = result.scalar_one_or_none()
    
    if perfume is None:
        raise HTTPException(status_code=404, detail="Perfume not found")
    
    await db.delete(perfume)
    await db.commit()
    return {"message": "Perfume deleted successfully"} 