from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.models.concentration import Concentration as ConcentrationModel
from app.schemas.concentration import Concentration, ConcentrationCreate

router = APIRouter()

@router.get("/", response_model=List[Concentration])
async def read_concentrations(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """
    Retrieve concentrations.
    """
    query = select(ConcentrationModel).offset(skip).limit(limit)
    result = await db.execute(query)
    concentrations = result.scalars().all()
    return concentrations

@router.post("/", response_model=Concentration)
async def create_concentration(
    *,
    db: AsyncSession = Depends(get_db),
    concentration_in: ConcentrationCreate
):
    """
    Create new concentration.
    """
    query = select(ConcentrationModel).filter(ConcentrationModel.name == concentration_in.name)
    result = await db.execute(query)
    db_concentration = result.scalar_one_or_none()
    
    if db_concentration:
        raise HTTPException(
            status_code=400,
            detail="Concentration with this name already exists."
        )
    
    db_concentration = ConcentrationModel(name=concentration_in.name)
    db.add(db_concentration)
    await db.commit()
    await db.refresh(db_concentration)
    return db_concentration

@router.get("/{concentration_id}", response_model=Concentration)
async def read_concentration(
    *,
    db: AsyncSession = Depends(get_db),
    concentration_id: int
):
    """
    Get concentration by ID.
    """
    query = select(ConcentrationModel).filter(ConcentrationModel.id == concentration_id)
    result = await db.execute(query)
    concentration = result.scalar_one_or_none()
    
    if not concentration:
        raise HTTPException(
            status_code=404,
            detail="Concentration not found"
        )
    return concentration 