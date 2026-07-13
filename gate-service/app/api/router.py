from fastapi import APIRouter

from app.api.health import router as health_router
from app.api.services import router as services_router
from app.api.findings import router as findings_router
from app.api.gate import router as gate_router
from app.api.enrichment import router as enrichment_router
from app.api.prioritized import ( router as prioritized_router,)
router = APIRouter()

router.include_router(health_router)
router.include_router(services_router)
router.include_router(findings_router)
router.include_router(gate_router)
router.include_router(enrichment_router)
router.include_router(prioritized_router,)
