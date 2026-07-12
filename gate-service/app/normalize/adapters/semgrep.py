from datetime import datetime, timezone

from app.contracts.finding import (
    CanonicalFinding,
    FindingCategory,
    FindingSeverity,
    SourceTool,
)
from app.normalize.base import BaseAdapter


SEVERITY_MAP = {
    "ERROR": FindingSeverity.critical,
    "WARNING": FindingSeverity.high,
    "INFO": FindingSeverity.low,
}


class SemgrepAdapter(BaseAdapter):

    def normalize(
        self,
        raw_json: dict,
        service: str,
        commit_sha: str,
        environment: str,
    ) -> list[CanonicalFinding]:

        findings: list[CanonicalFinding] = []

        for result in raw_json.get("results", []):

            extra = result.get("extra", {})

            findings.append(
                CanonicalFinding(
                    source_tool=SourceTool.semgrep,
                    category=FindingCategory.sast,
                    severity=SEVERITY_MAP.get(
                        extra.get("severity", "INFO").upper(),
                        FindingSeverity.info,
                    ),
                    cve_id=None,
                    title=result.get("check_id", "Semgrep Finding"),
                    description=extra.get("message", ""),
                    file_path=result.get("path"),
                    line_number=result.get("start", {}).get("line"),
                    package_name=None,
                    package_version=None,
                    fixed_version=None,
                    service=service,
                    commit_sha=commit_sha,
                    environment=environment,
                    detected_at=datetime.now(timezone.utc),
                    raw_scanner_output=result,
                )
            )

        return findings