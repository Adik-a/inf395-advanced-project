from fastapi import APIRouter, Depends

from modules.jobs.schemas import JobsSchema, JobsUpdateSchema
from modules.jobs.repository import JobsRepository
from modules.offers.schemas import OffersSchema, OffersStatusUpdateSchema
from modules.offers.repository import OffersRepository
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


@router.post("/{job_id}/offer")
async def create_job_offer(
    job_id: int,
    offer_data: OffersSchema,
    session: SessionDep,
    current_user: dict = Depends(get_current_user),
):
    job_data = await JobsRepository.get_job(
        job_id=job_id,
        session=session,
    )

    if not job_data:
        return {"msg": "Job not found"}

    if job_data.user_id == current_user["sub"]:
        return {"msg": "You cannot make an offer on your own job"}

    if offer_data.price is None:
        offer_data.price = job_data.budget

    new_offer = await OffersRepository.create_offer(
        user_id=current_user["sub"],
        job_id=job_id,
        offer_data=offer_data,
        session=session,
    )

    return {
        "msg": "Offer created successfully",
        "offer": new_offer,
    }


@router.get("/{job_id}/offers")
async def get_job_offers(
    job_id: int,
    session: SessionDep,
    current_user: dict = Depends(get_current_user),
):
    job_data = await JobsRepository.get_user_job(
        user_id=current_user["sub"],
        job_id=job_id,
        session=session,
    )

    if not job_data:
        return {"msg": "Job not found"}

    offers = await OffersRepository.get_offers_by_job(
        job_id=job_id,
        session=session,
    )
    return {
        "job": job_data,
        "offers": offers,
    }


@router.patch("/{offer_id}/respond")
async def respond_to_offer(
    offer_id: int,
    status: OffersStatusUpdateSchema,
    session: SessionDep,
    current_user: dict = Depends(get_current_user),
):
    job_offer_data = await JobsRepository.get_user_job_and_offer(
        user_id=current_user["sub"],
        offer_id=offer_id,
        session=session,
    )

    if not job_offer_data:
        return {"msg": "You don't have permission to respond"}
    
    updated_offer = await OffersRepository.update_offer_status(
        offer_id=offer_id,
        status_update=status.status,
        session=session,
    )
    print("🔰"*50)
    print(updated_offer)

    return {
        "msg": "Successfully respond",
        "offer": updated_offer,
    }
