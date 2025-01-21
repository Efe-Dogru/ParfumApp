from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.models.family import Family as FamilyModel
from app.schemas.family import Family, FamilyCreate

router = APIRouter()

@router.get("/", response_model=List[Family])
async def read_families(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """
    Retrieve families.
    """
    query = select(FamilyModel).offset(skip).limit(limit)
    result = await db.execute(query)
    families = result.scalars().all()
    return families

@router.post("/", response_model=Family)
async def create_family(
    *,
    db: AsyncSession = Depends(get_db),
    family_in: FamilyCreate
):
    """
    Create new family.
    """
    query = select(FamilyModel).filter(FamilyModel.name == family_in.name)
    result = await db.execute(query)
    db_family = result.scalar_one_or_none()
    
    if db_family:
        raise HTTPException(
            status_code=400,
            detail="Family with this name already exists."
        )
    
    db_family = FamilyModel(name=family_in.name)
    db.add(db_family)
    await db.commit()
    await db.refresh(db_family)
    return db_family

@router.get("/{family_id}", response_model=Family)
async def read_family(
    *,
    db: AsyncSession = Depends(get_db),
    family_id: int
):
    """
    Get family by ID.
    """
    query = select(FamilyModel).filter(FamilyModel.id == family_id)
    result = await db.execute(query)
    family = result.scalar_one_or_none()
    
    if not family:
        raise HTTPException(
            status_code=404,
            detail="Family not found"
        )
    return family 