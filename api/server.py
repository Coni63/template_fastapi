from __future__ import annotations
from contextlib import asynccontextmanager

from api.routes.todo import router, openapi_tag
from app.services.database import Database
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    Database.setup_db()
    yield
    Database.drop_db()
    

description = """
# INFORMATION

Describe what you API is supposed to be used to do.
"""

openapi_tags = [
    openapi_tag,  # add more modules if needed
]

app = FastAPI(
    title="TODO APP",
    description=description,
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Author",
        "url": "https://www.foo.com/contact/",
        "email": "author@example.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    openapi_tags=openapi_tags,
    lifespan=lifespan,
)

app.include_router(router)  # add more modules if needed