from fastapi import FastAPI
from backend.urls import router


def include_router(app: FastAPI):
    app.include_router(router)


def start_app():
    app = FastAPI()
    include_router(app)
    return app


app = start_app()
