from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.models.concentration import Concentration as ConcentrationModel
from app.schemas.concentration import Concentration

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