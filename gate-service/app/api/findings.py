from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.auth import verify_api_key
from app.contracts.requests import CreateFindingsRequest
from app.contracts.responses import (
    FindingsCreatedResponse,
    FindingsListResponse,
)
from app.contracts.finding import CanonicalFinding
from app.crud.findings import (
    get_findings_by_service,
    insert_findings,
)
from app.db.session import get_db

router = APIRouter(
    prefix="/findings",
    tags=["Findings"],
)


@router.post(
    "",
    response_model=FindingsCreatedResponse,
)
def create_findings(
    request: CreateFindingsRequest,
    db: Session = Depends(get_db),
    _: str = Depends(verify_api_key),
):

    inserted = insert_findings(
        db,
        request.findings,
    )

    return FindingsCreatedResponse(
        inserted=inserted,
    )


@router.get(
    "",
    response_model=FindingsListResponse,
)
def list_findings(
    service: str = Query(...),
    db: Session = Depends(get_db),
    _: str = Depends(verify_api_key),
):

    rows = get_findings_by_service(
        db,
        service,
    )

    findings = []

    for row in rows:

        findings.append(
            CanonicalFinding(
                finding_id=row.finding_id,
                source_tool=row.source_tool,
                category=row.category,
                severity=row.severity,
                cve_id=row.cve_id,
                epss_score=row.epss_score,
                title=row.title,
                description=row.description,
                file_path=row.file_path,
                line_number=row.line_number,
                package_name=row.package_name,
                package_version=row.package_version,
                fixed_version=row.fixed_version,
                service=row.service,
                commit_sha=row.commit_sha,
                environment=row.environment,
                detected_at=row.detected_at,
                status=row.status,
                raw_scanner_output=row.raw_scanner_output,
            )
        )

    return FindingsListResponse(
        findings=findings,
    )