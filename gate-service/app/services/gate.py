from app.db.models.finding import Finding
from app.db.models.service import Service
from app.services.opa import evaluate_policy


def evaluate_gate(
    service: Service,
    findings: list[Finding],
) -> tuple[bool, list[dict]]:
    """
    Evaluate deployment policy using OPA.
    """

    finding_payload = []

    for finding in findings:
        finding_payload.append(
            {
                "title": finding.title,
                "severity": (
                    finding.severity.value
                    if hasattr(finding.severity, "value")
                    else finding.severity
                ),
                "status": (
                    finding.status.value
                    if hasattr(finding.status, "value")
                    else finding.status
                ),
            }
        )

    return evaluate_policy(
        tier=(
            service.criticality_tier.value
            if hasattr(service.criticality_tier, "value")
            else service.criticality_tier
        ),
        findings=finding_payload,
    )