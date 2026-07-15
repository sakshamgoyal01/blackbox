from datetime import datetime, timezone

from sqlalchemy.orm import Session
from app.contracts.runtime_event import FalcoRuntimeEvent

from app.crud.runtime_event import (
    create_runtime_event,
    get_service_by_namespace,
    list_runtime_events,
)
from app.db.models.runtime_event import RuntimeEvent


def store_runtime_event(
    db,
    event: FalcoRuntimeEvent,
):

    fields = event.output_fields

    namespace = fields.get("k8s.ns.name")

    matched_service = get_service_by_namespace(
        db,
        namespace,
    )

    runtime_event = RuntimeEvent(

        rule=event.rule,

        priority=event.priority,

        output=event.output,

        container_id=fields.get("container.id"),

        container_name=fields.get("container.name"),

        pod_name=fields.get("k8s.pod.name"),

        namespace=namespace,

        node=event.hostname,

        k8s_labels=None,

        service=matched_service.name if matched_service else None,

        source=event.source,

        # NEW
        rule_url=None,
        mitre_attack=None,
        remediation_summary=None,
        investigation_notes=None,

        raw_output=event.model_dump(mode="json"),

        detected_at=event.time,
    )


def get_runtime_events(
    db: Session,
    service: str | None = None,
    priority: str | None = None,
):

    return list_runtime_events(
        db=db,
        service=service,
        priority=priority,
    )