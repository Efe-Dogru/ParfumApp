from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.models.brand import Brand as BrandModel
from app.schemas.brand import Brand, BrandCreate

router = APIRouter()

@router.get("/", response_model=List[Brand])
async def read_brands(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """
    Retrieve brands.
    """
    query = select(BrandModel).offset(skip).limit(limit)
    result = await db.execute(query)
    brands = result.scalars().all()
    return brands

@router.post("/", response_model=Brand)
async def create_brand(
    *,
    db: AsyncSession = Depends(get_db),
    brand_in: BrandCreate
):
    """
    Create new brand.
    """
    query = select(BrandModel).filter(BrandModel.name == brand_in.name)
    result = await db.execute(query)
    db_brand = result.scalar_one_or_none()
    
    if db_brand:
        raise HTTPException(
            status_code=400,
            detail="Brand with this name already exists."
        )
    
    db_brand = BrandModel(name=brand_in.name)
    db.add(db_brand)
    await db.commit()
    await db.refresh(db_brand)
    return db_brand

@router.get("/{brand_id}", response_model=Brand)
async def read_brand(
    *,
    db: AsyncSession = Depends(get_db),
    brand_id: int
):
    """
    Get brand by ID.
    """
    query = select(BrandModel).filter(BrandModel.id == brand_id)
    result = await db.execute(query)
    brand = result.scalar_one_or_none()
    
    if not brand:
        raise HTTPException(
            status_code=404,
            detail="Brand not found"
        )
    return brand 