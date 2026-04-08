from datetime import timedelta

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from .models import JobsModel
from .schemas import JobsSchema, JobsUpdateSchema


class JobsRepository:
    @classmethod
    async def create_job(
        cls,
        user_id: int,
        job_data: JobsSchema,
        session: AsyncSession,
    ):
        job_data_dict = job_data.model_dump()
        job_data_dict["duration"] = timedelta(seconds=job_data_dict["duration"])
        new_job = JobsModel(**job_data_dict, user_id=user_id)
        session.add(new_job)
        await session.commit()
        await session.refresh(new_job)

        return new_job

    @classmethod
    async def get_jobs(
        cls,
        session: AsyncSession,
        category: str | None = None,
    ):
        query = select(JobsModel).order_by(JobsModel.created_at.desc())
        if category:
            query = query.where(JobsModel.category == category)

        data = await session.scalars(query)
        return data.all()

    @classmethod
    async def get_job(
        cls,
        job_id: int,
        session: AsyncSession,
    ):
        data = await session.scalar(
            select(JobsModel).where(JobsModel.id == job_id),
        )
        return data

    @classmethod
    async def get_user_job(
        cls,
        user_id: int,
        job_id: int,
        session: AsyncSession,
    ):
        data = await session.scalar(
            select(JobsModel).where(
                JobsModel.user_id == user_id,
                JobsModel.id == job_id,
            )
        )
        return data

    @classmethod
    async def update_job(
        cls,
        job: JobsModel,
        job_update: JobsUpdateSchema,
        session: AsyncSession,
        partial: bool = False,
    ):
        for key, value in job_update.model_dump(exclude_unset=partial).items():
            setattr(job, key, value)

        await session.commit()
        await session.refresh(job)

        return job

    @classmethod
    async def delete_job(
        cls,
        job: JobsModel,
        session: AsyncSession,
    ):
        await session.delete(job)
        await session.commit()
