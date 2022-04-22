import datetime
from typing import Any

from pydantic import BaseModel
from pydantic.utils import GetterDict


class CurrencyPairRateGetter(GetterDict):
    def get(self, key: str, default: Any = None) -> Any:
        if key in ("base", "quote"):
            return getattr(self._obj, key).name
        return getattr(self._obj, key)


class CurrencyPairRate(BaseModel):
    base: str
    quote: str
    date: datetime.date
    rate: str

    class Config:
        orm_mode = True
        getter_dict = CurrencyPairRateGetter
