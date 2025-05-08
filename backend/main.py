import os
import shutil
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from backend.api.routes import router as api_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for path in ["backend/previews", "backend/feedbacks"]:
    shutil.rmtree(path, ignore_errors=True)
    os.makedirs(path, exist_ok=True)

app.mount("/preview", StaticFiles(directory="backend/previews"), name="pv")
app.mount("/feedback", StaticFiles(directory="backend/feedbacks"), name="fb")


app.include_router(api_router)