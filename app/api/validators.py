from fastapi import HTTPException, status
from pydantic import PositiveInt
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import project_crud
from app.models import CharityProject


async def check_name_duplicate(
    project_name: str,
    session: AsyncSession,
) -> None:
    """Check the name of the project for uniqueness."""
    project_id = await project_crud.get_project_id_by_name(
        project_name, session
    )
    if project_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Проект с таким именем уже существует!',
        )


async def check_charity_project_exists(
    project_id: int,
    session: AsyncSession,
) -> CharityProject:
    """Verify that the project exists."""
    charity_project = await project_crud.get_by_attribute(
        'id', project_id, session
    )
    if not charity_project:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail='Проект не найден!'
        )
    return charity_project


async def check_charity_project_invested(project: CharityProject) -> None:
    """Verify that funds have been entered into the project."""
    if project.invested_amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!',
        )


async def check_if_full_amount_enough(
    full_amount: PositiveInt,
    project_id: int,
    session: AsyncSession,
) -> bool:
    """Check that the project can be updated and closed if necessary."""
    charity_project = await project_crud.get_by_attribute(
        'id', project_id, session
    )
    if full_amount < charity_project.invested_amount:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail='Сумма проекта не может быть меньше внесённой!',
        )
    return full_amount == charity_project.invested_amount


async def check_charity_project_closed(project: CharityProject) -> None:
    """Check if the project is closed."""
    if project.fully_invested:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Закрытый проект нельзя редактировать!',
        )
