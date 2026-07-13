package blackbox

severity_rank := {
    "info": 0,
    "low": 1,
    "medium": 2,
    "high": 3,
    "critical": 4,
}

tier_threshold := {
    "critical": 1,
    "standard": 2,
    "experimental": 3,
}

#
# Severity-based violation
#
violations contains {
    "reason": "Severity threshold exceeded",
    "finding": finding.title,
    "severity": finding.severity,
    "cve": finding.cve_id,
} if {

    finding := input.findings[_]

    finding.status == "open"

    severity_rank[finding.severity] >
        tier_threshold[input.tier]
}

#
# KEV-based violation
#
violations contains {
    "reason": "Known Exploited Vulnerability",
    "finding": finding.title,
    "severity": finding.severity,
    "cve": finding.cve_id,
} if {

    finding := input.findings[_]

    finding.status == "open"

    finding.kev_listed
}

#
# Final gate decision
#
default allow := false
allow if {
    count(violations) == 0
}