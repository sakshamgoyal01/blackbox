from datetime import datetime, timezone

from app.contracts.finding import (
    CanonicalFinding,
    FindingCategory,
    FindingSeverity,
    SourceTool,
)
from app.normalize.base import BaseAdapter


SEVERITY_MAP = {
    "CRITICAL": FindingSeverity.critical,
    "HIGH": FindingSeverity.high,
    "MEDIUM": FindingSeverity.medium,
    "LOW": FindingSeverity.low,
    "UNKNOWN": FindingSeverity.info,
}


class TrivyAdapter(BaseAdapter):

    def normalize(
        self,
        raw_json: dict,
        service: str,
        commit_sha: str,
        environment: str,
    ) -> list[CanonicalFinding]:

        findings: list[CanonicalFinding] = []

        for result in raw_json.get("Results", []):

            findings.extend(
                self._parse_vulnerabilities(
                    result,
                    service,
                    commit_sha,
                    environment,
                )
            )

            findings.extend(
                self._parse_secrets(
                    result,
                    service,
                    commit_sha,
                    environment,
                )
            )

            findings.extend(
                self._parse_misconfigurations(
                    result,
                    service,
                    commit_sha,
                    environment,
                )
            )

        return findings

    def _parse_vulnerabilities(
        self,
        result,
        service,
        commit_sha,
        environment,
    ):

        findings = []

        for vuln in result.get("Vulnerabilities", []):

            findings.append(
                CanonicalFinding(
                    source_tool=SourceTool.trivy,
                    category=FindingCategory.sca,
                    severity=SEVERITY_MAP.get(
                        vuln.get("Severity", "UNKNOWN"),
                        FindingSeverity.info,
                    ),
                    cve_id=vuln.get("VulnerabilityID"),
                    title=vuln.get("Title")
                    or vuln.get("PkgName", "Unknown Package"),
                    description=vuln.get("Description", ""),
                    file_path=result.get("Target"),
                    line_number=None,
                    package_name=vuln.get("PkgName"),
                    package_version=vuln.get("InstalledVersion"),
                    fixed_version=vuln.get("FixedVersion"),
                    service=service,
                    commit_sha=commit_sha,
                    environment=environment,
                    detected_at=datetime.now(timezone.utc),
                    raw_scanner_output=vuln,
                )
            )

        return findings

    def _parse_secrets(
        self,
        result,
        service,
        commit_sha,
        environment,
    ):

        findings = []

        for secret in result.get("Secrets", []):

            findings.append(
                CanonicalFinding(
                    source_tool=SourceTool.trivy,
                    category=FindingCategory.secret,
                    severity=SEVERITY_MAP.get(
                        secret.get("Severity", "UNKNOWN"),
                        FindingSeverity.info,
                    ),
                    cve_id=None,
                    title=secret.get("Title", "Secret Detected"),
                    description=secret.get(
                        "RuleID",
                        "Secret detected",
                    ),
                    file_path=result.get("Target"),
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

    def _parse_misconfigurations(
        self,
        result,
        service,
        commit_sha,
        environment,
    ):

        findings = []

        for misconfig in result.get("Misconfigurations", []):

            findings.append(
                CanonicalFinding(
                    source_tool=SourceTool.trivy,
                    category=FindingCategory.iac,
                    severity=SEVERITY_MAP.get(
                        misconfig.get("Severity", "UNKNOWN"),
                        FindingSeverity.info,
                    ),
                    cve_id=None,
                    title=misconfig.get(
                        "Title",
                        "Misconfiguration",
                    ),
                    description=misconfig.get(
                        "Description",
                        "",
                    ),
                    file_path=result.get("Target"),
                    line_number=None,
                    package_name=None,
                    package_version=None,
                    fixed_version=None,
                    service=service,
                    commit_sha=commit_sha,
                    environment=environment,
                    detected_at=datetime.now(timezone.utc),
                    raw_scanner_output=misconfig,
                )
            )

        return findings