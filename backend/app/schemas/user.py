from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class UserBase(BaseModel):
    nickname: str = Field(default="", max_length=64)
    avatar_url: str = Field(default="", max_length=512)
    timezone: str = Field(default="Asia/Shanghai")
    theme: str = Field(default="auto")
    language: str = Field(default="zh-CN")


class UserCreate(BaseModel):
    openid: str | None = None
    nickname: str = Field(default="新用户", max_length=64)
    avatar_url: str = ""


class UserUpdate(BaseModel):
    nickname: str | None = None
    avatar_url: str | None = None
    timezone: str | None = None
    theme: str | None = None
    language: str | None = None
    settings: dict | None = None


class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: str
    phone: str | None = None
    membership: str = "free"
    is_active: bool = True
    created_at: datetime
    updated_at: datetime


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserResponse


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class WechatLoginRequest(BaseModel):
    code: str
    nickname: str | None = None
    avatar_url: str | None = None
