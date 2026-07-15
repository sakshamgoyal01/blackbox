from datetime import timedelta

from sqlalchemy.orm import Session

from app.db.models.finding import Finding
from app.db.models.runtime_event import RuntimeEvent
from app.db.models.policy_decision import PolicyDecision
from app.db.models.incident import Incident


def get_incident(db: Session, incident_id):
    return (
        db.query(Incident)
        .filter(Incident.id == incident_id)
        .first()
    )


def get_context_findings(db: Session, incident: Incident):

    return (
        db.query(Finding)
        .filter(
            Finding.service == incident.service,
            Finding.status == "open",
        )
        .order_by(
            Finding.priority_score.desc()
        )
        .all()
    )


def get_context_runtime_events(db: Session, incident: Incident):

    start = incident.opened_at - timedelta(hours=24)

    return (
        db.query(RuntimeEvent)
        .filter(
            RuntimeEvent.service == incident.service,
            RuntimeEvent.detected_at >= start,
            RuntimeEvent.detected_at <= incident.opened_at,
        )
        .order_by(
            RuntimeEvent.detected_at.desc()
        )
        .all()
    )


def get_context_policy_decisions(
    db: Session,
    incident: Incident,
):

    start = incident.opened_at - timedelta(days=7)

    return (
        db.query(PolicyDecision)
        .filter(
            PolicyDecision.service == incident.service,
            PolicyDecision.decided_at >= start,
            PolicyDecision.decided_at <= incident.opened_at,
        )
        .order_by(
            PolicyDecision.decided_at.desc()
        )
        .all()
    )