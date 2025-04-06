from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fastapi_pagination import add_pagination

from app.core.config import settings
from app.api.endpoints import router as api_router


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
)
add_pagination(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)

app.include_router(api_router, prefix="/api")

@app.get('/')
async def index():
    return {"Service": "TRON scanner"}
