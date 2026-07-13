from pydantic import BaseModel


class GateViolation(BaseModel):
    finding: str
    severity: str
    reason: str
    cve: str | None = None

    # Phase 2 enrichment
    priority_score: float | None = None
    epss_score: float | None = None
    kev_listed: bool = False


class GateEvaluationResponse(BaseModel):
    allowed: bool
    tier: str
    violations: list[GateViolation]