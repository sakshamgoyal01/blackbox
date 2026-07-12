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
) -> PolicyDecision:

    decision = PolicyDecision(
        service=service,
        commit_sha=commit_sha,
        allowed=allowed,
        violations=violations,
        tier_at_decision=tier,
    )

    db.add(decision)
    db.commit()
    db.refresh(decision)

    return decision