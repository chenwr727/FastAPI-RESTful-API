from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings
from core.database import create_db_and_tables
from core.logging import logger
from routers import item, user


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up application")
    create_db_and_tables()
    logger.info("Database tables created")
    yield
    logger.info("Shutting down application")


app = FastAPI(title=settings.APP_TITLE, version=settings.VERSION, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(item.router, prefix="/items", tags=["items"])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=settings.PORT)
