from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.models.perfumer import Perfumer as PerfumerModel
from app.schemas.perfumer import Perfumer

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