from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, func

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


class CRUDCharity_project(CRUDBase):

    async def remove(
        self,
        db_obj,
        session: AsyncSession
    ) -> CharityProject:
        await session.delete(db_obj)
        await session.commit()
        return db_obj

    async def update(
            self,
            db_obj,
            obj_in,
            session: AsyncSession,
    ) -> CharityProject:
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def get_charity_project_id_by_name(
        self,
        charity_project_name: str,
        session: AsyncSession
    ) -> Optional[int]:
        charity_project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == charity_project_name
            ))
        charity_project_id = charity_project_id.scalars().first()
        return charity_project_id

    async def close_not_fully_project(
        self,
        charity_project: CharityProject,
        session: AsyncSession
    ):
        session.add(charity_project)
        await session.commit()
        await session.refresh(charity_project)
        return charity_project

    async def get_projects_by_completion_rate(
        self,
        session: AsyncSession,
    ) -> list[CharityProject]:
        close_projects = await session.execute(
            select(CharityProject).where(
                CharityProject.fully_invested == True  # noqa
            ).order_by(
                func.julianday(CharityProject.close_date) -
                func.julianday(CharityProject.create_date)
            )
        )
        close_projects = close_projects.scalars().all()
        return close_projects


charity_project_crud = CRUDCharity_project(CharityProject)
