from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from app.models.project import Project, ProjectMember
from app.models.task import Task
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectStats
from app.core.exceptions import NotFoundException, DuplicateException, ForbiddenException
from app.core.error_codes import ErrorCode


class ProjectService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_project(self, user_id: str, data: ProjectCreate) -> Project:
        project = Project(
            name=data.name,
            icon=data.icon,
            color=data.color,
            description=data.description,
            owner_id=user_id,
        )
        self.db.add(project)
        await self.db.flush()

        member = ProjectMember(project_id=project.id, user_id=user_id, role="admin")
        self.db.add(member)
        await self.db.flush()

        return await self.get_project(project.id, user_id)

    async def get_project(self, project_id: str, user_id: str) -> Project:
        result = await self.db.execute(
            select(Project).options(selectinload(Project.members)).where(Project.id == project_id)
        )
        project = result.scalar_one_or_none()
        if not project:
            raise NotFoundException(ErrorCode.PROJECT_NOT_FOUND)
        return project

    async def list_projects(self, user_id: str, include_archived: bool = False) -> list[Project]:
        query = (
            select(Project)
            .options(selectinload(Project.members))
            .join(ProjectMember)
            .where(ProjectMember.user_id == user_id)
        )
        if not include_archived:
            query = query.where(Project.is_archived == False)
        query = query.order_by(Project.sort_order, Project.created_at.desc())
        result = await self.db.execute(query)
        return result.scalars().unique().all()

    async def update_project(self, project_id: str, user_id: str, data: ProjectUpdate) -> Project:
        project = await self.get_project(project_id, user_id)
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(project, key, value)
        await self.db.flush()
        return project

    async def delete_project(self, project_id: str, user_id: str) -> None:
        project = await self.get_project(project_id, user_id)
        if project.owner_id != user_id:
            raise ForbiddenException(ErrorCode.PERMISSION_DENIED, "仅项目所有者可删除项目")
        await self.db.delete(project)
        await self.db.flush()

    async def get_project_stats(self, project_id: str, user_id: str) -> ProjectStats:
        await self.get_project(project_id, user_id)
        result = await self.db.execute(
            select(Task.status, func.count(Task.id))
            .where(Task.project_id == project_id)
            .group_by(Task.status)
        )
        status_counts = dict(result.all())
        now = datetime.utcnow()
        overdue_result = await self.db.execute(
            select(func.count(Task.id))
            .where(Task.project_id == project_id, Task.due_date < now, Task.status != "done")
        )
        overdue_count = overdue_result.scalar() or 0

        return ProjectStats(
            total_tasks=sum(status_counts.values()),
            todo_count=status_counts.get("todo", 0),
            in_progress_count=status_counts.get("in_progress", 0),
            done_count=status_counts.get("done", 0),
            overdue_count=overdue_count,
        )

    async def add_member(self, project_id: str, user_id: str, member_user_id: str, role: str = "member") -> ProjectMember:
        await self.get_project(project_id, user_id)
        result = await self.db.execute(
            select(ProjectMember).where(
                ProjectMember.project_id == project_id,
                ProjectMember.user_id == member_user_id,
            )
        )
        if result.scalar_one_or_none():
            raise DuplicateException(ErrorCode.PROJECT_MEMBER_EXISTS)
        member = ProjectMember(project_id=project_id, user_id=member_user_id, role=role)
        self.db.add(member)
        await self.db.flush()
        return member

    async def remove_member(self, project_id: str, user_id: str, member_user_id: str) -> None:
        await self.get_project(project_id, user_id)
        result = await self.db.execute(
            select(ProjectMember).where(
                ProjectMember.project_id == project_id,
                ProjectMember.user_id == member_user_id,
            )
        )
        member = result.scalar_one_or_none()
        if not member:
            raise NotFoundException(ErrorCode.PROJECT_MEMBER_NOT_FOUND)
        await self.db.delete(member)
        await self.db.flush()
