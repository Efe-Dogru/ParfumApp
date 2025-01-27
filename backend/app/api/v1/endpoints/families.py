from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.models.family import Family as FamilyModel
from app.schemas.family import Family

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