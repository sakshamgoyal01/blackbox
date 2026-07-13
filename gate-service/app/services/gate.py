from app.db.models.finding import Finding
from app.db.models.service import Service
from app.services.opa import evaluate_policy


def evaluate_gate(
    service: Service,
    findings: list[Finding],
) -> tuple[bool, list[dict]]:
    """
    Evaluate deployment policy using OPA and enrich returned
    violations with metadata needed by downstream consumers
    (GitHub PR comments, dashboards, APIs).
    """

    finding_payload = []

    finding_lookup = {}

    for finding in findings:

        severity = (
            finding.severity.value
            if hasattr(finding.severity, "value")
            else finding.severity
        )

        status = (
            finding.status.value
            if hasattr(finding.status, "value")
            else finding.status
        )

        payload = {
            "title": finding.title,
            "severity": severity,
            "status": status,
            "cve_id": finding.cve_id,
            "kev_listed": finding.kev_listed,
            "epss_score": finding.epss_score,
            "priority_score": finding.priority_score,
        }

        finding_payload.append(payload)

        finding_lookup[finding.title] = payload

    allowed, violations = evaluate_policy(
        tier=(
            service.criticality_tier.value
            if hasattr(service.criticality_tier, "value")
            else service.criticality_tier
        ),
        findings=finding_payload,
    )

    #
    # Phase 2:
    # Enrich OPA violations with metadata from the original findings.
    #
    for violation in violations:

        payload = finding_lookup.get(
            violation["finding"]
        )

        if payload is None:
            continue

        violation["priority_score"] = payload["priority_score"]
        violation["epss_score"] = payload["epss_score"]
        violation["kev_listed"] = payload["kev_listed"]

    return allowed, violations