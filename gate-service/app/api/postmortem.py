from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.auth import verify_api_key
from app.contracts.postmortem import (
    PostmortemResponse,
)
from app.db.session import get_db
from app.services.postmortem_service import (
    draft_postmortem,
)

router = APIRouter(
    prefix="/incidents",
    tags=["Postmortem"],
)


@router.post(
    "/{incident_id}/postmortem/draft",
    response_model=PostmortemResponse,
    dependencies=[Depends(verify_api_key)],
)
def generate_postmortem(
    incident_id: UUID,
    db: Session = Depends(get_db),
):
    return draft_postmortem(
        db,
        incident_id,
    )