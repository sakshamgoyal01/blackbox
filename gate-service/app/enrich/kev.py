from __future__ import annotations

import requests

from app.enrich.cache import (
    cache_expired,
    cache_exists,
    load_cache,
    save_cache,
)

KEV_URL = (
    "https://www.cisa.gov/sites/default/files/feeds/"
    "known_exploited_vulnerabilities.json"
)


class KEVClient:

    def _download(self) -> dict:

        response = requests.get(
            KEV_URL,
            timeout=30,
        )

        response.raise_for_status()

        return response.json()

    def feed(self) -> dict:

        if (
            not cache_exists()
            or cache_expired()
        ):

            data = self._download()

            save_cache(data)

            return data

        return load_cache()

    def is_exploited(
        self,
        cve: str,
    ) -> bool:

        feed = self.feed()

        vulnerabilities = feed.get(
            "vulnerabilities",
            [],
        )

        return any(
            item.get("cveID") == cve
            for item in vulnerabilities
        )