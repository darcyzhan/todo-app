"""TDD 测试: 统计与通知"""
import pytest
from httpx import AsyncClient


class TestStatsDashboard:
    """统计仪表盘测试"""

    async def test_dashboard_empty(self, auth_client: AsyncClient):
        """测试: 空仪表盘"""
        resp = await auth_client.get("/api/v1/stats/dashboard")
        assert resp.status_code == 200
        data = resp.json()
        assert "today_todo" in data
        assert "week_done" in data
        assert "overdue" in data
        assert "in_progress" in data
        assert "completion_rate" in data

    async def test_dashboard_with_tasks(self, auth_client: AsyncClient):
        """测试: 有任务的仪表盘"""
        await auth_client.post("/api/v1/tasks", json={"title": "统计任务1", "status": "done"})
        await auth_client.post("/api/v1/tasks", json={"title": "统计任务2", "status": "in_progress"})

        resp = await auth_client.get("/api/v1/stats/dashboard")
        assert resp.status_code == 200
        data = resp.json()
        assert data["week_done"] >= 1
        assert data["in_progress"] >= 1


class TestNotifications:
    """通知测试"""

    async def test_list_notifications(self, auth_client: AsyncClient):
        """测试: 通知列表"""
        resp = await auth_client.get("/api/v1/notifications")
        assert resp.status_code == 200
        data = resp.json()
        assert "items" in data
        assert "total" in data

    async def test_unread_count(self, auth_client: AsyncClient):
        """测试: 未读数"""
        resp = await auth_client.get("/api/v1/notifications/unread-count")
        assert resp.status_code == 200
        assert "count" in resp.json()

    async def test_mark_all_read(self, auth_client: AsyncClient):
        """测试: 全部已读"""
        resp = await auth_client.put("/api/v1/notifications/read-all")
        assert resp.status_code == 200
        assert "marked_count" in resp.json()
