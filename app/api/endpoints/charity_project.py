from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import (
    CharityProjectCreate, CharityProjectUpdate, CharityProjectDB
)
from app.api.validators import (
    check_name_duplicate, check_charity_project_exists, check_charity_project,
    check_project_before_delete
)
from app.core.user import current_superuser
from app.services.investation import create_project_invest
from app.models import Donation


router = APIRouter()


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session)
):
    """Все благотворительные проекты"""
    return await charity_project_crud.get_multi(session)


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_new_charity_project(
    obj_in: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session)
):
    """Только для суперюзеров."""
    await check_name_duplicate(obj_in.name, session)
    new_charity_project = await charity_project_crud.create(
        obj_in, session
    )
    return await create_project_invest(
        new_charity_project, Donation, session
    )


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def remove_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Только для суперюзеров.

    Если в проект внесены средства, то он просто закрывается,
    если нет, то удаляется.
    """
    charity_project = await check_project_before_delete(
        project_id, session
    )
    return await charity_project_crud.remove(
        charity_project, session
    )


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_charity_project(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Только для суперюзеров.
    Закрытый проект нельзя редактировать,
    также нельзя установить требуемую сумму меньше уже вложенной.
    """
    charity_project = await check_charity_project_exists(
        project_id, session
    )
    if obj_in.name is not None and obj_in.name != charity_project.name:
        await check_name_duplicate(obj_in.name, session)
    if obj_in.full_amount is not None:
        await check_charity_project(project_id, obj_in, session)

    return await charity_project_crud.update(
        charity_project, obj_in, session
    )
