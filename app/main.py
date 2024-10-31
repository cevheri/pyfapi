import logging
from contextlib import asynccontextmanager

import markdown
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates

from app.api import api_router
from app.conf.app_settings import app_settings, server_settings, cors_settings
from app.conf.env.db_config import init_db
from app.errors.business_exception import BusinessException
from app.middleware.security_middleware import SecurityMiddleware
from app.migration import user_migration

print("app.main.py is running")

_log = logging.getLogger(__name__)
_templates = Jinja2Templates(directory="././templates")


@asynccontextmanager
async def lifespan(_):
    _log.debug("FastAPI Lifespan started")
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
    title=app_settings.APP_NAME,
    summary=app_settings.APP_DESCRIPTION,
    description=app_settings.APP_DESCRIPTION,
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
app.include_router(api_router)


def write_log(request: Request, exc: BusinessException):
    _log.error(f"BusinessException - Request: {request.method} {request.url.path} failed with {exc.code} {exc.msg}")


@app.exception_handler(BusinessException)
async def business_exception_handler(request: Request, exc: BusinessException):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": {"error_code": f"{status.HTTP_400_BAD_REQUEST}.{exc.code.name}", "error_message": exc.msg}},
        headers={"X-Error": f"{status.HTTP_400_BAD_REQUEST}.{exc.code}"},
        media_type="application/json",
        background=write_log(request, exc),
    )


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

    return _templates.TemplateResponse("index.html", context)


@app.get("/")
async def root(request: Request):
    return await get_root_page_from_readme(request)


@app.get("/api/v1")
async def root_base_path(request: Request):
    return await get_root_page_from_readme(request)


@app.get("/api/v1/health")
async def health():
    return {"status": "UP"}
