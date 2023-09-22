from typing import List
from uuid import UUID

from fastapi import HTTPException
from models.minter import Minter, MinterCreate
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import delete, select


async def create_minter(session: AsyncSession, minter: MinterCreate) -> Minter:
    db_minter = Minter(**minter.dict())
    try:
        session.add(db_minter)
        await session.commit()
        await session.refresh(db_minter)
        return db_minter
    except IntegrityError as e:
        await session.rollback()
        raise e


async def get_minter(session: AsyncSession, id: UUID) -> Minter:
    query = select(Minter).where(Minter.id == id)
    response = await session.execute(query)
    return response.scalar_one_or_none()


async def get_minters(session: AsyncSession) -> List[Minter]:
    query = select(Minter)
    response = await session.execute(query)
    return response.scalars().all()


async def get_minter_by_naa(session: AsyncSession, naa: str) -> Minter:
    query = select(Minter).where(Minter.naa == naa)
    response = await session.execute(query)
    return response.scalar_one_or_none()


# async def update_minter_n(session: AsyncSession, id: UUID, n: int) -> Minter:
#     db_minter = await get_minter(session, id)
#     db_minter.last_n = n

#     try:
#         await session.commit()
#         await session.refresh(db_minter)
#         return db_minter
#     except IntegrityError:
#         session.rollback()


async def delete_minter(session: AsyncSession, id: UUID) -> int:
    query = delete(Minter).where(Minter.id == id)
    response = await session.execute(query)
    await session.commit()
    return response.rowcount
