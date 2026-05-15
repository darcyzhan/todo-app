from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class TagCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=64)
    color: str = Field(default="#6C5CE7", max_length=20)
    icon: str | None = None
    parent_id: str | None = None


class TagUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=64)
    color: str | None = None
    icon: str | None = None
    sort_order: float | None = None


class TagResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    name: str
    color: str
    icon: str | None = None
    parent_id: str | None = None
    sort_order: float
    usage_count: int
    created_at: datetime
