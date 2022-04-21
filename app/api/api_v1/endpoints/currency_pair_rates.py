from typing import Any, List, Generator

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, schemas
from app.db.session import SessionLocal

router = APIRouter()


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@router.get("/history/{base}/{quote}", response_model=List[schemas.CurrencyPairRate])
def get_currency_pair_rate_history(
    base: str,
    quote: str,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve currency_pair_rate history.
    """
    return crud.currency_pair_rate.get_history(db, base=base, quote=quote, skip=skip, limit=limit)
