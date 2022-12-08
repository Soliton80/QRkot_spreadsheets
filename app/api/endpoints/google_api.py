from datetime import datetime
from typing import Dict, List, Union

from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.charity_project import CharityProjectDB
from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser
from app.crud.charity_project import project_crud
from app.services import (set_user_permissions, spreadsheets_create,
                          spreadsheets_update_value)

router = APIRouter()

FORMAT = '%Y/%m/%d %H:%M:%S'


@router.post(
    '/',
    response_model=List[CharityProjectDB],
    dependencies=[Depends(current_superuser)],
)


async def get_report(
        session: AsyncSession = Depends(get_async_session),
        wrapper_services: Aiogoogle = Depends(get_service)
):
    """For superusers only."""
    projects = await project_crud.get_projects_by_completion_rate(
        session
    )
    now_date_time = datetime.now().strftime(FORMAT)
    spreadsheet_id = await spreadsheets_create(wrapper_services, now_date_time)
    await set_user_permissions(spreadsheet_id, wrapper_services)
    await spreadsheets_update_value(spreadsheet_id, projects, wrapper_services, now_date_time)
    
    return projects
