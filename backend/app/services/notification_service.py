from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.notification import Notification
from app.core.exceptions import NotFoundException
from app.core.error_codes import ErrorCode


class NotificationService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_notifications(self, user_id: str, page: int = 1, page_size: int = 20) -> dict:
        query = select(Notification).where(Notification.user_id == user_id).order_by(Notification.created_at.desc())
        total = (await self.db.execute(
            select(func.count(Notification.id)).where(Notification.user_id == user_id)
        )).scalar() or 0

        offset = (page - 1) * page_size
        result = await self.db.execute(query.offset(offset).limit(page_size))
        items = result.scalars().all()

        return {"items": items, "total": total, "page": page, "page_size": page_size}

    async def get_unread_count(self, user_id: str) -> int:
        result = await self.db.execute(
            select(func.count(Notification.id)).where(
                Notification.user_id == user_id, Notification.is_read == False
            )
        )
        return result.scalar() or 0

    async def mark_read(self, notification_id: str, user_id: str) -> Notification:
        result = await self.db.execute(
            select(Notification).where(Notification.id == notification_id, Notification.user_id == user_id)
        )
        notif = result.scalar_one_or_none()
        if not notif:
            raise NotFoundException(ErrorCode.NOT_FOUND, "通知不存在")
        notif.is_read = True
        await self.db.flush()
        return notif

    async def mark_all_read(self, user_id: str) -> int:
        result = await self.db.execute(
            select(Notification).where(Notification.user_id == user_id, Notification.is_read == False)
        )
        count = 0
        for notif in result.scalars().all():
            notif.is_read = True
            count += 1
        await self.db.flush()
        return count

    async def create_notification(self, user_id: str, type: str, title: str, content: str | None = None, reference_type: str | None = None, reference_id: str | None = None) -> Notification:
        notif = Notification(
            user_id=user_id, type=type, title=title, content=content,
            reference_type=reference_type, reference_id=reference_id,
        )
        self.db.add(notif)
        await self.db.flush()
        return notif
