from uuid import UUID

from sqlalchemy.orm import Session

from app.db.models.incident import Incident
from app.db.models.incident_timeline_entry import IncidentTimelineEntry
from app.db.models.finding import Finding
from app.db.models.runtime_event import RuntimeEvent


def get_incident(
    db: Session,
    incident_id: UUID,
):
    return (
        db.query(Incident)
        .filter(Incident.id == incident_id)
        .first()
    )


def get_finding(
    db: Session,
    finding_id: UUID,
):
    return (
        db.query(Finding)
        .filter(Finding.finding_id == finding_id)
        .first()
    )


def get_runtime_event(
    db: Session,
    runtime_event_id: UUID,
):
    return (
        db.query(RuntimeEvent)
        .filter(RuntimeEvent.id == runtime_event_id)
        .first()
    )


def create_timeline_entry(
    db: Session,
    entry: IncidentTimelineEntry,
):
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry