from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class HabitCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=128)
    icon: str = Field(default="✅", max_length=10)
    color: str = Field(default="#6C5CE7", max_length=20)
    frequency: dict | None = None
    reminder_time: str | None = None


class HabitUpdate(BaseModel):
    title: str | None = None
    icon: str | None = None
    color: str | None = None
    frequency: dict | None = None
    reminder_time: str | None = None
    is_archived: bool | None = None


class HabitLogCreate(BaseModel):
    logged_date: str | None = None  # YYYY-MM-DD, defaults to today


class HabitResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    title: str
    icon: str
    color: str
    frequency: dict | None = None
    reminder_time: str | None = None
    is_archived: bool
    created_at: datetime
    streak: int = 0
    today_logged: bool = False


class HabitLogResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    habit_id: str
    user_id: str
    logged_date: str
    created_at: datetime
