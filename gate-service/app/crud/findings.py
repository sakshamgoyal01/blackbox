from sqlalchemy.orm import Session

from app.contracts.finding import CanonicalFinding
from app.db.models.finding import Finding


def insert_findings(
    db: Session,
    findings: list[CanonicalFinding],
) -> int:

    rows = []

    for finding in findings:

        rows.append(
            Finding(
                finding_id=finding.finding_id,
                source_tool=finding.source_tool.value,
                category=finding.category.value,
                severity=finding.severity.value,
                cve_id=finding.cve_id,
                epss_score=finding.epss_score,
                title=finding.title,
                description=finding.description,
                file_path=finding.file_path,
                line_number=finding.line_number,
                package_name=finding.package_name,
                package_version=finding.package_version,
                fixed_version=finding.fixed_version,
                service=finding.service,
                commit_sha=finding.commit_sha,
                environment=finding.environment,
                detected_at=finding.detected_at,
                status=finding.status.value,
                raw_scanner_output=finding.raw_scanner_output,
            )
        )

    db.add_all(rows)
    db.commit()

    return len(rows)


def get_findings_by_service(
    db: Session,
    service: str,
):

    return (
        db.query(Finding)
        .filter(Finding.service == service)
        .all()
    )


def get_findings_by_service_commit(
    db: Session,
    service: str,
    commit_sha: str,
):

    return (
        db.query(Finding)
        .filter(Finding.service == service)
        .filter(Finding.commit_sha == commit_sha)
        .all()
    )