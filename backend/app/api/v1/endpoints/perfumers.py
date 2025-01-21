from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.models.perfumer import Perfumer as PerfumerModel
from app.schemas.perfumer import Perfumer, PerfumerCreate

router = APIRouter()

@router.get("/", response_model=List[Perfumer])
async def read_perfumers(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """
    Retrieve perfumers.
    """
    query = select(PerfumerModel).offset(skip).limit(limit)
    result = await db.execute(query)
    perfumers = result.scalars().all()
    return perfumers

@router.post("/", response_model=Perfumer)
async def create_perfumer(
    *,
    db: AsyncSession = Depends(get_db),
    perfumer_in: PerfumerCreate
):
    """
    Create new perfumer.
    """
    query = select(PerfumerModel).filter(PerfumerModel.name == perfumer_in.name)
    result = await db.execute(query)
    db_perfumer = result.scalar_one_or_none()
    
    if db_perfumer:
        raise HTTPException(
            status_code=400,
            detail="Perfumer with this name already exists."
        )
    
    db_perfumer = PerfumerModel(name=perfumer_in.name)
    db.add(db_perfumer)
    await db.commit()
    await db.refresh(db_perfumer)
    return db_perfumer

@router.get("/{perfumer_id}", response_model=Perfumer)
async def read_perfumer(
    *,
    db: AsyncSession = Depends(get_db),
    perfumer_id: int
):
    """
    Get perfumer by ID.
    """
    query = select(PerfumerModel).filter(PerfumerModel.id == perfumer_id)
    result = await db.execute(query)
    perfumer = result.scalar_one_or_none()
    
    if not perfumer:
        raise HTTPException(
            status_code=404,
            detail="Perfumer not found"
        )
    return perfumer 