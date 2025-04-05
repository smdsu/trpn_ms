from app.core.config import async_session_maker
from sqlalchemy import insert
from sqlalchemy.future import select
from sqlalchemy import update as sqlalchemy_update, delete as sqlalchemy_delete
from sqlalchemy.exc import SQLAlchemyError

from datetime import datetime, timedelta

from fastapi.logger import logger
from fastapi import HTTPException


class BaseDAO:
    model = None

    @classmethod
    async def find_all(cls, **filter_by):
        try:
            async with async_session_maker() as session:
                query = select(cls.model).filter_by(**filter_by)
                result = await session.execute(query)
                return result.scalars().all()
        except Exception as e:
            logger.error(f"Error finding all for {cls.model.__tablename__}: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Error finding all, {str(e)}"
            ) from e

    @classmethod
    async def find_one_or_none_by_id(cls, data_id: int):
        try:
            async with async_session_maker() as session:
                query = select(cls.model).filter_by(id=data_id)
                result = await session.execute(query)
                return result.scalar_one_or_none()
        except Exception as e:
            logger.error(
                f"Error finding one by id for {cls.model.__tablename__}:"
                f"{str(e)}"
            )
            raise HTTPException(
                status_code=500,
                detail=f"Error finding one by id={data_id}, {str(e)}"
            ) from e

    @classmethod
    async def find_one_or_none_by_filter(cls, **filter_by):
        try:
            async with async_session_maker() as session:
                query = select(cls.model).filter_by(**filter_by)
                result = await session.execute(query)
                return result.scalar_one_or_none()
        except Exception as e:
            logger.error(
                f"Error finding one by filter for {cls.model.__tablename__}:"
                f"{str(e)}"
            )
            raise HTTPException(
                status_code=500,
                detail=f"Error finding one by filter={filter_by}, {str(e)}"
            ) from e

    @classmethod
    async def add(cls, **values):
        try:
            async with async_session_maker() as session:
                async with session.begin():
                    new_instance = cls.model(**values)
                session.add(new_instance)
                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    return e
                return new_instance
        except Exception as e:
            logger.error(f"Error adding to {cls.model.__tablename__}: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Error adding to {cls.model.__tablename__}, {str(e)}"
            ) from e

    @classmethod
    async def update(cls, filter_by, **values):
        try:
            async with async_session_maker() as session:
                async with session.begin():
                    query = (
                        sqlalchemy_update(cls.model)
                        .where(
                            *[getattr(cls.model, k) == v for k, v in filter_by.items()]
                        )
                        .values(**values)
                        .execution_options(synchronize_session="fetch")
                    )
                result = await session.execute(query)
                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    logger.error(f"Error saving data: {str(e)}")
                    await session.rollback()
                    raise e
                return result.rowcount
        except Exception as e:
            logger.error(f"Error updating {cls.model.__tablename__}: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Error updating {cls.model.__tablename__}, {str(e)}"
            ) from e

    @classmethod
    async def delete(cls, delete_all: bool = False, **filter_by):
        if not delete_all and not filter_by:
            raise ValueError("You must specify at least one parameter for deletion")
        try:
            async with async_session_maker() as session:
                async with session.begin():
                    query = sqlalchemy_delete(cls.model).filter_by(**filter_by)
                    result = await session.execute(query)
                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                return result.rowcount
        except Exception as e:
            logger.error(f"Error deleting from {cls.model.__tablename__}: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Error deleting from {cls.model.__tablename__}, {str(e)}"
            ) from e

    @classmethod
    async def find_all_in_time_range(
        cls,
        start_time: datetime = None,
        end_time: datetime = None,
        param: str = "created_at",
        **filter_by
    ):
        try:
            async with async_session_maker() as session:
                query = select(cls.model).filter_by(**filter_by)

                if start_time:
                    query = query.where(getattr(cls.model, param) >= start_time)
                if end_time:
                    query = query.where(getattr(cls.model, param) <= end_time)

            result = await session.execute(query)
            return result.scalars().all()
        except Exception as e:
            logger.error(
                f"Error finding all in time range for {cls.model.__tablename__}:"
                f"{str(e)}"
            )
            raise HTTPException(
                status_code=500,
                detail=(
                    f"Error finding all in time range"
                    f"{start_time} {end_time}"
                    f"for {cls.model.__tablename__}, {str(e)}"
                )
            ) from e

    @classmethod
    async def bulk_insert(cls, data: list[dict]):
        try:
            async with async_session_maker() as session:
                async with session.begin():
                    query = insert(cls.model).values(data)
                    result = await session.execute(query)
                    try:
                        await session.commit()
                    except SQLAlchemyError as e:
                        await session.rollback()
                        raise e
                    return result.rowcount
        except Exception as e:
            logger.error(f"Error bulk inserting to {cls.model.__tablename__}: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Error bulk inserting to {cls.model.__tablename__}, {str(e)}"
            ) from e
