from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.models.main_accord import MainAccord
from app.schemas.main_accord import MainAccordCreate, MainAccordResponse

router = APIRouter()

@router.get("/", response_model=List[MainAccordResponse])
async def get_main_accords(
    db: AsyncSession = Depends(get_db)
):
    """
    Get all main accords.
    """
    query = select(MainAccord)
    result = await db.execute(query)
    accords = result.scalars().all()
    return accords

@router.post("/", response_model=MainAccordResponse)
async def create_main_accord(
    accord: MainAccordCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new main accord.
    """
    db_accord = MainAccord(name=accord.name)
    db.add(db_accord)
    try:
        await db.commit()
        await db.refresh(db_accord)
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Main accord with this name already exists"
        )
    return db_accord

@router.delete("/{accord_id}")
async def delete_main_accord(
    accord_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Delete a main accord.
    """
    query = select(MainAccord).filter(MainAccord.id == accord_id)
    result = await db.execute(query)
    accord = result.scalar_one_or_none()
    
    if accord is None:
        raise HTTPException(status_code=404, detail="Main accord not found")
    
    await db.delete(accord)
    await db.commit()
    return {"message": "Main accord deleted successfully"} 