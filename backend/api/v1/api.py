from fastapi import APIRouter

from api.v1.routes.authentication import router as auth_router
from api.v1.routes.users import router as users_router
from api.v1.routes.portfolios import router as portfolios_router
from api.v1.routes.jobs import router as jobs_router
from api.v1.routes.offers import router as offers_router


router = APIRouter()

router.include_router(auth_router)
router.include_router(users_router)
router.include_router(portfolios_router)
router.include_router(jobs_router)
router.include_router(offers_router)
