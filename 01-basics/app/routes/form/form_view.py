from typing import Annotated

from fastapi import APIRouter, File, Form, UploadFile

router = APIRouter()


# ! For Form `python-multipart` library needs to install
@router.post("/login")
async def login(
    username: Annotated[str, Form(min_length=1)],
    password: Annotated[str, Form(min_length=1)],
):
    return {"username": username}


@router.post("/files/")
async def create_files(
    files: Annotated[list[bytes], File(description="Multiple files as bytes")],
):
    return {"file_sizes": [len(file) for file in files]}


@router.post("/upload_files/")
async def create_upload_files(
    files: Annotated[
        list[UploadFile], File(description="Multiple files as UploadFile")
    ],
):
    return {"filenames": [file.filename for file in files]}


@router.post("/files-n-form/")
async def create_file(
    file: Annotated[bytes, File()],
    fileb: Annotated[UploadFile, File()],
    token: Annotated[str, Form()],
):
    return {
        "file_size": len(file),
        "token": token,
        "fileb_content_type": fileb.content_type,
    }
