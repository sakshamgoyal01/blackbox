from pydantic import BaseModel


class PostmortemResponse(BaseModel):
    incident_id: str
    postmortem: str