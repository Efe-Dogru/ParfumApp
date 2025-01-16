from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.models.season import Season
from app.schemas.season import SeasonCreate, SeasonResponse

router = APIRouter()

@router.get("/", response_model=List[SeasonResponse])
async def get_seasons(
    db: AsyncSession = Depends(get_db)
):
    """
    Get all seasons.
    """
    query = select(Season)
    result = await db.execute(query)
    seasons = result.scalars().all()
    return seasons

@router.post("/", response_model=SeasonResponse)
async def create_season(
    season: SeasonCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new season.
    """
    db_season = Season(name=season.name)
    db.add(db_season)
    try:
        await db.commit()
        await db.refresh(db_season)
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Season with this name already exists"
        )
    return db_season

@router.delete("/{season_id}")
async def delete_season(
    season_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Delete a season.
    """
    query = select(Season).filter(Season.id == season_id)
    result = await db.execute(query)
    season = result.scalar_one_or_none()
    
    if season is None:
        raise HTTPException(status_code=404, detail="Season not found")
    
    await db.delete(season)
    await db.commit()
    return {"message": "Season deleted successfully"} 