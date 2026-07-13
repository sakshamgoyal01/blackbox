from sqlalchemy.orm import Session

from app.crud.enrichment import (
    commit,
    get_pending_epss_findings,
    get_pending_kev_findings,
    get_priority_candidates,
    mark_enriched,
    update_epss_score,
    update_kev_status,
    update_priority_score,
get_duplicate_candidates,
    suppress_duplicate,
)

from app.enrich.epss import EPSSClient
from app.enrich.kev import KEVClient
from app.enrich.priority import calculate_priority
from app.enrich.dedup import Deduplicator

class EPSSEnrichmentService:

    def __init__(self):
        self.client = EPSSClient()
        self.kev = KEVClient()

    # ---------------------------------------------------------
    # EPSS
    # ---------------------------------------------------------

    def enrich(
        self,
        db: Session,
        service: str | None = None,
        commit_sha: str | None = None,
    ) -> int:

        findings = get_pending_epss_findings(
            db,
            service,
            commit_sha,
        )

        updated = 0

        for finding in findings:

            result = self.client.get_score(
                finding.cve_id
            )

            if result is None:
                continue

            update_epss_score(
                db,
                finding,
                result.epss,
            )

            updated += 1

        commit(db)

        return updated

    # ---------------------------------------------------------
    # KEV
    # ---------------------------------------------------------
    def deduplicate(
            self,
            db: Session,
            service: str | None = None,
            commit_sha: str | None = None,
    ) -> int:

        findings = get_duplicate_candidates(
            db,
            service,
            commit_sha,
        )

        deduplicator = Deduplicator()

        _, duplicates = deduplicator.deduplicate(
            findings
        )

        updated = 0

        for _, duplicate in duplicates:
            suppress_duplicate(
                db,
                duplicate,
            )

            updated += 1

        commit(db)

        return updated

    def enrich_kev(
        self,
        db: Session,
        service: str | None = None,
        commit_sha: str | None = None,
    ) -> int:

        findings = get_pending_kev_findings(
            db,
            service,
            commit_sha,
        )

        updated = 0

        for finding in findings:

            exploited = self.kev.is_exploited(
                finding.cve_id
            )

            update_kev_status(
                db,
                finding,
                exploited,
            )

            updated += 1

        commit(db)

        return updated

    # ---------------------------------------------------------
    # Priority
    # ---------------------------------------------------------

    def enrich_priority(
        self,
        db: Session,
        service: str | None = None,
        commit_sha: str | None = None,
    ) -> int:

        findings = get_priority_candidates(
            db,
            service,
            commit_sha,
        )

        updated = 0

        for finding in findings:

            score = calculate_priority(
                severity=finding.severity.value,
                epss_score=finding.epss_score,
                kev_listed=finding.kev_listed,
            )

            update_priority_score(
                db,
                finding,
                score,
            )

            updated += 1

        commit(db)

        return updated

    # ---------------------------------------------------------
    # Phase 2 Orchestrator
    # ---------------------------------------------------------

    def enrich_all(
        self,
        db: Session,
        service: str | None = None,
        commit_sha: str | None = None,
    ) -> dict:

        epss_updated = self.enrich(
            db,
            service,
            commit_sha,
        )

        kev_updated = self.enrich_kev(
            db,
            service,
            commit_sha,
        )

        priority_updated = self.enrich_priority(
            db,
            service,
            commit_sha,
        )
        duplicates = self.deduplicate(
            db,
            service,
            commit_sha,
        )

        enriched = mark_enriched(
            db,
            service,
            commit_sha,
        )

        commit(db)

        return {
            "processed": enriched,
            "epss_updated": epss_updated,
            "kev_updated": kev_updated,
            "priority_updated": priority_updated,
            "duplicates_suppressed": duplicates,
            "enriched": enriched,
            "status": "completed",
        }