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

violations contains finding if {
    finding := input.findings[_]
    finding.status == "open"
    severity_rank[finding.severity] > tier_threshold[input.tier]
}

allow := count(violations) == 0