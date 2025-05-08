from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Dict

from backend.ui5.generator import generate_ui5_code
from backend.ui5.preview import generate_ui5_preview_html
from backend.ui5.feedback import get_ui5_feedback, generate_feedback_html

router = APIRouter()

class LayoutInput(BaseModel):
    layout: list

class PreviewInput(BaseModel):
    xml: str

class FeedbackReviewInput(BaseModel):
    versions: List[str]
    messages: List[Dict[str, str]]

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
        return JSONResponse(content={"url": f"http://localhost:8000{preview_path}"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/feedback-ui5")
async def render_feedback_view(data: PreviewInput):
    try:
        feedback_path = generate_feedback_html(data.xml)
        return JSONResponse(content={"url": f"http://localhost:8000{feedback_path}"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/review-ui5")
async def review_ui5_code(data: FeedbackReviewInput):
    try:
        result = get_ui5_feedback(data.versions, data.messages)
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))