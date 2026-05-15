from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_
from sqlalchemy.orm import selectinload
from app.models.task import Task
from app.models.tag import Tag, TaskTag
from app.models.subtask import Subtask
from app.models.reminder import TaskAssignee
from app.schemas.task import TaskCreate, TaskUpdate, TaskFilter, TaskBatchUpdate
from app.core.exceptions import NotFoundException, AppException
from app.core.error_codes import ErrorCode


class TaskService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_task(self, user_id: str, data: TaskCreate) -> Task:
        task = Task(
            title=data.title,
            description=data.description,
            status=data.status,
            priority=data.priority,
            project_id=data.project_id,
            parent_task_id=data.parent_task_id,
            due_date=data.due_date,
            start_date=data.start_date,
            estimated_duration=data.estimated_duration,
            energy_level=data.energy_level,
            is_recurring=data.is_recurring,
            completed_at=datetime.utcnow() if data.status == "done" else None,
            recurrence_rule=data.recurrence_rule,
            location=data.location,
            created_by=user_id,
        )
        self.db.add(task)
        await self.db.flush()

        if data.tag_ids:
            for tag_id in data.tag_ids:
                self.db.add(TaskTag(task_id=task.id, tag_id=tag_id))
            await self.db.flush()

        if data.assignee_ids:
            for uid in data.assignee_ids:
                self.db.add(TaskAssignee(task_id=task.id, user_id=uid))
            await self.db.flush()

        if data.subtasks:
            for idx, st_title in enumerate(data.subtasks):
                self.db.add(Subtask(task_id=task.id, title=st_title, sort_order=float(idx)))
            await self.db.flush()

        return await self.get_task(task.id, user_id)

    async def get_task(self, task_id: str, user_id: str) -> Task:
        result = await self.db.execute(
            select(Task)
            .options(selectinload(Task.subtask_items))
            .where(Task.id == task_id)
        )
        task = result.scalar_one_or_none()
        if not task:
            raise NotFoundException(ErrorCode.TASK_NOT_FOUND)
        return task

    async def list_tasks(self, user_id: str, filters: TaskFilter) -> dict:
        query = select(Task).where(Task.created_by == user_id)

        if filters.status:
            query = query.where(Task.status.in_(filters.status))
        if filters.priority:
            query = query.where(Task.priority.in_(filters.priority))
        if filters.project_id:
            query = query.where(Task.project_id == filters.project_id)
        if filters.due_from:
            query = query.where(Task.due_date >= filters.due_from)
        if filters.due_to:
            query = query.where(Task.due_date <= filters.due_to)
        if filters.q:
            query = query.where(Task.title.ilike(f"%{filters.q}%"))

        count_query = select(func.count()).select_from(query.subquery())
        total = (await self.db.execute(count_query)).scalar()

        sort_col = getattr(Task, filters.sort, Task.created_at)
        if filters.order == "desc":
            sort_col = sort_col.desc()
        else:
            sort_col = sort_col.asc()
        query = query.order_by(sort_col)

        offset = (filters.page - 1) * filters.page_size
        query = query.offset(offset).limit(filters.page_size)

        result = await self.db.execute(query)
        tasks = result.scalars().all()

        return {
            "items": tasks,
            "total": total,
            "page": filters.page,
            "page_size": filters.page_size,
            "has_more": offset + len(tasks) < total,
        }

    async def update_task(self, task_id: str, user_id: str, data: TaskUpdate) -> Task:
        task = await self.get_task(task_id, user_id)

        update_data = data.model_dump(exclude_unset=True, exclude={"tag_ids", "assignee_ids"})
        for key, value in update_data.items():
            setattr(task, key, value)

        if data.status == "done" and task.completed_at is None:
            task.completed_at = datetime.utcnow()
        elif data.status and data.status != "done":
            task.completed_at = None

        if data.tag_ids is not None:
            await self.db.execute(
                TaskTag.__table__.delete().where(TaskTag.task_id == task_id)
            )
            for tag_id in data.tag_ids:
                self.db.add(TaskTag(task_id=task_id, tag_id=tag_id))

        if data.assignee_ids is not None:
            await self.db.execute(
                TaskAssignee.__table__.delete().where(TaskAssignee.task_id == task_id)
            )
            for uid in data.assignee_ids:
                self.db.add(TaskAssignee(task_id=task_id, user_id=uid))

        await self.db.flush()
        return await self.get_task(task_id, user_id)

    async def update_task_status(self, task_id: str, user_id: str, status: str) -> Task:
        task = await self.get_task(task_id, user_id)
        task.status = status
        if status == "done":
            task.completed_at = datetime.utcnow()
        else:
            task.completed_at = None
        await self.db.flush()
        return task

    async def delete_task(self, task_id: str, user_id: str) -> None:
        task = await self.get_task(task_id, user_id)
        await self.db.delete(task)
        await self.db.flush()

    async def batch_update(self, user_id: str, data: TaskBatchUpdate) -> list[Task]:
        tasks = []
        for task_id in data.task_ids:
            task = await self.get_task(task_id, user_id)
            if data.status:
                task.status = data.status
                if data.status == "done":
                    task.completed_at = datetime.utcnow()
            if data.priority:
                task.priority = data.priority
            if data.project_id:
                task.project_id = data.project_id
            tasks.append(task)
        await self.db.flush()
        return tasks

    async def get_subtasks(self, task_id: str, user_id: str) -> list[Subtask]:
        await self.get_task(task_id, user_id)
        result = await self.db.execute(
            select(Subtask).where(Subtask.task_id == task_id).order_by(Subtask.sort_order)
        )
        return result.scalars().all()

    async def create_subtask(self, task_id: str, user_id: str, title: str, assignee_id: str | None = None, due_date: datetime | None = None) -> Subtask:
        await self.get_task(task_id, user_id)
        subtask = Subtask(task_id=task_id, title=title, assignee_id=assignee_id, due_date=due_date)
        self.db.add(subtask)
        await self.db.flush()
        return subtask

    async def update_subtask(self, subtask_id: str, user_id: str, **kwargs) -> Subtask:
        result = await self.db.execute(select(Subtask).where(Subtask.id == subtask_id))
        subtask = result.scalar_one_or_none()
        if not subtask:
            raise NotFoundException(ErrorCode.SUBTASK_NOT_FOUND)
        for key, value in kwargs.items():
            if value is not None:
                setattr(subtask, key, value)
        await self.db.flush()
        return subtask

    async def delete_subtask(self, subtask_id: str, user_id: str) -> None:
        result = await self.db.execute(select(Subtask).where(Subtask.id == subtask_id))
        subtask = result.scalar_one_or_none()
        if not subtask:
            raise NotFoundException(ErrorCode.SUBTASK_NOT_FOUND)
        await self.db.delete(subtask)
        await self.db.flush()
