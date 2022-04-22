from fastapi import APIRouter

from app.api.api_v1.endpoints import currency_pair_rates

api_router = APIRouter()
api_router.include_router(currency_pair_rates.router, prefix='/currency-pair-rates')
