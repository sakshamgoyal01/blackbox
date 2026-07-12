from pydantic import BaseModel


class GateEvaluationResponse(BaseModel):
    allowed: bool
    tier: str
    violations: list[dict]