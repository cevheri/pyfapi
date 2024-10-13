import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from app import init_db
from app.api import user_api, auth_api, account_api
from app.config.app_settings import cors_settings, server_settings
from app.migration.migration_000 import init_migration
from app.security.auth_config import JWTBearer

print("app.main.py is running")

log = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_):
    log.debug("FastAPI Lifespan started")
    await init_db()
    await init_migration()
    yield


app = FastAPI(
    title="PyFAPI",
    summary="Python FastAPI mongodb Application",
    description="Python FastAPI mongodb app for Enterprise usage with best practices, tools, and more.",
    version="1.0.0",
    docs_url=f"{server_settings.CONTEXT_PATH}/docs",
    redoc_url=f"{server_settings.CONTEXT_PATH}/redoc",
    openapi_url=f"{server_settings.CONTEXT_PATH}/openapi.json",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_settings.ALLOWED_ORIGINS,
    allow_credentials=cors_settings.ALLOW_CREDENTIALS,
    allow_methods=cors_settings.ALLOWED_METHODS,
    allow_headers=cors_settings.ALLOWED_HEADERS
)

app.include_router(auth_api.router, tags=["auth"])
app.include_router(account_api.router, tags=["account"], dependencies=[Depends(JWTBearer())])
app.include_router(user_api.router, tags=["users"], dependencies=[Depends(JWTBearer())])


@app.get("/")
async def root():
    return {
        "app": {
            "name": "PyFAPI Application",
            "description": "Python FastAPI mongodb app for Enterprise usage with best practices, tools, and more.",
            "version": "1.0.0",
        },
        "author": "cevheri",
        "github": "https://github.com/cevheri/pyfapi.git",
    }
