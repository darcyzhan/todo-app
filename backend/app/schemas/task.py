from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=256)
    description: str | None = None
    status: str = Field(default="todo", pattern="^(todo|in_progress|done|archived|cancelled)$")
    priority: str = Field(default="P2", pattern="^(P0|P1|P2|P3)$")
    project_id: str | None = None
    parent_task_id: str | None = None
    due_date: datetime | None = None
    start_date: datetime | None = None
    estimated_duration: int | None = Field(default=None, ge=0)
    energy_level: str | None = Field(default=None, pattern="^(low|medium|high)$")
    is_recurring: bool = False
    recurrence_rule: dict | None = None
    location: dict | None = None
    tag_ids: list[str] = Field(default_factory=list)
    assignee_ids: list[str] = Field(default_factory=list)
    subtasks: list[str] = Field(default_factory=list)


class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=256)
    description: str | None = None
    status: str | None = Field(default=None, pattern="^(todo|in_progress|done|archived|cancelled)$")
    priority: str | None = Field(default=None, pattern="^(P0|P1|P2|P3)$")
    project_id: str | None = None
    due_date: datetime | None = None
    start_date: datetime | None = None
    estimated_duration: int | None = Field(default=None, ge=0)
    actual_duration: int | None = Field(default=None, ge=0)
    energy_level: str | None = None
    sort_order: float | None = None
    tag_ids: list[str] | None = None
    assignee_ids: list[str] | None = None


class TaskStatusUpdate(BaseModel):
    status: str = Field(..., pattern="^(todo|in_progress|done|archived|cancelled)$")


class TaskBatchUpdate(BaseModel):
    task_ids: list[str] = Field(..., min_length=1)
    status: str | None = None
    priority: str | None = None
    project_id: str | None = None
    tag_ids: list[str] | None = None
    assignee_ids: list[str] | None = None


class SubtaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=256)
    assignee_id: str | None = None
    due_date: datetime | None = None


class SubtaskUpdate(BaseModel):
    title: str | None = None
    is_completed: bool | None = None
    sort_order: float | None = None


class SubtaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    task_id: str
    title: str
    is_completed: bool
    sort_order: float
    assignee_id: str | None = None
    due_date: datetime | None = None
    created_at: datetime


class TagBriefResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    name: str
    color: str
    icon: str | None = None


class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    title: str
    description: str | None = None
    status: str
    priority: str
    project_id: str | None = None
    parent_task_id: str | None = None
    due_date: datetime | None = None
    start_date: datetime | None = None
    estimated_duration: int | None = None
    actual_duration: int | None = None
    energy_level: str | None = None
    sort_order: float
    is_recurring: bool
    recurrence_rule: dict | None = None
    location: dict | None = None
    created_by: str
    completed_at: datetime | None = None
    created_at: datetime
    updated_at: datetime
    tags: list[TagBriefResponse] = []
    subtasks: list[SubtaskResponse] = []
    assignees: list[dict] = []


class TaskListResponse(BaseModel):
    items: list[TaskResponse]
    total: int
    page: int
    page_size: int
    has_more: bool


class TaskFilter(BaseModel):
    status: list[str] | None = None
    priority: list[str] | None = None
    project_id: str | None = None
    tag_ids: list[str] | None = None
    assignee_id: str | None = None
    due_from: datetime | None = None
    due_to: datetime | None = None
    q: str | None = None
    sort: str = "created_at"
    order: str = "desc"
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)
