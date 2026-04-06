from fastapi import FastAPI
from contextlib import asynccontextmanager

from api.v1.api import router as v1_router
from database import engine, Model


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🔰🔗Database is launched🔗🔰")

    yield

    print("🛑🔗Turn off Server🔗🛑")


app = FastAPI(
    title="QWork",
    description="REST API for QWork freelance web-site",
    lifespan=lifespan,
)

app.include_router(v1_router)
