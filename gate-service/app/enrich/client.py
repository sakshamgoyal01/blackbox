from requests import Session


class HTTPClient:

    def __init__(self):

        self.session = Session()

        self.session.headers.update(
            {
                "Accept": "application/json",
                "User-Agent": "BLACKBOX/1.0",
            }
        )

    def get(self, url, **kwargs):

        response = self.session.get(
            url,
            timeout=15,
            **kwargs,
        )

        response.raise_for_status()

        return response.json()