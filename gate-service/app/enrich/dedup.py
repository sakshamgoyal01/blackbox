from collections import defaultdict

from app.db.models.finding import Finding


SEVERITY_RANK = {
    "critical": 4,
    "high": 3,
    "medium": 2,
    "low": 1,
    "info": 0,
}


class Deduplicator:

    @staticmethod
    def group(findings: list[Finding]):

        groups = defaultdict(list)

        for finding in findings:

            if not finding.cve_id:
                continue

            key = (
                finding.service,
                finding.commit_sha,
                finding.cve_id,
            )

            groups[key].append(finding)

        return groups

    @staticmethod
    def choose_primary(group: list[Finding]) -> Finding:

        return max(
            group,
            key=lambda finding: (
                SEVERITY_RANK[finding.severity.value],
                finding.priority_score or 0,
            ),
        )

    def deduplicate(
        self,
        findings: list[Finding],
    ):

        primary = []

        duplicates = []

        groups = self.group(findings)

        for _, group in groups.items():

            if len(group) == 1:

                primary.extend(group)

                continue

            keep = self.choose_primary(group)

            primary.append(keep)

            for finding in group:

                if finding.finding_id != keep.finding_id:
                    duplicates.append(
                        (
                            keep,
                            finding,
                        )
                    )

        return primary, duplicates