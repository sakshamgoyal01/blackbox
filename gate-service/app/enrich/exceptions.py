class EnrichmentError(Exception):
    """Base enrichment exception."""


class ExternalAPIError(EnrichmentError):
    """Remote API returned an error."""


class InvalidResponseError(EnrichmentError):
    """Unexpected response received from remote API."""


class RateLimitExceeded(EnrichmentError):
    """Remote API rate limited the request."""