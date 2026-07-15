
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth import verify_api_key
from app.contracts.runtime_event import (
    FalcoRuntimeEvent,
    RuntimeEventListResponse,
    RuntimeEventResponse,
)
from app.db.session import get_db
from app.services.runtime_event_service import (
    get_runtime_events,
    store_runtime_event,
)

router = APIRouter(
    prefix="/runtime-events",
    tags=["Runtime Events"],
)


@router.post(
    "",
    response_model=RuntimeEventResponse,
    dependencies=[Depends(verify_api_key)],
)
def ingest_runtime_event(
    event: FalcoRuntimeEvent,
    db: Session = Depends(get_db),
):
    return store_runtime_event(
        db,
        event,
    )


@router.get(
    "",
    response_model=RuntimeEventListResponse,
    dependencies=[Depends(verify_api_key)],
)
def list_events(
    service: str | None = None,
    priority: str | None = None,
    db: Session = Depends(get_db),
):

    events = get_runtime_events(
        db,
        service,
        priority,
    )

    return {
        "runtime_events": events,
    }