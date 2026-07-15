from app.crud.context import (
    get_incident,
    get_context_findings,
    get_context_runtime_events,
    get_context_policy_decisions,
)


def build_incident_context(
    db,
    incident_id,
):

    incident = get_incident(
        db,
        incident_id,
    )

    findings = get_context_findings(
        db,
        incident,
    )

    runtime_events = get_context_runtime_events(
        db,
        incident,
    )

    policy_decisions = get_context_policy_decisions(
        db,
        incident,
    )

    return {
        "findings": findings,
        "runtime_events": runtime_events,
        "policy_decisions": policy_decisions,
    }