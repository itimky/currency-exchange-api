from fastapi import FastAPI

from app.api.api_v1.api import api_router
from app.config import settings
from app.sentry import init_sentry

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)


init_sentry(app)


app.include_router(api_router, prefix=settings.API_V1_STR)
