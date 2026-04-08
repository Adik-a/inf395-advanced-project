from fastapi import APIRouter, Depends

from modules.jobs.schemas import JobsSchema, JobsUpdateSchema
from modules.jobs.repository import JobsRepository
from database import SessionDep
from auth import get_current_user

router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"],
)


@router.post("/create")
async def create_job(
    job_data: JobsSchema,
    session: SessionDep,
    current_user: dict = Depends(get_current_user),
):
    new_job = await JobsRepository.create_job(
        user_id=current_user["sub"], job_data=job_data, session=session
    )

    return {"msg": "Job created successfully", "job": new_job}


@router.get("")
async def get_jobs(
    session: SessionDep,
    category: str | None = None,
    current_user: dict = Depends(get_current_user),
):
    jobs = await JobsRepository.get_jobs(session=session, category=category)

    return jobs


@router.get("/{job_id}")
async def get_job(
    job_id: int,
    session: SessionDep,
    current_user: dict = Depends(get_current_user),
):
    job = await JobsRepository.get_job(
        job_id=job_id,
        session=session,
    )

    if not job:
        return {"msg": "Job not found"}

    return job


@router.patch("/{job_id}")
async def update_job(
    job_id: int,
    job_update: JobsUpdateSchema,
    session: SessionDep,
    current_user: dict = Depends(get_current_user),
):
    job = await JobsRepository.get_user_job(
        user_id=current_user["sub"],
        job_id=job_id,
        session=session,
    )

    if not job:
        return {"msg": "Job not found"}

    updated_job = await JobsRepository.update_job(
        job=job,
        job_update=job_update,
        session=session,
        partial=True,
    )

    return {
        "msg": "Job updated successfully",
        "job": updated_job,
    }


@router.delete("/{job_id}")
async def delete_job(
    job_id: int,
    session: SessionDep,
    current_user: dict = Depends(get_current_user),
):
    job = await JobsRepository.get_user_job(
        user_id=current_user["sub"],
        job_id=job_id,
        session=session,
    )

    if not job:
        return {"msg": "Job not found"}
    
    await JobsRepository.delete_job(
        job=job,
        session=session,
    )

    return {"msg": "Job deleted successfully"}
