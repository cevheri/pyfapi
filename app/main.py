import logging as log
from contextlib import asynccontextmanager
from sys import prefix

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import load_database_settings
from app.config.app_settings import cors_settings

from fastapi import APIRouter, Depends

from app.api import user_api
from app.config.jwt_config import JWTBearer



@asynccontextmanager
async def lifespan(_):
    log.debug("FastAPI Lifespan started")
    load_database_settings()
    yield


app = FastAPI(
    title="PyFAPI",
    summary="Python FastAPI mongodb Application",
    description="Python FastAPI mongodb app for Enterprise usage with best practices, tools, and more.",
    version="1.0.0",
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc",
    openapi_url="/api/v1/openapi.json",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_settings.ALLOWED_ORIGINS,
    allow_credentials=cors_settings.ALLOW_CREDENTIALS,
    allow_methods=cors_settings.ALLOWED_METHODS,
    allow_headers=cors_settings.ALLOWED_HEADERS
)

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
