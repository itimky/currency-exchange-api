from decimal import Decimal

from pydantic import BaseModel


# Shared properties
class CurrencyPairRate(BaseModel):
    base: str
    quote: str
    rate: Decimal

    class Config:
        orm_mode = True


# Properties to receive on item creation
class CurrencyPairRateCreate(CurrencyPairRate):
    pass


# Properties to receive on item update
class CurrencyPairRateUpdate(CurrencyPairRate):
    pass
