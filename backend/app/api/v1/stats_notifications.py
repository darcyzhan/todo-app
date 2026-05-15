from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.misc import StatsDashboard, NotificationResponse
from app.services.stats_service import StatsService
from app.services.notification_service import NotificationService
from app.models.user import User
from app.core.security import get_current_user

router = APIRouter(tags=["统计与通知"])


# Stats
@router.get("/stats/dashboard", response_model=StatsDashboard)
async def get_dashboard(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = StatsService(db)
    return await service.get_dashboard(current_user.id)


# Notifications
@router.get("/notifications", response_model=dict)
async def list_notifications(
    page: int = 1,
    page_size: int = 20,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = NotificationService(db)
    return await service.list_notifications(current_user.id, page, page_size)


@router.get("/notifications/unread-count")
async def get_unread_count(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = NotificationService(db)
    count = await service.get_unread_count(current_user.id)
    return {"count": count}


@router.put("/notifications/{notification_id}/read", response_model=NotificationResponse)
async def mark_read(
    notification_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = NotificationService(db)
    notif = await service.mark_read(notification_id, current_user.id)
    return NotificationResponse.model_validate(notif)


@router.put("/notifications/read-all")
async def mark_all_read(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = NotificationService(db)
    count = await service.mark_all_read(current_user.id)
    return {"marked_count": count}
