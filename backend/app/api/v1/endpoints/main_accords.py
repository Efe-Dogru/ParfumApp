from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.models.main_accord import MainAccord as MainAccordModel
from app.schemas.main_accord import MainAccord

router = APIRouter()

@router.get("/", response_model=List[MainAccord])
async def read_main_accords(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """
    Retrieve main accords.
    """
    query = select(MainAccordModel).offset(skip).limit(limit)
    result = await db.execute(query)
    main_accords = result.scalars().all()
    return main_accords 