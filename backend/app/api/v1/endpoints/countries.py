from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.models.country import Country as CountryModel
from app.schemas.country import Country, CountryCreate

router = APIRouter()

@router.get("/", response_model=List[Country])
async def read_countries(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """
    Retrieve countries.
    """
    query = select(CountryModel).offset(skip).limit(limit)
    result = await db.execute(query)
    countries = result.scalars().all()
    return countries

@router.post("/", response_model=Country)
async def create_country(
    *,
    db: AsyncSession = Depends(get_db),
    country_in: CountryCreate
):
    """
    Create new country.
    """
    query = select(CountryModel).filter(CountryModel.name == country_in.name)
    result = await db.execute(query)
    db_country = result.scalar_one_or_none()
    
    if db_country:
        raise HTTPException(
            status_code=400,
            detail="Country with this name already exists."
        )
    
    db_country = CountryModel(name=country_in.name)
    db.add(db_country)
    await db.commit()
    await db.refresh(db_country)
    return db_country

@router.get("/{country_id}", response_model=Country)
async def read_country(
    *,
    db: AsyncSession = Depends(get_db),
    country_id: int
):
    """
    Get country by ID.
    """
    query = select(CountryModel).filter(CountryModel.id == country_id)
    result = await db.execute(query)
    country = result.scalar_one_or_none()
    
    if not country:
        raise HTTPException(
            status_code=404,
            detail="Country not found"
        )
    return country 