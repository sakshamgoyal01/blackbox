from datetime import datetime, timezone

from app.contracts.finding import (
    CanonicalFinding,
    FindingCategory,
    FindingSeverity,
    SourceTool,
)
from app.normalize.base import BaseAdapter


class GitleaksAdapter(BaseAdapter):

    def normalize(
        self,
        raw_json: list,
        service: str,
        commit_sha: str,
        environment: str,
    ) -> list[CanonicalFinding]:

        findings: list[CanonicalFinding] = []

        for secret in raw_json:

            findings.append(
                CanonicalFinding(
                    source_tool=SourceTool.gitleaks,
                    category=FindingCategory.secret,
                    severity=FindingSeverity.critical,
                    cve_id=None,
                    title=secret.get("RuleID", "Secret Detected"),
                    description=secret.get("Description", ""),
                    file_path=secret.get("File"),
                    line_number=secret.get("StartLine"),
                    package_name=None,
                    package_version=None,
                    fixed_version=None,
                    service=service,
                    commit_sha=commit_sha,
                    environment=environment,
                    detected_at=datetime.now(timezone.utc),
                    raw_scanner_output=secret,
                )
            )

        return findings