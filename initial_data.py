import json
import logging
from datetime import datetime
from decimal import Decimal
from typing import List, Dict

from sqlalchemy.orm import Session

# from app.db.init_db import init_db
from app.db.session import SessionLocal
from app.models import Currency, CurrencyPairRate

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init() -> None:
    db = SessionLocal()
    populate(db)
    # init_db(db)


def populate(db: Session) -> None:
    with open('./initial_data/data.json') as json_file:
        data = json.load(json_file)

    currencies = populate_currencies(db, data['currencies'])
    cur_map = {c.name: c.id for c in currencies}
    populate_rates(db, cur_map, data['rates'])


def populate_currencies(db: Session, currencies: List[str]) -> List[Currency]:
    curs: List[Currency] = [
        Currency(
            name=cur,
        )
        for cur in currencies
    ]
    db.add_all(curs)
    db.commit()

    return curs


def populate_rates(db: Session, cur_map: Dict[str, int], rates: List[Dict[str, str]]) -> None:
    pair_rates: List[CurrencyPairRate] = [
        CurrencyPairRate(
            base_id=cur_map[rate['base']],
            quote_id=cur_map[rate['quote']],
            rate=Decimal(rate['rate']),
            date=datetime.strptime(rate['date'], "%Y-%m-%d").date(),
        )
        for rate in rates
    ]

    db.add_all(pair_rates)
    db.commit()


def main() -> None:
    logger.info("Creating initial data")
    init()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
