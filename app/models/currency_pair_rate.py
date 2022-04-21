from typing import TYPE_CHECKING

from sqlalchemy import Column, Date, Numeric, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .user import User  # noqa: F401


class CurrencyPairRate(Base):
    id = Column(Integer, primary_key=True, index=True)
    base_id = Column(Integer, ForeignKey("currency.id"), nullable=False)
    base = relationship("Currency", foreign_keys=[base_id])
    quote_id = Column(Integer, ForeignKey("currency.id"), nullable=False)
    quote = relationship("Currency", foreign_keys=[quote_id])
    rate = Column(Numeric(20, 14), nullable=False)
    date = Column(Date, nullable=False)
