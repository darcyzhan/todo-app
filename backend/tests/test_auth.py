"""TDD 测试: 用户认证模块"""
import pytest
from httpx import AsyncClient


class TestAuthRegister:
    """用户注册测试"""

    async def test_register_success(self, client: AsyncClient):
        """测试: 正常注册成功"""
        resp = await client.post("/api/v1/auth/register?nickname=newuser&password=pass123")
        assert resp.status_code == 200
        data = resp.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"
        assert data["user"]["nickname"] == "newuser"

    async def test_register_duplicate(self, client: AsyncClient):
        """测试: 重复注册失败"""
        await client.post("/api/v1/auth/register?nickname=dupuser&password=pass123")
        resp = await client.post("/api/v1/auth/register?nickname=dupuser&password=pass123")
        assert resp.status_code == 409


class TestAuthLogin:
    """用户登录测试"""

    async def test_login_success(self, client: AsyncClient):
        """测试: 正常登录成功"""
        await client.post("/api/v1/auth/register?nickname=loginuser&password=pass123")
        resp = await client.post("/api/v1/auth/login?nickname=loginuser&password=pass123")
        assert resp.status_code == 200
        data = resp.json()
        assert "access_token" in data
        assert "refresh_token" in data

    async def test_login_wrong_password(self, client: AsyncClient):
        """测试: 错误密码登录失败"""
        await client.post("/api/v1/auth/register?nickname=wrongpw&password=pass123")
        resp = await client.post("/api/v1/auth/login?nickname=wrongpw&password=wrongpw")
        assert resp.status_code == 401

    async def test_login_nonexistent_user(self, client: AsyncClient):
        """测试: 不存在用户登录失败"""
        resp = await client.post("/api/v1/auth/login?nickname=ghost&password=pass123")
        assert resp.status_code == 401


class TestAuthTokenRefresh:
    """Token 刷新测试"""

    async def test_refresh_success(self, client: AsyncClient):
        """测试: 使用 refresh_token 刷新成功"""
        resp = await client.post("/api/v1/auth/register?nickname=refreshuser&password=pass123")
        data = resp.json()
        refresh_resp = await client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": data["refresh_token"]},
        )
        assert refresh_resp.status_code == 200
        new_data = refresh_resp.json()
        assert "access_token" in new_data

    async def test_refresh_invalid_token(self, client: AsyncClient):
        """测试: 无效 refresh_token 刷新失败"""
        resp = await client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": "invalid_token"},
        )
        assert resp.status_code == 401


class TestWechatLogin:
    """微信登录测试"""

    async def test_wechat_login_new_user(self, client: AsyncClient):
        """测试: 微信新用户自动创建"""
        resp = await client.post(
            "/api/v1/auth/wechat-login",
            json={"code": "test_code_001", "nickname": "微信用户", "avatar_url": ""},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert "access_token" in data

    async def test_wechat_login_existing_user(self, client: AsyncClient):
        """测试: 微信已有用户直接登录"""
        resp1 = await client.post(
            "/api/v1/auth/wechat-login",
            json={"code": "test_code_002", "nickname": "用户1"},
        )
        resp2 = await client.post(
            "/api/v1/auth/wechat-login",
            json={"code": "test_code_002", "nickname": "用户1"},
        )
        assert resp2.status_code == 200
        assert resp1.json()["user"]["id"] == resp2.json()["user"]["id"]
