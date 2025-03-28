from fastapi import FastAPI
from db.database import engine
from model.models import Base
from routes.routes import router

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(router)


@app.get("/")
def read_root():
    """
    Root endpoint that returns a welcome message for the URL Shortener API.

    Returns:
        str: Welcome message for the API.
    """

    return "Welcome to the URL Shortener API!"

