from typing import List

from app.crud.base import CRUDBase
from sqlalchemy.orm import Session, aliased

from app.models import Currency
from app.models.currency_pair_rate import CurrencyPairRate
from app.schemas.currency_pair_rate import CurrencyPairRateCreate, CurrencyPairRateUpdate


class CRUDCurrencyPairRate(CRUDBase[CurrencyPairRate, CurrencyPairRateCreate, CurrencyPairRateUpdate]):
    def get_history(
        self, db: Session, base: str, quote: str, skip: int = 0, limit: int = 100,
    ) -> List[CurrencyPairRate]:
        base_alias, quote_alias = aliased(Currency), aliased(Currency)
        return db.query(self.model).join(base_alias, self.model.base).join(quote_alias, self.model.quote)\
            .filter(base_alias.name == base, quote_alias.name == quote)\
            .order_by(CurrencyPairRate.date.desc()).offset(skip).limit(limit).all()
    pass


currency_pair_rate = CRUDCurrencyPairRate(CurrencyPairRate)
