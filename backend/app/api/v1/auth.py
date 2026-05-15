from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.user import WechatLoginRequest, RefreshTokenRequest, UserUpdate, UserResponse, TokenResponse
from app.services.auth_service import AuthService
from app.models.user import User
from app.core.security import get_current_user

router = APIRouter(prefix="/auth", tags=["认证"])


@router.post("/register", response_model=TokenResponse)
async def register(nickname: str, password: str, db: AsyncSession = Depends(get_db)):
    service = AuthService(db)
    result = await service.register(nickname, password)
    user_result = await db.execute(
        __import__("sqlalchemy", fromlist=["select"]).select(User).where(User.id == result["user_id"])
    )
    user = user_result.scalar_one()
    return TokenResponse(
        access_token=result["access_token"],
        refresh_token=result["refresh_token"],
        user=UserResponse.model_validate(user),
    )


@router.post("/login", response_model=TokenResponse)
async def login(nickname: str, password: str, db: AsyncSession = Depends(get_db)):
    service = AuthService(db)
    result = await service.login(nickname, password)
    from sqlalchemy import select
    user_result = await db.execute(select(User).where(User.id == result["user_id"]))
    user = user_result.scalar_one()
    return TokenResponse(
        access_token=result["access_token"],
        refresh_token=result["refresh_token"],
        user=UserResponse.model_validate(user),
    )


@router.post("/wechat-login", response_model=TokenResponse)
async def wechat_login(data: WechatLoginRequest, db: AsyncSession = Depends(get_db)):
    service = AuthService(db)
    result = await service.get_or_create_wechat_user(
        openid=f"wx_{data.code}", nickname=data.nickname, avatar_url=data.avatar_url or ""
    )
    from sqlalchemy import select
    user_result = await db.execute(select(User).where(User.id == result["user_id"]))
    user = user_result.scalar_one()
    return TokenResponse(
        access_token=result["access_token"],
        refresh_token=result["refresh_token"],
        user=UserResponse.model_validate(user),
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(data: RefreshTokenRequest, db: AsyncSession = Depends(get_db)):
    service = AuthService(db)
    result = await service.refresh(data.refresh_token)
    from sqlalchemy import select
    user_result = await db.execute(select(User).where(User.id == result["user_id"]))
    user = user_result.scalar_one()
    return TokenResponse(
        access_token=result["access_token"],
        refresh_token=result["refresh_token"],
        user=UserResponse.model_validate(user),
    )
