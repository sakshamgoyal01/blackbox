from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import get_db

from app.crud.prioritized import (
    get_prioritized_findings,
)

from app.contracts.prioritized import (
    PrioritizedFinding,
    PrioritizedFindingsResponse,
)

router = APIRouter(
    prefix="/findings",
    tags=["Findings"],
)


@router.get(
    "/prioritized",
    response_model=PrioritizedFindingsResponse,
)
def prioritized_findings(
    service: str,
    db: Session = Depends(get_db),
):

    findings = get_prioritized_findings(
        db,
        service,
    )

    return PrioritizedFindingsResponse(
        findings=[
            PrioritizedFinding(
                finding_id=str(f.finding_id),
                title=f.title,
                severity=f.severity.value,
                cve_id=f.cve_id,
                epss_score=f.epss_score,
                kev_listed=f.kev_listed,
                priority_score=f.priority_score,
            )
            for f in findings
        ]
    )