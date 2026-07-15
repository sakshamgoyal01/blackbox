from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth import verify_api_key
from app.contracts.incident_link import (
    IncidentLinkRequest,
    IncidentTimelineEntryResponse,
)
from app.db.session import get_db
from app.services.incident_link_service import (
    link_object,
)

router = APIRouter(
    prefix="/incidents",
    tags=["Incident Linking"],
)


@router.post(
    "/{incident_id}/link",
    response_model=IncidentTimelineEntryResponse,
    dependencies=[Depends(verify_api_key)],
)
def link_incident(
    incident_id: UUID,
    request: IncidentLinkRequest,
    db: Session = Depends(get_db),
):

    return link_object(
        db,
        incident_id,
        request,
    )