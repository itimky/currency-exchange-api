# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base  # noqa
from app.models.currency import Currency
from app.models.currency_pair_rate import CurrencyPairRate
