from pydantic import BaseModel
from datetime import datetime


class WebhookEntry(BaseModel):
    request_id: str
    author: str
    action: str
    from_branch: str
    to_branch: str
    timestamp: datetime
    