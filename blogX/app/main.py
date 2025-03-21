from fastapi import FastAPI
from app.database.db import Base, engine
from app.core.config import get_settings
from app.routers.auth import router as auth_router
from app.routers.blog import router as blog_router
from app.routers.comments import router as comment_router
from app.core.logging_config import setup_logging

setup_logging()

app = FastAPI()
settings = get_settings()

Base.metadata.create_all(bind=engine)

app.include_router(auth_router)
app.include_router(blog_router)
app.include_router(comment_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)