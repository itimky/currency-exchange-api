from sqlalchemy import Column, Date, Numeric, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.db.base_class import Base

RATE_PRECISION = 18
RATE_SCALE = 6


class CurrencyPairRate(Base):
    id = Column(Integer, primary_key=True, index=True)
    base_id = Column(Integer, ForeignKey("currency.id"), nullable=False)
    base = relationship("Currency", foreign_keys=[base_id], lazy='joined')
    quote_id = Column(Integer, ForeignKey("currency.id"), nullable=False)
    quote = relationship("Currency", foreign_keys=[quote_id], lazy='joined')
    date = Column(Date, nullable=False)
    rate = Column(Numeric(RATE_PRECISION, RATE_SCALE), nullable=False)
