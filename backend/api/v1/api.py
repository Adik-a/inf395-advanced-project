from fastapi import APIRouter

from api.v1.routes import authentication as auth_router


router = APIRouter()

router.include_router(auth_router.router)