import datetime
from typing import List, Optional

from sqlalchemy import Numeric, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased
from sqlalchemy.sql import cast, func

from app.crud.base import CRUDBase
from app.models import Currency
from app.models.currency_pair_rate import RATE_PRECISION, RATE_SCALE, CurrencyPairRate


class CRUDCurrencyPairRate(
    CRUDBase[CurrencyPairRate, CurrencyPairRate, CurrencyPairRate]
):
    async def get_history(
        self,
        db: AsyncSession,
        base: str,
        quote: str,
        skip: int = 0,
        limit: int = 100,
    ) -> List[CurrencyPairRate]:
        base_alias, quote_alias = aliased(Currency), aliased(Currency)
        query = (
            select(self.model)
            .join(base_alias, self.model.base)
            .join(quote_alias, self.model.quote)
            .filter(base_alias.name == base, quote_alias.name == quote)
            .order_by(CurrencyPairRate.date.desc())
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        return result.scalars().all()

    async def find_rate(
        self, db: AsyncSession, base: str, quote: str, date: datetime.date
    ) -> Optional[CurrencyPairRate]:
        rate = await self.get_rate(db, base, quote, date)
        if rate is None:
            rate = await self.get_intermediate_rate(db, base, quote, date)

        return rate

    async def get_rate(
        self, db: AsyncSession, base: str, quote: str, date: datetime.date
    ) -> Optional[CurrencyPairRate]:
        base_alias, quote_alias = aliased(Currency), aliased(Currency)
        query = (
            select(self.model)
            .join(base_alias, self.model.base)
            .join(quote_alias, self.model.quote)
            .filter(
                base_alias.name == base,
                quote_alias.name == quote,
                self.model.date == date,
            )
        )
        result = await db.execute(query)
        return result.scalars().first()

    async def get_intermediate_rate(
        self, db: AsyncSession, base: str, quote: str, date: datetime.date
    ) -> Optional[CurrencyPairRate]:
        base_rate_alias, intermediate_rate_alias = aliased(CurrencyPairRate), aliased(
            CurrencyPairRate
        )
        base_alias, quote_alias = aliased(Currency), aliased(Currency)
        query = (
            select(
                cast(
                    func.min(base_rate_alias.rate * intermediate_rate_alias.rate),
                    Numeric(RATE_PRECISION, RATE_SCALE),
                )
            )
            .select_from(base_rate_alias)
            .join(
                intermediate_rate_alias,
                base_rate_alias.quote_id == intermediate_rate_alias.base_id,
            )
            .join(base_alias, base_rate_alias.base)
            .join(quote_alias, intermediate_rate_alias.quote)
            .filter(
                base_alias.name == base,
                quote_alias.name == quote,
                base_rate_alias.date == date,
                intermediate_rate_alias.date == date,
            )
        )

        result = await db.execute(query)
        final_rate = result.scalars().first()

        if final_rate is None:
            return None

        return CurrencyPairRate(
            base=Currency(name=base),
            quote=Currency(name=quote),
            date=date,
            rate=final_rate,
        )


currency_pair_rate = CRUDCurrencyPairRate(CurrencyPairRate)
