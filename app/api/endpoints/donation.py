from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.donation import donation_crud
from app.schemas.donation import DonationCreate, DonationDB, DonationMyDB
from app.core.user import current_superuser, current_user
from app.models import User, CharityProject
from app.services.investation import create_donat_invest


router = APIRouter()


@router.get(
    '/',
    response_model=list[DonationDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session)
):
    """
    Только для суперюзеров.
    Список всех пожертвований.
    """
    all_donations = await donation_crud.get_multi(session)
    return all_donations


@router.get(
    '/my',
    response_model=list[DonationMyDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_user)],
)
async def get_user_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    """Получить список пожертвований конкретного пользователя."""
    all_user_donations = await donation_crud.get_user_donations(user, session)
    return all_user_donations


@router.post(
    '/',
    response_model=DonationMyDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_user)]
)
async def create_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    new_donation = await donation_crud.create(donation, session, user)
    new_donation = await create_donat_invest(
        new_donation, CharityProject, session
    )
    return new_donation
