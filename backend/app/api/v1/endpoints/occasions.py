from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.models.occasion import Occasion
from app.schemas.occasion import OccasionCreate, OccasionResponse

router = APIRouter()

@router.get("/", response_model=List[OccasionResponse])
async def get_occasions(
    db: AsyncSession = Depends(get_db)
):
    """
    Get all occasions.
    """
    query = select(Occasion)
    result = await db.execute(query)
    occasions = result.scalars().all()
    return occasions

@router.post("/", response_model=OccasionResponse)
async def create_occasion(
    occasion: OccasionCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new occasion.
    """
    db_occasion = Occasion(name=occasion.name)
    db.add(db_occasion)
    try:
        await db.commit()
        await db.refresh(db_occasion)
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Occasion with this name already exists"
        )
    return db_occasion

@router.delete("/{occasion_id}")
async def delete_occasion(
    occasion_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Delete an occasion.
    """
    query = select(Occasion).filter(Occasion.id == occasion_id)
    result = await db.execute(query)
    occasion = result.scalar_one_or_none()
    
    if occasion is None:
        raise HTTPException(status_code=404, detail="Occasion not found")
    
    await db.delete(occasion)
    await db.commit()
    return {"message": "Occasion deleted successfully"} 