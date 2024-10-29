import logging
from contextlib import asynccontextmanager

import markdown
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates

from app import init_db, api
from app.conf.app_settings import cors_settings, server_settings, app_settings
from app.middleware.security_middleware import SecurityMiddleware
from app.migration import user_migration

print("app.main.py is running")

log = logging.getLogger(__name__)

templates = Jinja2Templates(directory="././templates")


@asynccontextmanager
async def lifespan(_):
    log.debug("FastAPI Lifespan started")
    await init_db()
    await user_migration.init_migration()
    yield


tags_metadata = [
    {
        "name": "auth",
        "description": "Operations with authentication. The **login** endpoint returns the access token."
    },
    {
        "name": "account",
        "description": "Operations with account. The **account** endpoint returns the account information."
    },
    {
        "name": "users",
        "description": "Operations with users. The **users** endpoint returns the user information."
    }
]
servers_metadata = [
        {
            "url": app_settings.APP_URL,
            "description": "Production server"
        },
        {
            "url": "http://localhost:8000",
            "description": "Local server"
        }
    ]
app = FastAPI(
    title="PyFAPI",
    summary="Python FastAPI mongodb Application",
    description="Python FastAPI mongodb app for Enterprise usage with best practices, tools, and more.",
    version="1.0.0",
    docs_url=f"{server_settings.CONTEXT_PATH}/docs",
    redoc_url=f"{server_settings.CONTEXT_PATH}/redoc",
    openapi_url=f"{server_settings.CONTEXT_PATH}/openapi.json",
    lifespan=lifespan,
    openapi_tags=tags_metadata,
    contact={
        "name": f"{app_settings.APP_NAME} Team",
        "url": "https://github.com/cevheri",
        "email": "cevheribozoglan@gmail.com"
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://github.com/cevheri/pyfapi/blob/main/LICENSE"
    },
    terms_of_service="https://example.com/terms/",
    servers=servers_metadata
)

# noinspection PyTypeChecker
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_settings.ALLOWED_ORIGINS,
    allow_credentials=cors_settings.ALLOW_CREDENTIALS,
    allow_methods=cors_settings.ALLOWED_METHODS,
    allow_headers=cors_settings.ALLOWED_HEADERS
)
# noinspection PyTypeChecker
app.add_middleware(SecurityMiddleware)
app.include_router(api.auth_router)
app.include_router(api.account_router)
app.include_router(api.user_router)


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
        "author": "cevheri",
        "github": "https://github.com/cevheri/pyfapi",
        "readme_content": html
    }
    return templates.TemplateResponse("index.html", context)


@app.get("/")
async def root(request: Request):
    return await get_root_page_from_readme(request)


@app.get("/api/v1")
async def root_base_path(request: Request):
    return await get_root_page_from_readme(request)


@app.get("/api/v1/health")
async def health():
    return {"status": "UP"}
