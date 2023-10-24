from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.crud.base import CRUDBase
from app.models.donation import Donation
from app.models import User


class CRUDDonation(CRUDBase):

    async def get_user_donations(
        self,
        user: User,
        session: AsyncSession
    ) -> List[Donation]:
        user_donations = await session.execute(
            select(Donation).where(Donation.user_id == user.id)
        )
        user_donations = user_donations.scalars().all()
        return user_donations


donation_crud = CRUDDonation(Donation)
