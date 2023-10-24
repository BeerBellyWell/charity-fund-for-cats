from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject
from app.core import constants


async def check_name_duplicate(
    charity_project_name: str,
    session: AsyncSession
) -> None:
    charity_project_id = await charity_project_crud.get_charity_project_id_by_name(
        charity_project_name, session
    )
    if charity_project_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=constants.ERR_NAME_DUPLICATE
        )


async def check_charity_project_exists(
    charity_project_id: int,
    session: AsyncSession
) -> CharityProject:
    charity_project = await charity_project_crud.get(
        charity_project_id, session
    )
    if charity_project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=constants.ERR_NOT_FOUND_PROJECT
        )
    return charity_project


async def check_charity_project(
    charity_project_id: int,
    obj_in: CharityProject,
    session: AsyncSession
) -> CharityProject:
    charity_project = await check_charity_project_exists(
        charity_project_id, session
    )
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=constants.ERR_CLOSE_PROJECT
        )

    if obj_in.full_amount < charity_project.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail=constants.ERR_FULL_AMOUNT
        )
    return charity_project


async def check_project_before_delete(
    charity_project_id: int,
    session: AsyncSession
) -> CharityProject:
    charity_project = await check_charity_project_exists(
        charity_project_id, session
    )
    if charity_project.invested_amount != 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=constants.ERR_UPDATE
        )
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=constants.ERR_UPDATE
        )

    return charity_project
