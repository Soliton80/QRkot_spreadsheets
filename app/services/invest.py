from datetime import datetime
from typing import Union

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation

from app.crud.base import CRUDBase


def close(obj: Union[CharityProject, Donation]) -> None:
    """Close the project or donation."""
    obj.fully_invested = True
    obj.close_date = datetime.now()


async def invest(
    obj: Union[CharityProject, Donation],
    session: AsyncSession,
):
    """Distribute donations to open projects."""
    open_objs = await CRUDBase.get_all_open(
        CharityProject if isinstance(obj, Donation) else Donation,
        session
    )
    if not open_objs:
        return []

    amount_to_invest = obj.full_amount
    modified_objs = []
    for open_obj in open_objs:
        invested_amount = min(
            open_obj.full_amount - open_obj.invested_amount,
            amount_to_invest
        )
        open_obj.invested_amount += invested_amount
        if obj.invested_amount is None:
            obj.invested_amount = 0
        obj.invested_amount += invested_amount
        amount_to_invest -= invested_amount

        if open_obj.full_amount == open_obj.invested_amount:
            close(open_obj)
            modified_objs.append(open_obj)

        if not amount_to_invest:
            close(obj)
            break

    return modified_objs
