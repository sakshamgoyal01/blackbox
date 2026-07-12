from pydantic import BaseModel

from app.contracts.finding import CanonicalFinding


class FindingsCreatedResponse(BaseModel):
    inserted: int


class FindingsListResponse(BaseModel):
    findings: list[CanonicalFinding]