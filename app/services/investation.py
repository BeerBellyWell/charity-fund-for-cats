import datetime as dt

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation
from app.models.base import BaseModel


async def create_project_invest(
    new_charity_project: CharityProject,
    donation: Donation,
    session: AsyncSession
) -> BaseModel:
    donations = await session.execute(select(
        donation).where(donation.fully_invested == False).order_by(  # noqa
            donation.create_date)
    )
    donations = donations.scalars().all()

    for donation in donations:
        new_charity_project, donation = await calc_result(
            new_charity_project, donation
        )
        session.add(new_charity_project)
        session.add(donation)
    await session.commit()
    await session.refresh(new_charity_project)
    return new_charity_project


async def create_donat_invest(
    new_donation: Donation,
    charity_project: CharityProject,
    session: AsyncSession
) -> BaseModel:
    charity_projects = await session.execute(select(
        charity_project).where(
            charity_project.fully_invested == False).order_by(  # noqa
                charity_project.create_date)
    )
    charity_projects = charity_projects.scalars().all()

    for project in charity_projects:
        new_donation, project = await calc_result(
            new_donation, project
        )
        session.add(new_donation)
        session.add(project)
    await session.commit()
    await session.refresh(new_donation)
    return new_donation


async def calc_result(
    obj_in: BaseModel,
    obj: BaseModel
):
    how_much_money_need = obj.full_amount - obj.invested_amount
    how_much_money_have = obj_in.full_amount - obj_in.invested_amount

    if how_much_money_have > how_much_money_need:
        obj_in.invested_amount += how_much_money_need
        obj.invested_amount = obj.full_amount
        obj.fully_invested = True
        obj.close_date = dt.datetime.now()

    elif how_much_money_have == how_much_money_need:
        obj.invested_amount = obj.full_amount
        obj.fully_invested = True
        obj.close_date = dt.datetime.now()

        obj_in.invested_amount = obj_in.full_amount
        obj_in.fully_invested = True
        obj_in.close_date = dt.datetime.now()

    else:
        obj.invested_amount += how_much_money_have
        obj_in.invested_amount = obj_in.full_amount
        obj_in.fully_invested = True
        obj_in.close_date = dt.datetime.now()

    return obj_in, obj
