from app.normalize.base import BaseAdapter


class SyftAdapter(BaseAdapter):

    def normalize(
        self,
        raw_json: dict,
        service: str,
        commit_sha: str,
        environment: str,
    ):
        """
        Syft produces package inventory (SBOM), not security findings.

        Phase 1 stores SBOM separately and queries it later.
        Therefore no CanonicalFinding objects are produced here.
        """

        return []