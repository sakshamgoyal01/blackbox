from pydantic import BaseModel


class GateEvaluationRequest(BaseModel):
    service: str
    commit_sha: str