from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.auth import verify_api_key
from app.contracts.context import IncidentContextResponse
from app.db.session import get_db
from app.services.context_service import build_incident_context

router = APIRouter(
    tags=["Incident Context"],
)


@router.get(
    "/incidents/{incident_id}/context",
    response_model=IncidentContextResponse,
    dependencies=[Depends(verify_api_key)],
)
def incident_context(
    incident_id: UUID,
    db: Session = Depends(get_db),
):

    return build_incident_context(
        db,
        incident_id,
    )