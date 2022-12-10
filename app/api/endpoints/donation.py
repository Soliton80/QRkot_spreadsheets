from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_user
from app.crud.donation import donation_crud
from app.models import User
from app.schemas.donation import DonationCreate, DonationDB, DonationDBMain
from app.services.invest import invest

router = APIRouter()


@router.post(
    '/',
    response_model=DonationDBMain,
    response_model_exclude_none=True,
)
async def create_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    new_donation = await donation_crud.create(donation, session, commit=False, user=user)
    open_projects = await invest(new_donation, session)
    if open_projects:
        session.add_all(open_projects)
    await session.commit()
    await session.refresh(new_donation)
    return new_donation


@router.get(
    '/',
    response_model=List[DonationDB],
    response_model_exclude_none=True,
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
):
    donations = await donation_crud.get_multi(session)
    return donations


@router.get(
    '/my',
    response_model=List[DonationDBMain],
    response_model_exclude_none=True,
    response_model_exclude={'user_id'},
)
async def get_my_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    """Gets a list of all donations for the current user."""
    donations = await donation_crud.get_by_user(session, user)
    return donations
