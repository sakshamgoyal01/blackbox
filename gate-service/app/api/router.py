from fastapi import APIRouter

from app.api.health import router as health_router
from app.api.services import router as services_router
from app.api.findings import router as findings_router
from app.api.gate import router as gate_router

router = APIRouter()

router.include_router(health_router)
router.include_router(services_router)
router.include_router(findings_router)
router.include_router(gate_router)


