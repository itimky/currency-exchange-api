import datetime
from typing import Any, List, Generator, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, schemas
from app.db.session import SessionLocalAsync

router = APIRouter()


async def get_db() -> Generator:
    try:
        async with SessionLocalAsync() as db:
            yield db
    finally:
        await db.close()


@router.get("/history/{base}/{quote}", response_model=List[schemas.CurrencyPairRate])
async def get_currency_pair_rate_history(
    base: str,
    quote: str,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Retrieve currency_pair_rate history.
    """
    return await crud.currency_pair_rate.get_history(db, base=base, quote=quote, skip=skip, limit=limit)


@router.get('/rate/{base}/{quote}', response_model=Optional[schemas.CurrencyPairRate])
async def get_currency_pair_rate_history(
        base: str,
        quote: str,
        date: datetime.date,
        db: AsyncSession = Depends(get_db),
) -> Any:
    return await crud.currency_pair_rate.find_rate(db, base=base, quote=quote, date=date)
