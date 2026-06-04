from jose import jwt, JWTError

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session

from app.config.database import SessionLocal

from app.models.user_model import User

from app.config.settings import settings

SECRET_KEY = settings.SECRET_KEY

ALGORITHM = settings.ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login"
)


# DATABASE
def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# CURRENT USER
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("id")

        user = db.query(User).filter(
            User.id == user_id
        ).first()

        if not user:
            raise HTTPException(
                status_code=401,
                detail="Invalid User"
            )

        return user

    except JWTError:

        raise HTTPException(
            status_code=401,
            detail="Invalid Token"
        )