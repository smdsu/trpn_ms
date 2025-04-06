import fastapi

from app.api.routes.tron_addresses import router as tron_addresses_router

router = fastapi.APIRouter()

router.include_router(router=tron_addresses_router)
