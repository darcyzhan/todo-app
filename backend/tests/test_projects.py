"""TDD 测试: 项目管理"""
import pytest
from httpx import AsyncClient


class TestProjectCreate:
    """项目创建测试"""

    async def test_create_project(self, auth_client: AsyncClient):
        """测试: 创建项目"""
        resp = await auth_client.post(
            "/api/v1/projects",
            json={"name": "新产品发布", "icon": "🚀", "color": "#FF6B6B"},
        )
        assert resp.status_code == 201
        data = resp.json()
        assert data["name"] == "新产品发布"
        assert data["icon"] == "🚀"
        assert data["owner_id"] == auth_client._test_user_id
        assert len(data["members"]) == 1
        assert data["members"][0]["role"] == "admin"

    async def test_create_project_default_values(self, auth_client: AsyncClient):
        """测试: 创建项目默认值"""
        resp = await auth_client.post(
            "/api/v1/projects", json={"name": "默认项目"}
        )
        assert resp.status_code == 201
        data = resp.json()
        assert data["icon"] == "📋"
        assert data["color"] == "#6C5CE7"


class TestProjectRead:
    """项目读取测试"""

    async def test_list_projects(self, auth_client: AsyncClient):
        """测试: 项目列表"""
        await auth_client.post("/api/v1/projects", json={"name": "项目A"})
        await auth_client.post("/api/v1/projects", json={"name": "项目B"})

        resp = await auth_client.get("/api/v1/projects")
        assert resp.status_code == 200
        assert len(resp.json()) >= 2

    async def test_get_project(self, auth_client: AsyncClient):
        """测试: 获取单个项目"""
        create_resp = await auth_client.post(
            "/api/v1/projects", json={"name": "查看项目"}
        )
        project_id = create_resp.json()["id"]

        resp = await auth_client.get(f"/api/v1/projects/{project_id}")
        assert resp.status_code == 200
        assert resp.json()["name"] == "查看项目"

    async def test_get_project_not_found(self, auth_client: AsyncClient):
        """测试: 获取不存在项目"""
        resp = await auth_client.get("/api/v1/projects/nonexistent")
        assert resp.status_code == 404


class TestProjectUpdate:
    """项目更新测试"""

    async def test_update_project(self, auth_client: AsyncClient):
        """测试: 更新项目"""
        create_resp = await auth_client.post(
            "/api/v1/projects", json={"name": "旧名称"}
        )
        project_id = create_resp.json()["id"]

        resp = await auth_client.put(
            f"/api/v1/projects/{project_id}",
            json={"name": "新名称", "color": "#FF0000"},
        )
        assert resp.status_code == 200
        assert resp.json()["name"] == "新名称"
        assert resp.json()["color"] == "#FF0000"


class TestProjectDelete:
    """项目删除测试"""

    async def test_delete_project(self, auth_client: AsyncClient):
        """测试: 删除项目"""
        create_resp = await auth_client.post(
            "/api/v1/projects", json={"name": "待删除"}
        )
        project_id = create_resp.json()["id"]

        resp = await auth_client.delete(f"/api/v1/projects/{project_id}")
        assert resp.status_code == 204

        get_resp = await auth_client.get(f"/api/v1/projects/{project_id}")
        assert get_resp.status_code == 404


class TestProjectStats:
    """项目统计测试"""

    async def test_project_stats(self, auth_client: AsyncClient):
        """测试: 项目统计"""
        create_resp = await auth_client.post(
            "/api/v1/projects", json={"name": "统计项目"}
        )
        project_id = create_resp.json()["id"]

        await auth_client.post(
            "/api/v1/tasks",
            json={"title": "任务1", "project_id": project_id, "status": "todo"},
        )
        await auth_client.post(
            "/api/v1/tasks",
            json={"title": "任务2", "project_id": project_id, "status": "done"},
        )

        resp = await auth_client.get(f"/api/v1/projects/{project_id}/stats")
        assert resp.status_code == 200
        data = resp.json()
        assert data["total_tasks"] == 2
        assert data["done_count"] == 1
