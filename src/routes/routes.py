from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from schems import schemas 
from crud import crud
from db import database

router = APIRouter()

def get_db():
    """
    Dependency function that returns a database session.

    Yields a database session object using a context manager, ensuring that the session
    is properly closed after it is used.
    """
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/url/", response_model=schemas.URL)
def create_url(url: schemas.URLBase, db: Session = Depends(get_db)):
    return crud.create_db_url(db, url)

    """
    Creates a new URL in the database, and returns the newly created URL.

    Args:
        url (schemas.URLBase): The URL to store
        db (Session): The database session

    Returns:
        schemas.URL: The newly created URL
    """
    return crud.create_db_url(db, url)


@router.get("/{key}")  
def redirect_url(key: str, db: Session = Depends(get_db)):
    """
    Redirects the user to the target URL of the given shortened URL.

    Args:
        key (str): The shortened URL key
        db (Session): The database session

    Raises:
        HTTPException: If the URL is not found

    Returns:
        RedirectResponse: The response to redirect the user to the target URL
    """
    db_url = crud.get_db_url_by_key(db, key)
    if not db_url:
        raise HTTPException(status_code=404, detail="URL not found")
    return RedirectResponse(url=db_url.target_url)


@router.delete("/url/{secret_key}")
def deactivate_url(secret_key: str, db: Session = Depends(get_db)):
    """
    Deactivates a URL in the database by its secret key.

    Args:
        secret_key (str): The secret key of the URL to deactivate.
        db (Session): The database session.

    Returns:
        dict: A message indicating the URL has been deactivated.

    Raises:
        HTTPException: If the URL is not found or is already inactive.
    """

    db_url = crud.deactivate_db_url_by_secret_key(db, secret_key)
    if not db_url:
        raise HTTPException(status_code=404, detail="URL not found or already inactive")
    return {"message": "URL deactivated"}
