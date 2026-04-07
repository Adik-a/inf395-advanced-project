from fastapi import APIRouter

from api.v1.routes import authentication as auth_router
from api.v1.routes import users as users_router


router = APIRouter()

router.include_router(auth_router.router)
router.include_router(users_router.router)
