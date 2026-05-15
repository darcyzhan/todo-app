"""TDD 测试: 用户模块"""
import pytest
from httpx import AsyncClient


class TestUserProfile:
    """用户信息测试"""

    async def test_get_me(self, auth_client: AsyncClient):
        """测试: 获取当前用户信息"""
        resp = await auth_client.get("/api/v1/users/me")
        assert resp.status_code == 200
        data = resp.json()
        assert data["nickname"] == "testuser"

    async def test_get_me_unauthorized(self, client: AsyncClient):
        """测试: 未认证获取用户信息失败"""
        resp = await client.get("/api/v1/users/me")
        assert resp.status_code == 403

    async def test_update_me(self, auth_client: AsyncClient):
        """测试: 更新用户信息"""
        resp = await auth_client.put(
            "/api/v1/users/me",
            json={"nickname": "新名字", "timezone": "America/New_York"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["nickname"] == "新名字"
        assert data["timezone"] == "America/New_York"

    async def test_update_theme(self, auth_client: AsyncClient):
        """测试: 更新主题"""
        resp = await auth_client.put("/api/v1/users/me", json={"theme": "dark"})
        assert resp.status_code == 200
        assert resp.json()["theme"] == "dark"
