from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.tag import Tag, TaskTag
from app.schemas.tag import TagCreate, TagUpdate
from app.core.exceptions import NotFoundException
from app.core.error_codes import ErrorCode


class TagService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_tag(self, user_id: str, data: TagCreate) -> Tag:
        tag = Tag(
            name=data.name,
            color=data.color,
            icon=data.icon,
            user_id=user_id,
            parent_id=data.parent_id,
        )
        self.db.add(tag)
        await self.db.flush()
        return tag

    async def list_tags(self, user_id: str) -> list[Tag]:
        result = await self.db.execute(
            select(Tag).where(Tag.user_id == user_id).order_by(Tag.sort_order, Tag.created_at)
        )
        return result.scalars().all()

    async def get_tag(self, tag_id: str, user_id: str) -> Tag:
        result = await self.db.execute(select(Tag).where(Tag.id == tag_id, Tag.user_id == user_id))
        tag = result.scalar_one_or_none()
        if not tag:
            raise NotFoundException(ErrorCode.TAG_NOT_FOUND)
        return tag

    async def update_tag(self, tag_id: str, user_id: str, data: TagUpdate) -> Tag:
        tag = await self.get_tag(tag_id, user_id)
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(tag, key, value)
        await self.db.flush()
        return tag

    async def delete_tag(self, tag_id: str, user_id: str) -> None:
        tag = await self.get_tag(tag_id, user_id)
        await self.db.delete(tag)
        await self.db.flush()
