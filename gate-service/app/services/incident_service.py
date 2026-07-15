from datetime import datetime, timezone

from app.contracts.incident import (
    IncidentCreate,
    IncidentUpdate,
)

from app.crud.incident import (
    create_incident,
    create_timeline_entry,
    get_incident,
    list_incidents,
    list_timeline_entries,
    update_incident,
)

from app.db.models.incident import (
    Incident,
    IncidentSeverity,
    IncidentStatus,
)

from app.db.models.incident_timeline_entry import (
    IncidentTimelineEntry,
    IncidentTimelineEntryType,
)


def create_incident_service(
    db,
    request: IncidentCreate,
):
    incident = Incident(
        title=request.title,
        service=request.service,
        severity=request.severity,
        status=IncidentStatus.open,
        opened_by="manual",

        incident_type=request.incident_type,

        root_cause_category=request.root_cause_category,

        tags=request.tags,
    )

    return create_incident(
        db,
        incident,
    )


def get_incident_service(
    db,
    incident_id,
):

    incident = get_incident(
        db,
        incident_id,
    )

    if incident is None:
        return None

    return {
        "incident": incident,
        "timeline": list_timeline_entries(
            db,
            incident_id,
        ),
    }


def list_incidents_service(
    db,
    service=None,
    status=None,
):

    return list_incidents(
        db,
        service,
        status,
    )


def update_incident_service(
    db,
    incident_id,
    request: IncidentUpdate,
):

    incident = get_incident(
        db,
        incident_id,
    )

    if incident is None:
        return None

    previous_status = incident.status

    if request.severity is not None:
        incident.severity = request.severity

    if request.incident_type is not None:
        incident.incident_type = request.incident_type

    if request.summary is not None:
        incident.summary = request.summary

    if request.root_cause_category is not None:
        incident.root_cause_category = request.root_cause_category
    if request.tags is not None:
        incident.tags = request.tags

    if request.postmortem is not None:
        incident.postmortem = request.postmortem

    status_changed = False

    if request.status is not None:

        if request.status != incident.status:
            status_changed = True

        incident.status = request.status

        if request.status == IncidentStatus.resolved:
            incident.resolved_at = datetime.now(
                timezone.utc
            )
        else:
            incident.resolved_at = None

    update_incident(
        db,
        incident,
    )

    if status_changed:

        timeline = IncidentTimelineEntry(
            incident_id=incident.id,
            entry_type=IncidentTimelineEntryType.status_change,
            content=f"""
            Manual status update

            Previous Status: {previous_status.value}

            Current Status: {incident.status.value}
            """.strip(),
        )

        create_timeline_entry(
            db,
            timeline,
        )

    return incident