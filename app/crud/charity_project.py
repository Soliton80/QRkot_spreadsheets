from typing import Optional, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .base import CRUDBase
from app.models.charity_project import CharityProject


class CRUDCharityProject(CRUDBase):

    async def get_project_id_by_name(
        self,
        project_name: str,
        session: AsyncSession,
    ) -> Optional[int]:
        db_project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name)
        )
        db_project_id = db_project_id.scalars().first()
        return db_project_id

    async def get_projects_by_completion(
            self,
            session: AsyncSession
    ) -> Optional[List]:
        projects = await session.execute(
            select(CharityProject).where(
                CharityProject.fully_invested))
        projects = projects.scalars().all()
        return projects


project_crud = CRUDCharityProject(CharityProject)
