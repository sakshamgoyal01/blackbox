from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.db.models.incident import (
    IncidentSeverity,
    IncidentStatus,
    IncidentType,
)

from app.db.models.incident_timeline_entry import (
    IncidentTimelineEntryType,
)


class IncidentCreate(BaseModel):
    title: str
    service: str | None = None
    severity: IncidentSeverity

    incident_type: IncidentType = IncidentType.runtime
    root_cause_category: str | None = None
    tags: list[str] | None = None


class IncidentUpdate(BaseModel):
    severity: IncidentSeverity | None = None
    status: IncidentStatus | None = None
    summary: str | None = None
    postmortem: str | None = None

    incident_type: IncidentType | None = None
    root_cause_category: str | None = None
    tags: list[str] | None = None


class IncidentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    service: str | None

    severity: IncidentSeverity
    status: IncidentStatus

    incident_type: IncidentType
    root_cause_category: str | None
    tags: list[str] | None

    opened_at: datetime
    resolved_at: datetime | None

    opened_by: str

    summary: str | None
    postmortem: str | None


class IncidentTimelineEntryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    incident_id: UUID
    entry_type: IncidentTimelineEntryType
    content: str
    created_at: datetime


class IncidentDetailResponse(BaseModel):
    incident: IncidentResponse
    timeline: list[IncidentTimelineEntryResponse]


class IncidentListResponse(BaseModel):
    incidents: list[IncidentResponse]