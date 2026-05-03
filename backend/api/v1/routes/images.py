import asyncio
from typing import List

from fastapi import APIRouter, status, UploadFile, File
from fastapi.concurrency import run_in_threadpool
import cloudinary.uploader

router = APIRouter(
    tags=["Images"],
)


@router.post("/upload-image", status_code=status.HTTP_201_CREATED)
async def upload_image(
    file: UploadFile = File(...),
):
    result = await run_in_threadpool(cloudinary.uploader.upload, file.file)
    url = result.get("secure_url")

    return {"url": url}


@router.post("/upload-images", status_code=status.HTTP_201_CREATED)
async def upload_images(
    files: List[UploadFile] = File(...),
):
    tasks = [run_in_threadpool(cloudinary.uploader.upload, file.file) for file in files]
    results = await asyncio.gather(*tasks)
    
    urls = [res.get("secure_url") for res in results]

    return {"urls": urls}
