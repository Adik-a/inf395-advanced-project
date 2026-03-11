from fastapi import FastAPI
from routers.login import router as login_router
from routers.registration import router as registration_router

from contextlib import asynccontextmanager
from database import engine, Model

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)

    print("🔰🔗Database is launched🔗🔰")

    yield

    print("🛑🔗Turn off Server🔗🛑")

app = FastAPI(
    title="QWork",
    description="REST API for QWork freelance web-site",
    lifespan=lifespan
)

app.include_router(login_router)
app.include_router(registration_router)