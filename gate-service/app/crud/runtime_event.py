from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.runtime_event import RuntimeEvent
from app.db.models.service import Service


def create_runtime_event(
    db: Session,
    runtime_event: RuntimeEvent,
) -> RuntimeEvent:
    db.add(runtime_event)
    db.commit()
    db.refresh(runtime_event)
    return runtime_event


def get_service_by_namespace(
    db: Session,
    namespace: str | None,
) -> Service | None:

    if namespace is None:
        return None

    return (
        db.execute(
            select(Service).where(
                Service.k8s_namespace == namespace
            )
        )
        .scalar_one_or_none()
    )


def list_runtime_events(
    db: Session,
    service: str | None = None,
    priority: str | None = None,
):

    query = select(RuntimeEvent)

    if service:
        query = query.where(RuntimeEvent.service == service)

    if priority:
        query = query.where(RuntimeEvent.priority == priority)

    query = query.order_by(RuntimeEvent.detected_at.desc())

    return db.execute(query).scalars().all()