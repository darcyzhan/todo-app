from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class CommentCreate(BaseModel):
    content: str = Field(..., min_length=1)
    parent_id: str | None = None
    mentions: list[str] | None = None


class CommentUpdate(BaseModel):
    content: str = Field(..., min_length=1)


class CommentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    task_id: str
    user_id: str
    content: str
    parent_id: str | None = None
    mentions: dict | None = None
    attachments: dict | None = None
    created_at: datetime
    updated_at: datetime


class NotificationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    type: str
    title: str
    content: str | None = None
    reference_type: str | None = None
    reference_id: str | None = None
    is_read: bool
    created_at: datetime


class StatsDashboard(BaseModel):
    today_todo: int = 0
    week_done: int = 0
    overdue: int = 0
    in_progress: int = 0
    completion_rate: float = 0.0


class FocusSessionCreate(BaseModel):
    task_id: str | None = None
    type: str = Field(default="pomodoro", pattern="^(pomodoro|custom)$")
    started_at: datetime | None = None


class FocusSessionEnd(BaseModel):
    duration: int = Field(..., ge=1)
    interruption_count: int = 0


class FocusSessionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    user_id: str
    task_id: str | None = None
    duration: int
    started_at: datetime
    ended_at: datetime | None = None
    interruption_count: int
    type: str
