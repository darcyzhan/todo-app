from datetime import date, datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.habit import Habit, HabitLog
from app.schemas.habit import HabitCreate, HabitUpdate
from app.core.exceptions import NotFoundException, DuplicateException
from app.core.error_codes import ErrorCode


class HabitService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_habit(self, user_id: str, data: HabitCreate) -> Habit:
        habit = Habit(
            user_id=user_id,
            title=data.title,
            icon=data.icon,
            color=data.color,
            frequency=data.frequency,
            reminder_time=data.reminder_time,
        )
        self.db.add(habit)
        await self.db.flush()
        return habit

    async def list_habits(self, user_id: str, include_archived: bool = False) -> list[Habit]:
        query = select(Habit).where(Habit.user_id == user_id)
        if not include_archived:
            query = query.where(Habit.is_archived == False)
        result = await self.db.execute(query.order_by(Habit.created_at))
        return result.scalars().all()

    async def get_habit(self, habit_id: str, user_id: str) -> Habit:
        result = await self.db.execute(select(Habit).where(Habit.id == habit_id, Habit.user_id == user_id))
        habit = result.scalar_one_or_none()
        if not habit:
            raise NotFoundException(ErrorCode.HABIT_NOT_FOUND)
        return habit

    async def update_habit(self, habit_id: str, user_id: str, data: HabitUpdate) -> Habit:
        habit = await self.get_habit(habit_id, user_id)
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(habit, key, value)
        await self.db.flush()
        return habit

    async def delete_habit(self, habit_id: str, user_id: str) -> None:
        habit = await self.get_habit(habit_id, user_id)
        await self.db.delete(habit)
        await self.db.flush()

    async def log_habit(self, habit_id: str, user_id: str, logged_date: date | None = None) -> HabitLog:
        habit = await self.get_habit(habit_id, user_id)
        target_date = logged_date or date.today()

        result = await self.db.execute(
            select(HabitLog).where(
                HabitLog.habit_id == habit_id,
                HabitLog.user_id == user_id,
                HabitLog.logged_date == target_date,
            )
        )
        if result.scalar_one_or_none():
            raise DuplicateException(ErrorCode.HABIT_ALREADY_LOGGED, "今日已打卡")

        log = HabitLog(habit_id=habit_id, user_id=user_id, logged_date=target_date)
        self.db.add(log)
        await self.db.flush()
        return log

    async def unlog_habit(self, habit_id: str, user_id: str, logged_date: date) -> None:
        result = await self.db.execute(
            select(HabitLog).where(
                HabitLog.habit_id == habit_id,
                HabitLog.user_id == user_id,
                HabitLog.logged_date == logged_date,
            )
        )
        log = result.scalar_one_or_none()
        if not log:
            raise NotFoundException(ErrorCode.HABIT_NOT_FOUND, "未找到打卡记录")
        await self.db.delete(log)
        await self.db.flush()

    async def get_streak(self, habit_id: str, user_id: str) -> int:
        result = await self.db.execute(
            select(HabitLog.logged_date)
            .where(HabitLog.habit_id == habit_id, HabitLog.user_id == user_id)
            .order_by(HabitLog.logged_date.desc())
        )
        dates = result.scalars().all()

        if not dates:
            return 0

        streak = 0
        expected = date.today()
        for d in dates:
            if d == expected:
                streak += 1
                expected -= timedelta(days=1)
            elif d < expected:
                break
        return streak

    async def is_today_logged(self, habit_id: str, user_id: str) -> bool:
        result = await self.db.execute(
            select(HabitLog).where(
                HabitLog.habit_id == habit_id,
                HabitLog.user_id == user_id,
                HabitLog.logged_date == date.today(),
            )
        )
        return result.scalar_one_or_none() is not None
