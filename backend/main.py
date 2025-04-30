from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.generator import generate_ui5_code

app = FastAPI(
    title="SAP UI5 Code Generator",
    description="Erzeugt SAP.m-konformen XML-Code auf Basis von Figma-Layoutdaten",
    version="1.0.0"
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
        xml_code = generate_ui5_code(input.layout)
        return {"xml": xml_code}
    except Exception as e:
        return {"error": str(e)}
