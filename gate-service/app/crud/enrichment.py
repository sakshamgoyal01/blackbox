from datetime import datetime

from sqlalchemy.orm import Session

from app.db.models.finding import Finding


# ==========================================================
# EPSS
# ==========================================================

def get_pending_epss_findings(
    db: Session,
    service: str | None = None,
    commit_sha: str | None = None,
) -> list[Finding]:

    query = db.query(Finding).filter(
        Finding.cve_id.isnot(None),
        Finding.epss_score.is_(None),
    )

    if service:
        query = query.filter(
            Finding.service == service
        )

    if commit_sha:
        query = query.filter(
            Finding.commit_sha == commit_sha
        )

    return query.all()


def update_epss_score(
    db: Session,
    finding: Finding,
    score: float,
) -> None:

    finding.epss_score = score

    db.add(finding)


# ==========================================================
# KEV
# ==========================================================

def get_pending_kev_findings(
    db: Session,
    service: str | None = None,
    commit_sha: str | None = None,
) -> list[Finding]:

    query = db.query(Finding).filter(
        Finding.cve_id.isnot(None),
        Finding.kev_listed.is_(False),
    )

    if service:
        query = query.filter(
            Finding.service == service
        )

    if commit_sha:
        query = query.filter(
            Finding.commit_sha == commit_sha
        )

    return query.all()


def update_kev_status(
    db: Session,
    finding: Finding,
    kev: bool,
) -> None:

    finding.kev_listed = kev

    db.add(finding)


# ==========================================================
# Priority
# ==========================================================

def get_priority_candidates(
    db: Session,
    service: str | None = None,
    commit_sha: str | None = None,
) -> list[Finding]:

    query = db.query(Finding)

    if service:
        query = query.filter(
            Finding.service == service
        )

    if commit_sha:
        query = query.filter(
            Finding.commit_sha == commit_sha
        )

    return query.all()


def update_priority_score(
    db: Session,
    finding: Finding,
    score: float,
) -> None:

    finding.priority_score = score

    db.add(finding)


# ==========================================================
# Enrichment State
# ==========================================================

def mark_enriched(
    db: Session,
    service: str | None = None,
    commit_sha: str | None = None,
) -> int:

    query = db.query(Finding).filter(
        Finding.enriched_at.is_(None)
    )

    if service:
        query = query.filter(
            Finding.service == service
        )

    if commit_sha:
        query = query.filter(
            Finding.commit_sha == commit_sha
        )

    findings = query.all()

    now = datetime.utcnow()

    for finding in findings:
        finding.enriched_at = now
        db.add(finding)

    return len(findings)


def reset_enrichment(
    db: Session,
    service: str | None = None,
    commit_sha: str | None = None,
) -> int:

    query = db.query(Finding)

    if service:
        query = query.filter(
            Finding.service == service
        )

    if commit_sha:
        query = query.filter(
            Finding.commit_sha == commit_sha
        )

    findings = query.all()

    for finding in findings:

        finding.epss_score = None
        finding.kev_listed = False
        finding.priority_score = None
        finding.enriched_at = None

        db.add(finding)

    commit(db)

    return len(findings)


# ==========================================================
# Commit
# ==========================================================
def get_duplicate_candidates(
    db: Session,
    service: str | None = None,
    commit_sha: str | None = None,
) -> list[Finding]:

    query = db.query(Finding).filter(
        Finding.cve_id.isnot(None),
        Finding.status == "open",
    )

    if service:
        query = query.filter(
            Finding.service == service
        )

    if commit_sha:
        query = query.filter(
            Finding.commit_sha == commit_sha
        )

    return query.all()


def suppress_duplicate(
    db: Session,
    finding: Finding,
) -> None:

    finding.status = "suppressed"

    db.add(finding)
def commit(db: Session) -> None:
    db.commit()