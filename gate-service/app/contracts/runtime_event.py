from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel


class FalcoRuntimeEvent(BaseModel):

    hostname: str

    rule: str

    priority: str

    output: str

    source: str

    time: datetime

    output_fields: dict[str, Any]


class RuntimeEventResponse(BaseModel):

    id: UUID

    rule: str

    priority: str

    output: str

    container_id: str | None

    container_name: str | None

    pod_name: str | None

    namespace: str | None

    node: str | None

    k8s_labels: dict[str, Any] | None

    service: str | None

    source: str

    detected_at: datetime

    status: str

    class Config:
        from_attributes = True


class RuntimeEventListResponse(BaseModel):

    runtime_events: list[RuntimeEventResponse]