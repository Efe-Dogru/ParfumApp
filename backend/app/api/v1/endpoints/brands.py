from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.models.brand import Brand as BrandModel
from app.schemas.brand import Brand

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