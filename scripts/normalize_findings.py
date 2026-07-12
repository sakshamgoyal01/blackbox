import json
from pathlib import Path

from app.normalize import get_adapter


DATA_DIR = Path("tests/data")


def normalize_file(
    tool: str,
    filename: str,
    service: str,
    commit_sha: str,
    environment: str,
):
    adapter = get_adapter(tool)

    with open(DATA_DIR / filename) as f:
        raw = json.load(f)

    findings = adapter.normalize(
        raw=raw,
        service=service,
        commit_sha=commit_sha,
        environment=environment,
    )

    return [finding.model_dump(mode="json") for finding in findings]


def main():

    all_findings = []

    scanners = [
        ("trivy", "trivy.json"),
        ("gitleaks", "gitleaks.json"),
        ("semgrep", "semgrep.json"),
    ]

    for tool, filename in scanners:

        all_findings.extend(
            normalize_file(
                tool,
                filename,
                service="gate-service",
                commit_sha="abc123",
                environment="dev",
            )
        )

    with open("normalized-findings.json", "w") as f:
        json.dump(all_findings, f, indent=2)

    print(f"Normalized {len(all_findings)} findings")


if __name__ == "__main__":
    main()