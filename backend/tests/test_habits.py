"""TDD 测试: 习惯追踪"""
import pytest
from httpx import AsyncClient
from datetime import date


class TestHabitCreate:
    """习惯创建测试"""

    async def test_create_habit(self, auth_client: AsyncClient):
        """测试: 创建习惯"""
        resp = await auth_client.post(
            "/api/v1/habits",
            json={"title": "每天运动", "icon": "🏃", "color": "#00B894"},
        )
        assert resp.status_code == 201
        data = resp.json()
        assert data["title"] == "每天运动"
        assert data["icon"] == "🏃"
        assert data["streak"] == 0
        assert data["today_logged"] is False

    async def test_create_habit_default(self, auth_client: AsyncClient):
        """测试: 习惯默认值"""
        resp = await auth_client.post("/api/v1/habits", json={"title": "阅读"})
        assert resp.status_code == 201
        data = resp.json()
        assert data["icon"] == "✅"
        assert data["color"] == "#6C5CE7"


class TestHabitRead:
    """习惯读取测试"""

    async def test_list_habits(self, auth_client: AsyncClient):
        """测试: 习惯列表"""
        await auth_client.post("/api/v1/habits", json={"title": "习惯A"})
        await auth_client.post("/api/v1/habits", json={"title": "习惯B"})

        resp = await auth_client.get("/api/v1/habits")
        assert resp.status_code == 200
        assert len(resp.json()) >= 2

    async def test_get_habit(self, auth_client: AsyncClient):
        """测试: 获取单个习惯"""
        create_resp = await auth_client.post("/api/v1/habits", json={"title": "查看习惯"})
        habit_id = create_resp.json()["id"]

        resp = await auth_client.get(f"/api/v1/habits/{habit_id}")
        assert resp.status_code == 200
        assert resp.json()["title"] == "查看习惯"


class TestHabitUpdate:
    """习惯更新测试"""

    async def test_update_habit(self, auth_client: AsyncClient):
        """测试: 更新习惯"""
        create_resp = await auth_client.post("/api/v1/habits", json={"title": "旧习惯"})
        habit_id = create_resp.json()["id"]

        resp = await auth_client.put(
            f"/api/v1/habits/{habit_id}",
            json={"title": "新习惯", "color": "#FF0000"},
        )
        assert resp.status_code == 200
        assert resp.json()["title"] == "新习惯"


class TestHabitDelete:
    """习惯删除测试"""

    async def test_delete_habit(self, auth_client: AsyncClient):
        """测试: 删除习惯"""
        create_resp = await auth_client.post("/api/v1/habits", json={"title": "待删除习惯"})
        habit_id = create_resp.json()["id"]

        resp = await auth_client.delete(f"/api/v1/habits/{habit_id}")
        assert resp.status_code == 204


class TestHabitLog:
    """习惯打卡测试"""

    async def test_log_habit(self, auth_client: AsyncClient):
        """测试: 习惯打卡"""
        create_resp = await auth_client.post("/api/v1/habits", json={"title": "打卡习惯"})
        habit_id = create_resp.json()["id"]

        today = date.today().isoformat()
        resp = await auth_client.post(f"/api/v1/habits/{habit_id}/log?logged_date={today}")
        assert resp.status_code == 201
        assert resp.json()["habit_id"] == habit_id

        # 验证今日已打卡
        habit_resp = await auth_client.get(f"/api/v1/habits/{habit_id}")
        assert habit_resp.json()["today_logged"] is True

    async def test_log_habit_duplicate(self, auth_client: AsyncClient):
        """测试: 重复打卡失败"""
        create_resp = await auth_client.post("/api/v1/habits", json={"title": "重复打卡"})
        habit_id = create_resp.json()["id"]

        today = date.today().isoformat()
        await auth_client.post(f"/api/v1/habits/{habit_id}/log?logged_date={today}")
        resp = await auth_client.post(f"/api/v1/habits/{habit_id}/log?logged_date={today}")
        assert resp.status_code == 409

    async def test_unlog_habit(self, auth_client: AsyncClient):
        """测试: 取消打卡"""
        create_resp = await auth_client.post("/api/v1/habits", json={"title": "取消打卡"})
        habit_id = create_resp.json()["id"]

        today = date.today().isoformat()
        await auth_client.post(f"/api/v1/habits/{habit_id}/log?logged_date={today}")
        resp = await auth_client.delete(f"/api/v1/habits/{habit_id}/log/{today}")
        assert resp.status_code == 204

    async def test_habit_streak(self, auth_client: AsyncClient):
        """测试: 连续天数计算"""
        create_resp = await auth_client.post("/api/v1/habits", json={"title": "连续打卡"})
        habit_id = create_resp.json()["id"]

        # 今天打卡
        today = date.today().isoformat()
        await auth_client.post(f"/api/v1/habits/{habit_id}/log?logged_date={today}")

        habit_resp = await auth_client.get(f"/api/v1/habits/{habit_id}")
        assert habit_resp.json()["streak"] >= 1
