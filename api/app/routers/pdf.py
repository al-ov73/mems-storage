import io
import os
import zipfile
from io import BytesIO
from typing import List
from urllib.parse import quote

from fastapi import APIRouter, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse, StreamingResponse
from PyPDF2 import PdfMerger, PdfReader, PdfWriter

from ..config.config import templates
from ..utils.pdf_utils import (
    combine_archives,
    convert_and_pack,
    convert_pdf_to_images,
    get_files_from_session,
    merge_pdfs,
    split_pdf,
)

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "session": request.state.session,
        },
    )


@router.post("/upload")
async def upload_pdf(request: Request, file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Только файлы формата PDF разрешены.")

    content = await file.read()
    memory_file = io.BytesIO(content)

    file_previews = convert_pdf_to_images(memory_file.getvalue())
    filename = file.filename

    new_file = {
        "filename": filename,
        "file_content": memory_file.getvalue(),
        "file_previews": file_previews,
    }
    files = request.state.session.get("files", [])
    files.append(new_file)
    updated_session = {"files": files}
    request.state.session.update(updated_session)

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "session": request.state.session,
        },
    )


@router.get("/split", response_class=HTMLResponse)
async def split_page(request: Request):
    return templates.TemplateResponse(
        "split.html",
        {
            "request": request,
            "session": request.state.session,
        },
    )


@router.post("/split-pdf")
async def split_pdf_page(
    request: Request,
    original_filename: str = Form(...),
    pages: str = Form(...),
    output_name: str = Form("output.pdf"),
):
    files = request.state.session.get("files", {})
    file_content = files.get(original_filename, {}).get("file_content", None)
    if not file_content:
        raise HTTPException(status_code=400, detail="Нет загруженного файла PDF в сессии.")

    output_stream = split_pdf(file_content, pages)

    return StreamingResponse(
        output_stream,
        headers={"Content-Disposition": f"attachment; filename={quote(output_name)}"},
        media_type="application/pdf",
    )


@router.get("/merge", response_class=HTMLResponse)
async def merge_page(request: Request):
    return templates.TemplateResponse(
        "merge.html",
        {
            "request": request,
            "session": request.state.session,
        },
    )


@router.post("/merge-pdfs")
async def merge_pdfs_page(request: Request, filenames: list = Form(...), output_name: str = Form("merged.pdf")):
    session_files = request.state.session.get("files", [])
    merged_bytes = merge_pdfs(filenames, session_files)
    return StreamingResponse(
        merged_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={output_name}"},
    )


@router.get("/convert", response_class=HTMLResponse)
async def convert_page(request: Request):
    return templates.TemplateResponse(
        "convert.html",
        {
            "request": request,
            "session": request.state.session,
        },
    )


@router.post("/convert-pdf-to-jpg")
async def convert_pdf_to_jpg(
    request: Request,
    filenames: list = Form(...),
    dpi: int = Form(300),
    output_name: str = Form("converted"),
):
    requested_files = get_files_from_session(request, filenames)

    individual_archives = []
    for filename, file_content in requested_files.items():
        individual_archive = convert_and_pack(filename, file_content, dpi)
        individual_archives.append(individual_archive)

    combined_archive = combine_archives(individual_archives)

    return StreamingResponse(
        combined_archive,
        media_type="application/zip",
        headers={"Content-Disposition": f"attachment; filename={output_name}.zip"},
    )


# {
#     "files": [
#         {
#             "filename": "example.pdf",
#             "file_content": bytes_object,
#             "file_previews": [...],
#         },
#         {
#             "filename": "another.pdf",
#             "file_content": bytes_object,
#             "file_previews": [...],
#         }
#     ]
# }
