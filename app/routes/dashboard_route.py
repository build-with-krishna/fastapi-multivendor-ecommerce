from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from app.config.database import SessionLocal

from app.controllers import (
    dashboard_controller
)

from app.utils.auth_middleware import (
    get_current_user
)

router = APIRouter()


# DATABASE
def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# ADMIN DASHBOARD
@router.get("/admin/dashboard")
def admin_dashboard(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    return dashboard_controller.admin_dashboard(
        db,
        current_user
    )


# VENDOR DASHBOARD
@router.get("/vendor/dashboard")
def vendor_dashboard(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    return dashboard_controller.vendor_dashboard(
        db,
        current_user
    )