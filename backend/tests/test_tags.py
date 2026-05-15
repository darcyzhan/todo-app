"""TDD 测试: 标签管理"""
import pytest
from httpx import AsyncClient


class TestTagCreate:
    """标签创建测试"""

    async def test_create_tag(self, auth_client: AsyncClient):
        """测试: 创建标签"""
        resp = await auth_client.post(
            "/api/v1/tags",
            json={"name": "工作", "color": "#FF6B6B", "icon": "💼"},
        )
        assert resp.status_code == 201
        data = resp.json()
        assert data["name"] == "工作"
        assert data["color"] == "#FF6B6B"
        assert data["icon"] == "💼"

    async def test_create_tag_default_color(self, auth_client: AsyncClient):
        """测试: 标签默认颜色"""
        resp = await auth_client.post("/api/v1/tags", json={"name": "默认标签"})
        assert resp.status_code == 201
        assert resp.json()["color"] == "#6C5CE7"


class TestTagRead:
    """标签读取测试"""

    async def test_list_tags(self, auth_client: AsyncClient):
        """测试: 标签列表"""
        await auth_client.post("/api/v1/tags", json={"name": "标签A"})
        await auth_client.post("/api/v1/tags", json={"name": "标签B"})

        resp = await auth_client.get("/api/v1/tags")
        assert resp.status_code == 200
        assert len(resp.json()) >= 2

    async def test_get_tag(self, auth_client: AsyncClient):
        """测试: 获取单个标签"""
        create_resp = await auth_client.post("/api/v1/tags", json={"name": "获取标签"})
        tag_id = create_resp.json()["id"]

        resp = await auth_client.get(f"/api/v1/tags/{tag_id}")
        assert resp.status_code == 200
        assert resp.json()["name"] == "获取标签"


class TestTagUpdate:
    """标签更新测试"""

    async def test_update_tag(self, auth_client: AsyncClient):
        """测试: 更新标签"""
        create_resp = await auth_client.post("/api/v1/tags", json={"name": "旧标签"})
        tag_id = create_resp.json()["id"]

        resp = await auth_client.put(
            f"/api/v1/tags/{tag_id}",
            json={"name": "新标签", "color": "#00FF00"},
        )
        assert resp.status_code == 200
        assert resp.json()["name"] == "新标签"


class TestTagDelete:
    """标签删除测试"""

    async def test_delete_tag(self, auth_client: AsyncClient):
        """测试: 删除标签"""
        create_resp = await auth_client.post("/api/v1/tags", json={"name": "待删除标签"})
        tag_id = create_resp.json()["id"]

        resp = await auth_client.delete(f"/api/v1/tags/{tag_id}")
        assert resp.status_code == 204


class TestTaskWithTag:
    """任务关联标签测试"""

    async def test_create_task_with_tags(self, auth_client: AsyncClient):
        """测试: 创建带标签的任务"""
        tag_resp = await auth_client.post("/api/v1/tags", json={"name": "工作标签"})
        tag_id = tag_resp.json()["id"]

        resp = await auth_client.post(
            "/api/v1/tasks",
            json={"title": "带标签任务", "tag_ids": [tag_id]},
        )
        assert resp.status_code == 201
        data = resp.json()
        assert len(data["tags"]) == 1
        assert data["tags"][0]["name"] == "工作标签"
