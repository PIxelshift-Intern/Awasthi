# app/main.py (updated)
from fastapi import FastAPI
from app.db.db import Base, engine
from app.config import get_settings
from app.api.routes import router
from app.core.logging_config import setup_logging

# Setup logging
setup_logging()

app = FastAPI()
settings = get_settings()

Base.metadata.create_all(bind=engine)

app.include_router(router, prefix=settings.API_V1_STR)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)