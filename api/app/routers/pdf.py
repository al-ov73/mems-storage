from fastapi import Depends, Form, APIRouter, Request
import os
from fastapi import Request, UploadFile, Form, File, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from typing import List
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from pdf2image import convert_from_path
import shutil

from ..config.config import templates

async def get_session_id(request: Request) -> str:
    return request.cookies.get("session_id")


router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.post("/upload")
async def upload_pdf(request: Request, file: UploadFile = File(...)):
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    file_path = f"uploads/{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    request.state.session["current_file"] = file.filename
    return RedirectResponse(url="/pdf/split", status_code=303)

@router.get("/split", response_class=HTMLResponse)
async def split_page(request: Request):
    current_file = request.state.session.get("current_file", "")
    return templates.TemplateResponse("split.html", {
        "request": request,
        "filename": current_file
    })

@router.post("/split-pdf")
async def split_pdf(
    request: Request,
    pages: str = Form(...),
    output_name: str = Form("output.pdf"),
):
    filename = request.state.session.get("current_file", "")
    if not filename:
        return RedirectResponse(url="/", status_code=303)
    
    input_path = f"uploads/{filename}"
    output_path = f"uploads/{output_name}"
    
    # Parse pages (e.g., "1-3,5,7-9")
    page_ranges = []
    for part in pages.split(","):
        if "-" in part:
            start, end = map(int, part.split("-"))
            page_ranges.extend(range(start-1, end))
        else:
            page_ranges.append(int(part)-1)
    
    reader = PdfReader(input_path)
    writer = PdfWriter()
    
    for page_num in page_ranges:
        if 0 <= page_num < len(reader.pages):
            writer.add_page(reader.pages[page_num])
    
    with open(output_path, "wb") as output_file:
        writer.write(output_file)
    
    return FileResponse(
        output_path,
        filename=output_name,
        media_type="application/pdf"
    )

@router.get("/merge", response_class=HTMLResponse)
async def merge_page(request: Request):
    pdf_files = [f for f in os.listdir("uploads") if f.lower().endswith(".pdf")]
    return templates.TemplateResponse("merge.html", {
        "request": request,
        "pdf_files": pdf_files
    })

@router.post("/merge-pdfs")
async def merge_pdfs(
    files: List[str] = Form(...),
    output_name: str = Form("merged.pdf")
):
    merger = PdfMerger()
    output_path = f"uploads/{output_name}"
    
    for filename in files:
        file_path = f"uploads/{filename}"
        merger.append(file_path)
    
    merger.write(output_path)
    merger.close()
    
    return FileResponse(
        output_path,
        filename=output_name,
        media_type="application/pdf"
    )

@router.get("/convert", response_class=HTMLResponse)
async def convert_page(request: Request):
    current_file = request.state.session.get("current_file", "")
    return templates.TemplateResponse("convert.html", {
        "request": request,
        "filename": current_file
    })

@router.post("/convert-pdf-to-jpg")
async def convert_pdf_to_jpg(
    request: Request,
    dpi: int = Form(300),
    output_name: str = Form("converted"),
):
    filename = request.state.session.get("current_file", "")
    if not filename:
        return RedirectResponse(url="/pdf", status_code=303)
    
    input_path = f"uploads/{filename}"
    
    images = convert_from_path(input_path, dpi=dpi)

    output_dir = "uploads/converted"
    os.makedirs(output_dir, exist_ok=True)
    
    output_files = []
    for i, image in enumerate(images):
        output_path = f"{output_dir}/{output_name}_{i+1}.jpg"
        image.save(output_path, "JPEG")
        output_files.append(output_path)
    
    # Create a zip if multiple files
    if len(output_files) > 1:
        import zipfile
        zip_path = f"uploads/{output_name}.zip"
        with zipfile.ZipFile(zip_path, "w") as zipf:
            for file in output_files:
                zipf.write(file, os.path.basename(file))
        
        return FileResponse(
            zip_path,
            filename=f"{output_name}.zip",
            media_type="application/zip"
        )
    else:
        return FileResponse(
            output_files[0],
            filename=f"{output_name}.jpg",
            media_type="image/jpeg"
        )