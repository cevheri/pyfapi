import logging
from contextlib import asynccontextmanager

import markdown
from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates

from app import init_db
from app.api import user_api, auth_api, account_api
from app.conf.app_settings import cors_settings, server_settings, app_settings
from app.migration import user_migration
from app.security import auth_handler

print("app.main.py is running")

log = logging.getLogger(__name__)

templates = Jinja2Templates(directory="././templates")


@asynccontextmanager
async def lifespan(_):
    log.debug("FastAPI Lifespan started")
    await init_db()
    await user_migration.init_migration()
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

# noinspection PyTypeChecker
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_settings.ALLOWED_ORIGINS,
    allow_credentials=cors_settings.ALLOW_CREDENTIALS,
    allow_methods=cors_settings.ALLOWED_METHODS,
    allow_headers=cors_settings.ALLOWED_HEADERS
)

app.include_router(auth_api.router, tags=["auth"])
app.include_router(account_api.router, tags=["account"], dependencies=[Depends(auth_handler.get_current_user)])
app.include_router(user_api.router, tags=["users"], dependencies=[Depends(auth_handler.get_current_user)])


# async def get_root_page(request: Request):
#     context = {
#         "request": request,
#         "app_name": app_settings.APP_NAME,
#         "app_url": app_settings.APP_URL,
#         "app_description": app_settings.APP_DESCRIPTION,
#         "app_version": app_settings.APP_VERSION,
#         "server_settings": server_settings,
#         "author": "piai-team",
#         "github": "https://github.com/cevheri/pyfapi"
#     }
#     return templates.TemplateResponse("index.html", context)


async def get_root_page_from_readme(request: Request):
    with open("././README.md") as f:
        readme = f.read()
        html = markdown.markdown(readme, extensions=["markdown.extensions.tables"])
    context = {
        "request": request,
        "app_name": app_settings.APP_NAME,
        "app_url": app_settings.APP_URL,
        "app_description": app_settings.APP_DESCRIPTION,
        "app_version": app_settings.APP_VERSION,
        "server_settings": server_settings,
        "author": "piai-team",
        "github": "https://github.com/cevheri/pyfapi",
        "readme_content": html
    }
    return templates.TemplateResponse("index.html", context)


@app.get("/")
async def root(request: Request):
    return await get_root_page_from_readme(request)


@app.get("/api/v1/")
async def root_base_path(request: Request):
    return await get_root_page_from_readme(request)


@app.get("/api/v1/health")
async def health():
    return {"status": "UP"}
