from enum import Enum
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel


class IncidentLinkType(str, Enum):
    finding = "finding"
    runtime_event = "runtime_event"


class IncidentLinkRequest(BaseModel):
    type: IncidentLinkType
    id: UUID


class IncidentTimelineEntryResponse(BaseModel):
    id: UUID
    incident_id: UUID
    entry_type: str
    content: str
    created_at: datetime

    model_config = {
        "from_attributes": True,
    }