from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.core.security import get_current_user
from app.services.user import UserService
from app.schemas.user import UserInDB, UserUpdate, SuccessResponse


router = APIRouter()
user_service = UserService()


@router.get("/profile", response_model=UserInDB)
async def get_user_profile(current_user: UserInDB = Depends(get_current_user)):
    return current_user


@router.put("/profile", response_model=UserInDB)
async def update_user_profile(
    user_update: UserUpdate,
    current_user: UserInDB = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    updated_user = await user_service.update_user(db, current_user.id, user_update)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user


@router.delete("/profile", response_model=SuccessResponse)
async def delete_user_profile(
    current_user: UserInDB = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    deleted = await user_service.delete_user(db, current_user.id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return SuccessResponse(success=True, message="User deleted successfully")