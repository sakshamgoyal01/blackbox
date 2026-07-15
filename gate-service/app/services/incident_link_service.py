from fastapi import HTTPException

from app.contracts.incident_link import IncidentLinkRequest
from app.crud.incident_link import (
    create_timeline_entry,
    get_finding,
    get_incident,
    get_runtime_event,
)
from app.db.models.incident_timeline_entry import (
    IncidentTimelineEntry,
    IncidentTimelineEntryType,
)


def link_object(
    db,
    incident_id,
    request: IncidentLinkRequest,
):

    incident = get_incident(
        db,
        incident_id,
    )

    if incident is None:
        raise HTTPException(
            status_code=404,
            detail="Incident not found",
        )

    if request.type == "finding":

        finding = get_finding(
            db,
            request.id,
        )

        if finding is None:
            raise HTTPException(
                status_code=404,
                detail="Finding not found",
            )

        entry_type = IncidentTimelineEntryType.finding_linked

        timeline_content = f"""
        Finding linked

        Title: {finding.title}
        Severity: {finding.severity.value.capitalize()}
        Priority Score: {finding.priority_score if finding.priority_score is not None else "N/A"}
        KEV Listed: {"Yes" if finding.kev_listed else "No"}
        CVE: {finding.cve_id if finding.cve_id else "N/A"}
        Scanner: {finding.source_tool.value.capitalize()}
        Service: {finding.service}
        """.strip()

    else:

        runtime_event = get_runtime_event(
            db,
            request.id,
        )

        if runtime_event is None:
            raise HTTPException(
                status_code=404,
                detail="Runtime event not found",
            )

        entry_type = IncidentTimelineEntryType.runtime_event_linked

        timeline_content = f"""
        Runtime event linked

        Rule: {runtime_event.rule}
        Priority: {runtime_event.priority}
        MITRE ATT&CK: {runtime_event.mitre_attack if runtime_event.mitre_attack else "N/A"}
        Container: {runtime_event.container_name if runtime_event.container_name else "N/A"}
        Namespace: {runtime_event.namespace if runtime_event.namespace else "N/A"}
        Service: {runtime_event.service if runtime_event.service else "N/A"}
        """.strip()

    entry = IncidentTimelineEntry(
        incident_id=incident.id,
        entry_type=entry_type,
        content=timeline_content,
    )

    return create_timeline_entry(
        db,
        entry,
    )