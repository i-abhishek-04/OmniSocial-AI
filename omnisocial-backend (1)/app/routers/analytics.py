"""
Analytics routes.
"""
from fastapi import APIRouter, Depends, HTTPException

from app.core.database import get_db
from app.middleware.auth import get_current_user
from app.models.user import User
from app.schemas.analytics import ConnectPlatformRequest
from app.services import analytics_service
from app.services.platforms.registry import get_adapter
from app.utils.helpers import success_response
from sqlalchemy.orm import Session

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/overview")
def overview(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    data = analytics_service.get_overview(db, current_user.id, current_user.email)
    return success_response(data)


@router.get("/platforms")
def platforms(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    data = analytics_service.get_platform_summaries(db, current_user.id)
    return success_response(data)


@router.get("/platforms/{platform}")
def platform_detail(platform: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    data = analytics_service.get_platform_detail(db, current_user.id, current_user.email, platform)
    if data is None:
        raise HTTPException(status_code=404, detail="Unknown platform")
    return success_response(data)


@router.post("/platforms/{platform}/connect")
async def connect_platform(
    platform: str,
    payload: ConnectPlatformRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    adapter = get_adapter(platform)
    if adapter is None:
        raise HTTPException(status_code=404, detail="Unknown platform")
    if not adapter.is_live:
        raise HTTPException(
            status_code=400,
            detail=f"{adapter.display_name} integration is coming soon and can't be connected yet",
        )
    data = await analytics_service.connect_platform(db, current_user.id, current_user.email, platform, payload.handle)
    if data is None:
        raise HTTPException(status_code=404, detail="Unknown platform")
    return success_response(data, f"{data['display_name']} connected")


@router.post("/platforms/{platform}/disconnect")
def disconnect_platform(platform: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    data = analytics_service.disconnect_platform(db, current_user.id, current_user.email, platform)
    if data is None:
        raise HTTPException(status_code=404, detail="Unknown platform")
    return success_response(data, f"{data['display_name']} disconnected")


@router.get("/revenue")
def revenue(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    data = analytics_service.get_revenue(db, current_user.id, current_user.email)
    return success_response(data)
