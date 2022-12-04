from datetime import datetime
from typing import List, Type, TypeVar, Union

from sqlalchemy import false, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation

ModelType = TypeVar('ModelType', CharityProject, Donation)


async def close(obj: Union[CharityProject, Donation]) -> None:
    """Close the project or donation."""
    obj.fully_invested = True
    obj.close_date = datetime.now()


async def get_all_open(
    model: Type[ModelType],
    session: AsyncSession,
) -> List[Union[CharityProject, Donation]]:
    """Get all open projects or donations."""
    open_objs = await session.execute(
        select(model).where(
            model.fully_invested == false()
        ).order_by(model.create_date)
    )
    open_objs = open_objs.scalars().all()
    return open_objs


async def invest(
    obj: Union[CharityProject, Donation],
    session: AsyncSession,
) -> None:
    """Distribute donations to open projects."""
    MODELS = (CharityProject, Donation)

    model = MODELS[isinstance(obj, CharityProject)]
    open_objs = await get_all_open(model, session)
    if open_objs:
        amount_to_invest = obj.full_amount
        for open_obj in open_objs:
            amount = open_obj.full_amount - open_obj.invested_amount
            invested_amount = min(amount, amount_to_invest)
            open_obj.invested_amount += invested_amount
            obj.invested_amount += invested_amount
            amount_to_invest -= invested_amount

            if open_obj.full_amount == open_obj.invested_amount:
                await close(open_obj)

            if not amount_to_invest:
                await close(obj)
                break
        await session.commit()
