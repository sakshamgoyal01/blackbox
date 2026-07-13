from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.auth import verify_api_key
from app.contracts.enrichment import (
    EnrichmentRequest,
    EnrichmentResponse,
)
from app.db.session import get_db
from app.services.enrichment import EPSSEnrichmentService

router = APIRouter(
    tags=["Enrichment"],
)


@router.post(
    "/findings/enrich",
    response_model=EnrichmentResponse,
    dependencies=[Depends(verify_api_key)],
)
def enrich_findings(
    request: EnrichmentRequest,
    db: Session = Depends(get_db),
):

    result = EPSSEnrichmentService().enrich_all(
        db=db,
        service=request.service,
        commit_sha=request.commit_sha,
    )

    return EnrichmentResponse(**result)