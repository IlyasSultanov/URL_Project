import secrets
import string

from sqlalchemy.orm import Session

from crud import crud

def create_random_key(length: int = 5) -> str:
    """
    Generates a random key composed of uppercase letters and digits.

    Args:
        length (int): Length of the key to generate. Defaults to 5.

    Returns:
        str: The generated key
    """
    chars = string.ascii_uppercase + string.digits
    return "".join(secrets.choice(chars) for _ in range(length))

def create_unique_random_key(db: Session) -> str:
    
    """
    Generates a random key that does not already exist in the database.
    
    Args:
        db (Session): SQLAlchemy session
    Returns:
        str: Unique random key
    """
    key = create_random_key()
    while crud.get_db_url_by_key(db, key):
        key = create_random_key()
    return key
