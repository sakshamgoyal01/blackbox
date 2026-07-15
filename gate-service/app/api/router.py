from fastapi import APIRouter

from app.api.health import router as health_router
from app.api.services import router as services_router
from app.api.findings import router as findings_router
from app.api.gate import router as gate_router
from app.api.enrichment import router as enrichment_router
from app.api.prioritized import ( router as prioritized_router,)
from app.api.runtime_events import router as runtime_events_router
from app.api.incidents import router as incident_router
from app.api.context import router as context_router
from app.api.incident_link import router as incident_link_router
from app.api.postmortem import (router as postmortem_router,)

router = APIRouter()

router.include_router(health_router)
router.include_router(services_router)
router.include_router(findings_router)
router.include_router(gate_router)
router.include_router(enrichment_router)
router.include_router(prioritized_router,)
router.include_router(runtime_events_router)
router.include_router(
    incident_router
)
router.include_router(context_router)
router.include_router(incident_link_router)
router.include_router(postmortem_router)