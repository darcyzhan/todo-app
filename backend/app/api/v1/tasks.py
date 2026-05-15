from datetime import datetime
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.task import (
    TaskCreate, TaskUpdate, TaskResponse, TaskListResponse,
    TaskFilter, TaskStatusUpdate, TaskBatchUpdate,
    SubtaskCreate, SubtaskUpdate, SubtaskResponse, TagBriefResponse,
)
from app.services.task_service import TaskService
from app.models.task import Task
from app.models.tag import TaskTag, Tag
from app.models.subtask import Subtask
from app.models.reminder import TaskAssignee
from app.models.user import User
from app.core.security import get_current_user
from sqlalchemy import select

router = APIRouter(prefix="/tasks", tags=["任务"])


def _task_to_response(task: Task, tags=None, subtasks=None, assignees=None) -> dict:
    """手动构建响应，避免 lazy load 问题"""
    return {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "status": task.status,
        "priority": task.priority,
        "project_id": task.project_id,
        "parent_task_id": task.parent_task_id,
        "due_date": task.due_date,
        "start_date": task.start_date,
        "estimated_duration": task.estimated_duration,
        "actual_duration": task.actual_duration,
        "energy_level": task.energy_level,
        "sort_order": task.sort_order,
        "is_recurring": task.is_recurring,
        "recurrence_rule": task.recurrence_rule,
        "location": task.location,
        "created_by": task.created_by,
        "completed_at": task.completed_at,
        "created_at": task.created_at,
        "updated_at": task.updated_at,
        "tags": tags or [],
        "subtasks": subtasks or [],
        "assignees": assignees or [],
    }


@router.post("", response_model=TaskResponse, status_code=201)
async def create_task(
    data: TaskCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = TaskService(db)
    task = await service.create_task(current_user.id, data)
    return await _build_task_response(task, db)


@router.get("", response_model=TaskListResponse)
async def list_tasks(
    status: str | None = Query(None),
    priority: str | None = Query(None),
    project_id: str | None = Query(None),
    q: str | None = Query(None),
    sort: str = Query("created_at"),
    order: str = Query("desc"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    filters = TaskFilter(
        status=status.split(",") if status else None,
        priority=priority.split(",") if priority else None,
        project_id=project_id,
        q=q,
        sort=sort,
        order=order,
        page=page,
        page_size=page_size,
    )
    service = TaskService(db)
    result = await service.list_tasks(current_user.id, filters)
    items = []
    for task in result["items"]:
        items.append(await _build_task_response(task, db))
    return TaskListResponse(
        items=items,
        total=result["total"],
        page=result["page"],
        page_size=result["page_size"],
        has_more=result["has_more"],
    )


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = TaskService(db)
    task = await service.get_task(task_id, current_user.id)
    return await _build_task_response(task, db)


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: str,
    data: TaskUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = TaskService(db)
    task = await service.update_task(task_id, current_user.id, data)
    return await _build_task_response(task, db)


@router.put("/{task_id}/status", response_model=TaskResponse)
async def update_task_status(
    task_id: str,
    data: TaskStatusUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = TaskService(db)
    task = await service.update_task_status(task_id, current_user.id, data.status)
    return await _build_task_response(task, db)


@router.delete("/{task_id}", status_code=204)
async def delete_task(
    task_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = TaskService(db)
    await service.delete_task(task_id, current_user.id)


@router.post("/batch", response_model=list[TaskResponse])
async def batch_update(
    data: TaskBatchUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = TaskService(db)
    tasks = await service.batch_update(current_user.id, data)
    return [await _build_task_response(t, db) for t in tasks]


# Subtask routes
@router.post("/{task_id}/subtasks", response_model=SubtaskResponse, status_code=201)
async def create_subtask(
    task_id: str,
    data: SubtaskCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = TaskService(db)
    subtask = await service.create_subtask(
        task_id, current_user.id, data.title, data.assignee_id, data.due_date
    )
    return SubtaskResponse.model_validate(subtask)


@router.put("/subtasks/{subtask_id}", response_model=SubtaskResponse)
async def update_subtask(
    subtask_id: str,
    data: SubtaskUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = TaskService(db)
    update_data = data.model_dump(exclude_unset=True)
    subtask = await service.update_subtask(subtask_id, current_user.id, **update_data)
    return SubtaskResponse.model_validate(subtask)


@router.delete("/subtasks/{subtask_id}", status_code=204)
async def delete_subtask(
    subtask_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = TaskService(db)
    await service.delete_subtask(subtask_id, current_user.id)


async def _build_task_response(task: Task, db: AsyncSession) -> TaskResponse:
    """从数据库加载关联数据构建响应"""
    # Load tags
    tag_result = await db.execute(
        select(Tag).join(TaskTag, TaskTag.tag_id == Tag.id).where(TaskTag.task_id == task.id)
    )
    tags = [TagBriefResponse(id=t.id, name=t.name, color=t.color, icon=t.icon) for t in tag_result.scalars().all()]

    # Load subtasks
    st_result = await db.execute(
        select(Subtask).where(Subtask.task_id == task.id).order_by(Subtask.sort_order)
    )
    subtasks = [SubtaskResponse.model_validate(s) for s in st_result.scalars().all()]

    # Load assignees
    from app.models.user import User as UserModel
    from app.models.reminder import TaskAssignee as TA
    assignee_result = await db.execute(
        select(UserModel).join(TA, TA.user_id == UserModel.id).where(TA.task_id == task.id)
    )
    assignees = [{"id": u.id, "nickname": u.nickname, "avatar_url": u.avatar_url} for u in assignee_result.scalars().all()]

    data = _task_to_response(task, tags, subtasks, assignees)
    return TaskResponse(**data)
