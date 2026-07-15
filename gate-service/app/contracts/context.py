from datetime import datetime
from typing import Any
from uuid import UUID
from pydantic import BaseModel


class ContextFinding(BaseModel):
    id: UUID
    title: str
    severity: str
    priority_score: int | None


class ContextRuntimeEvent(BaseModel):
    id: UUID
    rule: str
    priority: str
    output: str
    detected_at: datetime


class ContextPolicyDecision(BaseModel):
    id: UUID
    commit_sha: str
    allowed: bool
    tier_at_decision: str
    decided_at: datetime
    overridden: bool
    violations: list[Any]


class IncidentContextResponse(BaseModel):
    findings: list[ContextFinding]
    runtime_events: list[ContextRuntimeEvent]
    policy_decisions: list[ContextPolicyDecision]