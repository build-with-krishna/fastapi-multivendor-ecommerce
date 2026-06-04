from fastapi import HTTPException
from sqlalchemy.orm import Session
from jose import jwt
from app.models.user_model import User
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm

from jose import jwt, JWTError

from app.config.settings import settings

from app.utils.password import (
    hash_password,
    verify_password
)

from app.utils.jwt_handler import (
    create_access_token,
    create_refresh_token
)

from app.utils.jwt_handler import create_access_token

SECRET_KEY = "mysecretkey"

ALGORITHM = "HS256"

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

# REGISTER
def register_user(db: Session, user):

    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_user:
        return {
            "error": "Email already exists"
        }

    new_user = User(
        name=user.name,
        email=user.email,
        password=hash_password(user.password),
        role=user.role
    )

    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    return {
        "message": "User registered successfully"
    }


# LOGIN
def login_user(db: Session, user):

    existing_user = db.query(User).filter(
        User.email == user.username
    ).first()

    if not existing_user:

        return {
            "error": "Invalid Email"
        }

    valid_password = verify_password(
        user.password,
        existing_user.password
    )

    if not valid_password:

        return {
            "error": "Invalid Password"
        }

    token_data = {
        "id": existing_user.id,
        "email": existing_user.email,
        "role": existing_user.role
    }

    access_token = create_access_token(
        token_data
    )

    refresh_token = create_refresh_token(
        token_data
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

from jose import jwt, JWTError

from app.config.settings import settings


# REFRESH ACCESS TOKEN
def refresh_access_token(refresh_token: str):

    try:

        payload = jwt.decode(
            refresh_token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        token_type = payload.get("type")

        if token_type != "refresh":

            return {
                "error": "Invalid refresh token"
            }

        new_access_token = create_access_token({
            "id": payload.get("id"),
            "email": payload.get("email"),
            "role": payload.get("role")
        })

        return {
            "access_token": new_access_token
        }

    except JWTError:

        return {
            "error": "Token expired or invalid"
        }