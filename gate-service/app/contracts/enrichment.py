from pydantic import BaseModel


class EnrichmentRequest(BaseModel):
    service: str | None = None
    commit_sha: str | None = None


class EnrichmentResponse(BaseModel):

    processed: int

    epss_updated: int

    kev_updated: int

    priority_updated: int

    enriched: int

    status: str