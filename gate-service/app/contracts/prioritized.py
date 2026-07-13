from pydantic import BaseModel


class PrioritizedFinding(BaseModel):
    finding_id: str
    title: str
    severity: str
    cve_id: str | None
    epss_score: float | None
    kev_listed: bool
    priority_score: float | None


class PrioritizedFindingsResponse(BaseModel):
    findings: list[PrioritizedFinding]