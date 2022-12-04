from typing import Optional

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

    async def get_projects_by_completion_rate(
            self,
            session: AsyncSession
    ) -> Optional[list[dict[str, str]]]:
        projects = await session.execute(
            select(
                CharityProject.name,
                CharityProject.close_date,
                CharityProject.create_date,
                CharityProject.description).where(
                    CharityProject.fully_invested)
        )
        result = []
        for elem in projects:
            result.append({
                'name': elem.name,
                'time_delta': str(elem.close_date - elem.create_date),
                'description': elem.description})
        return sorted(result, key=lambda x: x['time_delta'])
    


project_crud = CRUDCharityProject(CharityProject)
