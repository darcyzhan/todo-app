from datetime import date
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.habit import HabitCreate, HabitUpdate, HabitResponse, HabitLogResponse
from app.services.habit_service import HabitService
from app.models.user import User
from app.core.security import get_current_user

router = APIRouter(prefix="/habits", tags=["习惯"])


@router.post("", response_model=HabitResponse, status_code=201)
async def create_habit(
    data: HabitCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = HabitService(db)
    habit = await service.create_habit(current_user.id, data)
    return await _build_habit_response(habit, service)


@router.get("", response_model=list[HabitResponse])
async def list_habits(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = HabitService(db)
    habits = await service.list_habits(current_user.id)
    result = []
    for h in habits:
        result.append(await _build_habit_response(h, service))
    return result


@router.get("/{habit_id}", response_model=HabitResponse)
async def get_habit(
    habit_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = HabitService(db)
    habit = await service.get_habit(habit_id, current_user.id)
    return await _build_habit_response(habit, service)


@router.put("/{habit_id}", response_model=HabitResponse)
async def update_habit(
    habit_id: str,
    data: HabitUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = HabitService(db)
    habit = await service.update_habit(habit_id, current_user.id, data)
    return await _build_habit_response(habit, service)


@router.delete("/{habit_id}", status_code=204)
async def delete_habit(
    habit_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = HabitService(db)
    await service.delete_habit(habit_id, current_user.id)


@router.post("/{habit_id}/log", response_model=HabitLogResponse, status_code=201)
async def log_habit(
    habit_id: str,
    logged_date: str | None = Query(None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = HabitService(db)
    target_date = date.fromisoformat(logged_date) if logged_date else None
    log = await service.log_habit(habit_id, current_user.id, target_date)
    return HabitLogResponse(
        id=log.id,
        habit_id=log.habit_id,
        user_id=log.user_id,
        logged_date=str(log.logged_date),
        created_at=log.created_at,
    )


@router.delete("/{habit_id}/log/{logged_date}", status_code=204)
async def unlog_habit(
    habit_id: str,
    logged_date: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = HabitService(db)
    await service.unlog_habit(habit_id, current_user.id, date.fromisoformat(logged_date))


async def _build_habit_response(habit, service: HabitService) -> HabitResponse:
    streak = await service.get_streak(habit.id, habit.user_id)
    today_logged = await service.is_today_logged(habit.id, habit.user_id)
    return HabitResponse(
        id=habit.id,
        title=habit.title,
        icon=habit.icon,
        color=habit.color,
        frequency=habit.frequency,
        reminder_time=habit.reminder_time,
        is_archived=habit.is_archived,
        created_at=habit.created_at,
        streak=streak,
        today_logged=today_logged,
    )
