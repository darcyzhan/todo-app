from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token, decode_token
from app.core.exceptions import UnauthorizedException, DuplicateException
from app.core.error_codes import ErrorCode


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def register(self, nickname: str, password: str, avatar_url: str = "") -> dict:
        result = await self.db.execute(select(User).where(User.nickname == nickname))
        if result.scalar_one_or_none():
            raise DuplicateException(ErrorCode.USER_ALREADY_EXISTS, "用户名已存在")

        user = User(
            nickname=nickname,
            hashed_password=hash_password(password),
            avatar_url=avatar_url,
        )
        self.db.add(user)
        await self.db.flush()

        return self._generate_tokens(user)

    async def login(self, nickname: str, password: str) -> dict:
        result = await self.db.execute(select(User).where(User.nickname == nickname))
        user = result.scalar_one_or_none()

        if not user or not user.hashed_password or not verify_password(password, user.hashed_password):
            raise UnauthorizedException(ErrorCode.AUTH_FAILED, "用户名或密码错误")

        return self._generate_tokens(user)

    async def refresh(self, refresh_token: str) -> dict:
        payload = decode_token(refresh_token)
        if payload.get("type") != "refresh":
            raise UnauthorizedException(ErrorCode.TOKEN_INVALID, "无效的 Refresh Token")

        user_id = payload.get("sub")
        result = await self.db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()

        if not user:
            raise UnauthorizedException(ErrorCode.USER_NOT_FOUND)

        return self._generate_tokens(user)

    async def get_or_create_wechat_user(self, openid: str, nickname: str = "微信用户", avatar_url: str = "") -> dict:
        result = await self.db.execute(select(User).where(User.openid == openid))
        user = result.scalar_one_or_none()

        if not user:
            user = User(openid=openid, nickname=nickname, avatar_url=avatar_url)
            self.db.add(user)
            await self.db.flush()

        return self._generate_tokens(user)

    def _generate_tokens(self, user: User) -> dict:
        data = {"sub": user.id}
        access_token = create_access_token(data)
        refresh_token = create_refresh_token(data)
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user_id": user.id,
        }
