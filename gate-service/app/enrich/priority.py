from __future__ import annotations

SEVERITY_RANK = {
    "critical": 4,
    "high": 3,
    "medium": 2,
    "low": 1,
    "info": 0,
}


def calculate_priority(
    severity: str,
    epss_score: float | None,
    kev_listed: bool,
) -> float:
    """
    BLACKBOX Phase 2 priority formula.

    priority_score =
        (severity_rank * 10)
        + (epss_score * 40 if epss_score else 0)
        + (30 if kev_listed else 0)
    """

    severity_value = SEVERITY_RANK.get(
        severity.lower(),
        0,
    )

    score = severity_value * 10

    if epss_score is not None:
        score += epss_score * 40

    if kev_listed:
        score += 30

    return round(score, 2)