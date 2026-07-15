from uuid import UUID

from sqlalchemy.orm import Session

from app.db.models.incident import (
    Incident,
    IncidentStatus,
    IncidentSeverity,
)

from app.db.models.incident_timeline_entry import (
    IncidentTimelineEntry,
    IncidentTimelineEntryType,
)

def create_incident(
    db: Session,
    incident: Incident,
):
    db.add(incident)
    db.commit()
    db.refresh(incident)
    return incident


def get_incident(
    db: Session,
    incident_id: UUID,
):
    return (
        db.query(Incident)
        .filter(Incident.id == incident_id)
        .first()
    )


def list_incidents(
    db: Session,
    service: str | None = None,
    status=None,
):
    query = db.query(Incident)

    if service:
        query = query.filter(
            Incident.service == service
        )

    if status:
        query = query.filter(
            Incident.status == status
        )

    return (
        query.order_by(
            Incident.opened_at.desc()
        )
        .all()
    )


def update_incident(
    db: Session,
    incident: Incident,
):
    db.add(incident)
    db.commit()
    db.refresh(incident)
    return incident


def create_timeline_entry(
    db: Session,
    entry: IncidentTimelineEntry,
):
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


def list_timeline_entries(
    db: Session,
    incident_id: UUID,
):
    return (
        db.query(
            IncidentTimelineEntry
        )
        .filter(
            IncidentTimelineEntry.incident_id
            == incident_id
        )
        .order_by(
            IncidentTimelineEntry.created_at
        )
        .all()
    )