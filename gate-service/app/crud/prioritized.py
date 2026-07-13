from sqlalchemy.orm import Session

from app.db.models.finding import Finding
from app.db.models.finding import FindingStatus


def get_prioritized_findings(
    db: Session,
    service: str,
) -> list[Finding]:

    return (
        db.query(Finding)
        .filter(
            Finding.service == service,
            Finding.status == FindingStatus.open,
        )
        .order_by(
            Finding.priority_score.desc().nullslast(),
            Finding.severity.desc(),
        )
        .all()
    )