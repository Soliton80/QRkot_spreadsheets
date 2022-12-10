from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_charity_project_closed,
                                check_charity_project_exists,
                                check_charity_project_invested,
                                check_if_full_amount_enough,
                                check_name_duplicate)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import project_crud
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectDB,
                                         CharityProjectUpdate)
from app.services.invest import close, invest
# import pdb;
# from sqlalchemy import inspect


router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_new_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """For superusers only. Creating a charitable project"""
    await check_name_duplicate(charity_project.name, session)
    new_project = await project_crud.create(charity_project, session, commit=False)
    open_projects = await invest(new_project, session)
    if open_projects:
        session.add_all(open_projects)
    await session.commit()
    await session.refresh(new_project)

    return new_project


@router.get(
    '/',
    response_model=List[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session),
):
    projects = await project_crud.get_multi(session)
    return projects


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_charity_project(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    """For superusers only."""
    charity_project = await check_charity_project_exists(
        project_id, session
    )
    await check_charity_project_closed(charity_project)

    if obj_in.name:
        await check_name_duplicate(obj_in.name, session)

    if obj_in.full_amount:
        to_close_project = await check_if_full_amount_enough(
            obj_in.full_amount, project_id, session
        )
        if to_close_project:
            close(charity_project)

    charity_project = await project_crud.update(
        charity_project, obj_in, session
    )
    return charity_project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def remove_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """For superusers only."""
    charity_project = await check_charity_project_exists(project_id, session)
    await check_charity_project_invested(charity_project)
    charity_project = await project_crud.remove(charity_project, session)
    return charity_project
