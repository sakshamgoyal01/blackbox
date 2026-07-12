from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth import verify_api_key
from app.contracts.gate_requests import GateEvaluationRequest
from app.contracts.gate_responses import GateEvaluationResponse
from app.crud.findings import get_findings_by_service_commit
from app.crud.policy_decisions import create_policy_decision
from app.db.models.service import Service
from app.db.session import get_db
from app.services.gate import evaluate_gate

router = APIRouter(
    prefix="/gate",
    tags=["Gate"],
)


@router.post(
    "/evaluate",
    response_model=GateEvaluationResponse,
)
def evaluate(
    request: GateEvaluationRequest,
    db: Session = Depends(get_db),
    _: str = Depends(verify_api_key),
):

    service = (
        db.query(Service)
        .filter(Service.name == request.service)
        .first()
    )

    if service is None:
        raise HTTPException(
            status_code=404,
            detail="Service not found",
        )

    findings = get_findings_by_service_commit(
        db,
        request.service,
        request.commit_sha,
    )

    allowed, violations = evaluate_gate(
        service,
        findings,
    )

    create_policy_decision(
        db=db,
        service=request.service,
        commit_sha=request.commit_sha,
        allowed=allowed,
        violations=violations,
        tier=service.criticality_tier.value,
    )

    return GateEvaluationResponse(
        allowed=allowed,
        tier=service.criticality_tier.value,
        violations=violations,
    )