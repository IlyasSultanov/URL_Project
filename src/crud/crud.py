from sqlalchemy.orm import Session

from model import models
from schems import schemas
from key_gen import keygen


def create_db_url(db: Session, url: schemas.URLBase) -> schemas.URL:
    """
    Creates a new URL in the database, and returns the newly created URL.

    Args:
        db (Session): The database session
        url (schemas.URLBase): The URL to store

    Returns:
        schemas.URL: The newly created URL
    """
    key = keygen.create_unique_random_key(db)
    secret_key = f"{key}_{keygen.create_random_key(length=8)}"

    db_url = models.URL(
    target_url=url.target_url,
    key=key,
    secret_key=secret_key
)

    db.add(db_url)
    db.commit()
    db.refresh(db_url)

    return schemas.URL(
        key=db_url.key,
        secret_key=db_url.secret_key,
        target_url=db_url.target_url,
        clicks=db_url.clicks,
        is_active=db_url.is_active
    )


def get_db_url_by_key(db: Session, key: str) -> schemas.URL | None:
    """
    Get a URL from the database by its key

    Args:
        db (Session): The database session
        key (str): The key of the URL to retrieve

    Returns:
        schemas.URL | None: The retrieved URL or None if not found
    """
    db_url = db.query(models.URL).filter(models.URL.key == key, models.URL.is_active).first()
    if db_url:
        return schemas.URL(
            key=db_url.key,
            secret_key=db_url.secret_key,
            target_url=db_url.target_url,
            clicks=db_url.clicks,
            is_active=db_url.is_active
        )
    return None

def get_db_url_by_secret_key(db: Session, secret_key: str) -> schemas.URL | None:
    """
    Get a URL from the database by its secret key

    Args:
        db (Session): The database session
        secret_key (str): The secret key of the URL to retrieve

    Returns:
        schemas.URL | None: The retrieved URL or None if not found
    """
    db_url = db.query(models.URL).filter(models.URL.secret_key == secret_key, models.URL.is_active).first()
    if db_url:
        return schemas.URL(
            key=db_url.key,
            secret_key=db_url.secret_key,
            target_url=db_url.target_url,
            clicks=db_url.clicks,
            is_active=db_url.is_active
        )
    return None

def update_db_clicks(db: Session, db_url: models.URL) -> schemas.URL:
    """
    Updates the click count of a URL in the database

    Args:
        db (Session): The database session
        db_url (models.URL): The URL to update

    Returns:
        schemas.URL: The updated URL
    """
    db_url.clicks += 1
    db.commit()
    db.refresh(db_url)
    return schemas.URL(
        key=db_url.key,
        secret_key=db_url.secret_key,
        target_url=db_url.target_url,
        clicks=db_url.clicks,
        is_active=db_url.is_active
    )

def deactivate_db_url_by_secret_key(db: Session, secret_key: str) -> schemas.URL | None:
    """
    Deactivates a URL in the database by its secret key

    Args:
        db (Session): The database session
        secret_key (str): The secret key of the URL to deactivate

    Returns:
        schemas.URL | None: The deactivated URL or None if not found
    """
    db_url = db.query(models.URL).filter(models.URL.secret_key == secret_key, models.URL.is_active).first()
    if db_url:
        db_url.is_active = False
        db.commit()
        db.refresh(db_url)
        return schemas.URL(
            key=db_url.key,
            secret_key=db_url.secret_key,
            target_url=db_url.target_url,
            clicks=db_url.clicks,
            is_active=db_url.is_active
        )
    return None
