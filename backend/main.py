from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.generator import generate_ui5_code

app = FastAPI(
    title="UI5 Code Generator",
    version="v1"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LayoutInput(BaseModel):
    layout: list

@app.post("/generate-ui5")
async def generate_code(input: LayoutInput):
    try:
        result = generate_ui5_code(input.layout)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
