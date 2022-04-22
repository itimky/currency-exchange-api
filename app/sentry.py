import sentry_sdk
from fastapi import FastAPI
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

from app.config import settings


def init_sentry(app: FastAPI) -> None:
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
    )
    app.add_middleware(SentryAsgiMiddleware)
