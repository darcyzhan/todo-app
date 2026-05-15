import uuid
from datetime import datetime
from sqlalchemy import String, DateTime, Text, Float, Integer, Boolean, ForeignKey, Enum as SAEnum
from sqlalchemy.dialects.sqlite import JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title: Mapped[str] = mapped_column(String(256), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="todo", index=True)
    priority: Mapped[str] = mapped_column(String(5), default="P2", index=True)
    project_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("projects.id", ondelete="SET NULL"), nullable=True, index=True)
    parent_task_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("tasks.id", ondelete="CASCADE"), nullable=True, index=True)
    due_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True, index=True)
    start_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    estimated_duration: Mapped[int | None] = mapped_column(Integer, nullable=True)
    actual_duration: Mapped[int | None] = mapped_column(Integer, nullable=True)
    energy_level: Mapped[str | None] = mapped_column(String(10), nullable=True)
    sort_order: Mapped[float] = mapped_column(Float, default=0.0)
    is_recurring: Mapped[bool] = mapped_column(Boolean, default=False)
    recurrence_rule: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    location: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    created_by: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), index=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    creator = relationship("User", back_populates="tasks", foreign_keys=[created_by])
    project = relationship("Project", back_populates="tasks", foreign_keys=[project_id])
    parent_task = relationship("Task", remote_side="Task.id", back_populates="subtasks_parent")
    subtasks_parent = relationship("Task", back_populates="parent_task", foreign_keys=[parent_task_id])
    subtask_items = relationship("Subtask", back_populates="task", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="task", cascade="all, delete-orphan")
    reminders = relationship("Reminder", back_populates="task", cascade="all, delete-orphan")
    attachments = relationship("Attachment", back_populates="task", cascade="all, delete-orphan")
    task_tags = relationship("TaskTag", back_populates="task", cascade="all, delete-orphan")
    task_assignees = relationship("TaskAssignee", back_populates="task", cascade="all, delete-orphan")
    focus_sessions = relationship("FocusSession", back_populates="task")
