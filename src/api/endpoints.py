import fastapi

from src.api.routes.job import router as job_router
from src.api.routes.authentication import router as authentication_router
from src.api.routes.applications import router as application_router

router = fastapi.APIRouter()

router.include_router(router=authentication_router)
router.include_router(router=job_router)
router.include_router(router=application_router)