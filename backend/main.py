from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from api.v1.api import router as v1_router
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
    lifespan=lifespan,
)

origins = [
    "http://127.0.0.1:5500",
    "http://localhost:5500",
    # добавь другие адреса, если используешь их
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # Разрешает запросы с твоего фронтенда
    allow_credentials=True,
    allow_methods=["*"],              # Разрешает все методы (GET, POST и т.д.)
    allow_headers=["*"],              # Разрешает все заголовки
)

app.include_router(v1_router)
