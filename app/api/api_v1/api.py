from fastapi import APIRouter

from app.api.api_v1.endpoints import currency_pair_rates  # items, users

api_router = APIRouter()
api_router.include_router(currency_pair_rates.router, prefix='/currency-pair-rates')
# api_router.include_router(users.router, prefix="/users", tags=["users"])
# api_router.include_router(items.router, prefix="/items", tags=["items"])
