from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.config.database import SessionLocal

from app.schemas.user_schema import (
    UserRegister,
    UserLogin
)

from app.schemas.token_schema import (
    RefreshTokenRequest
)

from app.controllers import auth_controller

router = APIRouter()


# DATABASE
def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# REGISTER
@router.post("/register")
def register(
    user: UserRegister,
    db: Session = Depends(get_db)
):
    return auth_controller.register_user(
        db,
        user
    )


# LOGIN
@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    return auth_controller.login_user(
        db,
        form_data
    )

# REFRESH TOKEN
@router.post("/refresh-token")
def refresh_token(data: RefreshTokenRequest):

    return auth_controller.refresh_access_token(
        data.refresh_token
    )