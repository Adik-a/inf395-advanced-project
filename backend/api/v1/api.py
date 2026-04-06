from fastapi import APIRouter

from api.v1.routes import login as login_router
from api.v1.routes import registration as registration_router


router = APIRouter()

router.include_router(login_router.router)
router.include_router(registration_router.router)