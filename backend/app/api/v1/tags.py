from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.tag import TagCreate, TagUpdate, TagResponse
from app.services.tag_service import TagService
from app.models.user import User
from app.core.security import get_current_user

router = APIRouter(prefix="/tags", tags=["标签"])


@router.post("", response_model=TagResponse, status_code=201)
async def create_tag(
    data: TagCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = TagService(db)
    tag = await service.create_tag(current_user.id, data)
    return TagResponse.model_validate(tag)


@router.get("", response_model=list[TagResponse])
async def list_tags(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = TagService(db)
    tags = await service.list_tags(current_user.id)
    return [TagResponse.model_validate(t) for t in tags]


@router.get("/{tag_id}", response_model=TagResponse)
async def get_tag(
    tag_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = TagService(db)
    tag = await service.get_tag(tag_id, current_user.id)
    return TagResponse.model_validate(tag)


@router.put("/{tag_id}", response_model=TagResponse)
async def update_tag(
    tag_id: str,
    data: TagUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = TagService(db)
    tag = await service.update_tag(tag_id, current_user.id, data)
    return TagResponse.model_validate(tag)


@router.delete("/{tag_id}", status_code=204)
async def delete_tag(
    tag_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = TagService(db)
    await service.delete_tag(tag_id, current_user.id)
