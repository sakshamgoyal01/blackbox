from app.enrich.client import HTTPClient
from app.enrich.exceptions import InvalidResponseError
from app.enrich.retry import retry
from app.enrich.types import EPSSResult


BASE_URL = "https://api.first.org/data/v1/epss"


class EPSSClient:
    def __init__(self):
        self.client = HTTPClient()

    def get_score(self, cve_id: str) -> EPSSResult | None:
        """
        Fetch EPSS information for a single CVE.

        Returns:
            EPSSResult
            or
            None (if CVE not found)
        """

        def request():
            return self.client.get(
                BASE_URL,
                params={"cve": cve_id},
            )

        response = retry(request)

        if response.get("status") != "OK":
            raise InvalidResponseError(
                f"Unexpected API status: {response}"
            )

        data = response.get("data", [])

        if not data:
            return None

        finding = data[0]

        return EPSSResult(
            cve=finding["cve"],
            epss=float(finding["epss"]),
            percentile=float(finding["percentile"]),
            date=finding["date"],
        )