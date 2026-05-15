from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class ProjectCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=128)
    icon: str = Field(default="📋", max_length=10)
    color: str = Field(default="#6C5CE7", max_length=20)
    description: str | None = None


class ProjectUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=128)
    icon: str | None = None
    color: str | None = None
    description: str | None = None
    status: str | None = Field(default=None, pattern="^(active|paused|archived)$")
    sort_order: float | None = None


class ProjectMemberAdd(BaseModel):
    user_id: str
    role: str = Field(default="member", pattern="^(admin|member|readonly)$")


class ProjectMemberUpdate(BaseModel):
    role: str = Field(..., pattern="^(admin|member|readonly)$")


class ProjectMemberResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    user_id: str
    role: str
    joined_at: datetime


class ProjectStats(BaseModel):
    total_tasks: int = 0
    todo_count: int = 0
    in_progress_count: int = 0
    done_count: int = 0
    overdue_count: int = 0


class ProjectResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    name: str
    icon: str
    color: str
    description: str | None = None
    status: str
    owner_id: str
    sort_order: float
    is_archived: bool
    created_at: datetime
    updated_at: datetime
    members: list[ProjectMemberResponse] = []
    stats: ProjectStats | None = None
