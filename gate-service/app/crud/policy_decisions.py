from sqlalchemy.orm import Session

from app.db.models.policy_decision import PolicyDecision


def create_policy_decision(
    db: Session,
    *,
    service: str,
    commit_sha: str,
    allowed: bool,
    violations: list,
    tier: str,
    policy_name: str | None = None,
    policy_description: str | None = None,
    recommendation: str | None = None,
    documentation_url: str | None = None,
    evaluated_resource: str | None = None,
    metadata: dict | None = None,
) -> PolicyDecision:
    decision = PolicyDecision(
        service=service,
        commit_sha=commit_sha,
        allowed=allowed,
        violations=violations,
        tier_at_decision=tier,

        policy_name=policy_name,
        policy_description=policy_description,
        recommendation=recommendation,
        documentation_url=documentation_url,
        evaluated_resource=evaluated_resource,
        policy_metadata=metadata,
    )

    db.add(decision)
    db.commit()
    db.refresh(decision)

    return decision