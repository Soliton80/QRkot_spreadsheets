from typing import List

from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from http import HTTPStatus

from app.schemas.charity_project import CharityProjectDB
from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser
from app.crud.charity_project import project_crud
from app.services import (set_user_permissions, spreadsheets_create,
                          spreadsheets_update_value)
from fastapi import HTTPException

router = APIRouter()


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
    projects = await project_crud.get_projects_by_completion(
        session
    )
    spreadsheet_id = await spreadsheets_create(wrapper_services)
    await set_user_permissions(spreadsheet_id, wrapper_services)
    try:
        await spreadsheets_update_value(spreadsheet_id, projects, wrapper_services)
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=e,
        )
    return projects
