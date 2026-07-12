from pydantic import BaseModel

from app.contracts.finding import CanonicalFinding


class CreateFindingsRequest(BaseModel):
    findings: list[CanonicalFinding]