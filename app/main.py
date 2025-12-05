from fastapi import FastAPI
from app.core.config import settings
from app.admin import setup_admin
from app.api.v1 import router as api_v1_router


def create_app():
    app = FastAPI(
        title=settings.APP_NAME, 
        version=settings.VERSION
    )
    app.include_router(api_v1_router)

    setup_admin(app=app)
    return app

app = create_app()