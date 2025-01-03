import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.framework.middlewares import ExceptionMiddleware
from src.framework.routers import base_router
from src.framework.routers import health_router
from src.framework.settings import get_settings

settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(ExceptionMiddleware)

# Routers
app.include_router(router=health_router)
app.include_router(router=base_router)


@app.get("/health")
async def health():
    return {"status": "OK"}


# For local debugging purposes only
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
