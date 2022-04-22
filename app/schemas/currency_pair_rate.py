import datetime
from typing import Any

from pydantic import BaseModel
from pydantic.utils import GetterDict


class CurrencyPairRateGetter(GetterDict):
    def get(self, key: str, default: Any = None) -> Any:
        if key in ("base", "quote"):
            return getattr(self._obj, key).name
        return getattr(self._obj, key)


# Shared properties
class CurrencyPairRate(BaseModel):
    base: str
    quote: str
    date: datetime.date
    rate: str

    class Config:
        orm_mode = True
        # json_encoders = {Decimal: str}
        getter_dict = CurrencyPairRateGetter


# Properties to receive on item creation
class CurrencyPairRateCreate(CurrencyPairRate):
    pass


# Properties to receive on item update
class CurrencyPairRateUpdate(CurrencyPairRate):
    pass
