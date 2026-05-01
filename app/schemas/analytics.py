

from pydantic import BaseModel


class AnalyticsSchema(BaseModel):
    query: str