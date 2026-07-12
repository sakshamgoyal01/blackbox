from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, HttpUrl

from app.db.models import CriticalityTier
from app.db.models import Environment


class ServiceCreate(BaseModel):
    name: str
    repo_url: HttpUrl
    owner: str
    criticality_tier: CriticalityTier
    environment: Environment


class ServiceResponse(BaseModel):
    id: UUID
    name: str
    repo_url: str
    owner: str
    criticality_tier: CriticalityTier
    environment: Environment
    created_at: datetime

    model_config = {
        "from_attributes": True
    }