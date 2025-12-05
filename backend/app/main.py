from fastapi import FastAPI
from app.core.config import settings
from app.api.v1.endpoints import cases
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title=settings.PROJECT_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(cases.router, prefix="/api/v1", tags=["Cases"])

@app.get("/")
def root():
    return {"status": "Court is in session"}