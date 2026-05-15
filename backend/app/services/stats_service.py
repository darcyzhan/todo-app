from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_
from app.models.task import Task
from app.schemas.misc import StatsDashboard


class StatsService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_dashboard(self, user_id: str) -> StatsDashboard:
        now = datetime.utcnow()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        week_start = today_start - timedelta(days=now.weekday())

        today_todo = (await self.db.execute(
            select(func.count(Task.id)).where(
                Task.created_by == user_id,
                Task.status.in_(["todo", "in_progress"]),
                Task.due_date >= today_start,
                Task.due_date < today_start + timedelta(days=1),
            )
        )).scalar() or 0

        week_done = (await self.db.execute(
            select(func.count(Task.id)).where(
                Task.created_by == user_id,
                Task.status == "done",
                or_(
                    Task.completed_at >= week_start,
                    Task.updated_at >= week_start,
                ),
            )
        )).scalar() or 0

        overdue = (await self.db.execute(
            select(func.count(Task.id)).where(
                Task.created_by == user_id,
                Task.status != "done",
                Task.due_date < now,
            )
        )).scalar() or 0

        in_progress = (await self.db.execute(
            select(func.count(Task.id)).where(
                Task.created_by == user_id,
                Task.status == "in_progress",
            )
        )).scalar() or 0

        total_active = (await self.db.execute(
            select(func.count(Task.id)).where(
                Task.created_by == user_id,
                Task.status.in_(["todo", "in_progress", "done"]),
            )
        )).scalar() or 0

        done_total = (await self.db.execute(
            select(func.count(Task.id)).where(
                Task.created_by == user_id,
                Task.status == "done",
            )
        )).scalar() or 0

        completion_rate = (done_total / total_active * 100) if total_active > 0 else 0.0

        return StatsDashboard(
            today_todo=today_todo,
            week_done=week_done,
            overdue=overdue,
            in_progress=in_progress,
            completion_rate=round(completion_rate, 1),
        )
