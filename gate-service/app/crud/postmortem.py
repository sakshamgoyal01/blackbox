from uuid import UUID

from sqlalchemy.orm import Session

from app.db.models.incident import Incident
from app.db.models.incident_timeline_entry import IncidentTimelineEntry


def get_incident(
    db: Session,
    incident_id: UUID,
):
    return (
        db.query(Incident)
        .filter(Incident.id == incident_id)
        .first()
    )


def get_timeline(
    db: Session,
    incident_id: UUID,
):
    return (
        db.query(IncidentTimelineEntry)
        .filter(
            IncidentTimelineEntry.incident_id == incident_id
        )
        .order_by(
            IncidentTimelineEntry.created_at
        )
        .all()
    )


def save_postmortem(
    db: Session,
    incident: Incident,
    markdown: str,
):
    incident.postmortem = markdown

    db.commit()

    db.refresh(incident)

    return incident