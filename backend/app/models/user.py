import uuid
from datetime import datetime
from sqlalchemy import String, DateTime, Enum as SAEnum, Text, Boolean
from sqlalchemy.dialects.sqlite import JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    openid: Mapped[str | None] = mapped_column(String(128), unique=True, index=True, nullable=True)
    union_id: Mapped[str | None] = mapped_column(String(128), unique=True, index=True, nullable=True)
    nickname: Mapped[str] = mapped_column(String(64), default="")
    avatar_url: Mapped[str] = mapped_column(String(512), default="")
    phone: Mapped[str | None] = mapped_column(String(20), unique=True, nullable=True)
    timezone: Mapped[str] = mapped_column(String(64), default="Asia/Shanghai")
    theme: Mapped[str] = mapped_column(String(20), default="auto")
    language: Mapped[str] = mapped_column(String(10), default="zh-CN")
    membership: Mapped[str] = mapped_column(String(20), default="free")
    membership_expires_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    hashed_password: Mapped[str | None] = mapped_column(String(256), nullable=True)
    settings: Mapped[dict | None] = mapped_column(JSON, default=dict)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    tasks = relationship("Task", back_populates="creator", foreign_keys="Task.created_by")
    projects = relationship("Project", back_populates="owner", foreign_keys="Project.owner_id")
    tags = relationship("Tag", back_populates="user", foreign_keys="Tag.user_id")
    habits = relationship("Habit", back_populates="user", foreign_keys="Habit.user_id")
    notifications = relationship("Notification", back_populates="user", foreign_keys="Notification.user_id")
