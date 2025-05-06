from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from backend.ui5.generator import generate_ui5_code
from backend.ui5.preview import generate_ui5_preview_html

router = APIRouter()

class LayoutInput(BaseModel):
    layout: list

class PreviewInput(BaseModel):
    xml: str

@router.post("/generate-ui5")
async def generate_code(input: LayoutInput):
    try:
        return generate_ui5_code(input.layout)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/preview-ui5")
async def render_ui5_preview(data: PreviewInput):
    try:
        preview_path = generate_ui5_preview_html(data.xml)
        return JSONResponse(content={ "url": f"http://localhost:8000{preview_path}" })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))