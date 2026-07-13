from dataclasses import dataclass


@dataclass(slots=True)
class EPSSResult:
    cve: str
    epss: float
    percentile: float
    date: str