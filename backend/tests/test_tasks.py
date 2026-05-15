"""TDD 测试: 任务核心 CRUD"""
import pytest
from httpx import AsyncClient


class TestTaskCreate:
    """任务创建测试"""

    async def test_create_basic_task(self, auth_client: AsyncClient):
        """测试: 创建基础任务"""
        resp = await auth_client.post(
            "/api/v1/tasks",
            json={"title": "完成项目报告"},
        )
        assert resp.status_code == 201
        data = resp.json()
        assert data["title"] == "完成项目报告"
        assert data["status"] == "todo"
        assert data["priority"] == "P2"
        assert data["id"] is not None

    async def test_create_task_with_all_fields(self, auth_client: AsyncClient):
        """测试: 创建带完整字段的任务"""
        resp = await auth_client.post(
            "/api/v1/tasks",
            json={
                "title": "重要会议",
                "description": "季度复盘会议",
                "status": "in_progress",
                "priority": "P0",
                "due_date": "2026-12-31T23:59:59",
                "estimated_duration": 120,
                "energy_level": "high",
                "tag_ids": [],
                "assignee_ids": [],
                "subtasks": ["准备PPT", "整理数据"],
            },
        )
        assert resp.status_code == 201
        data = resp.json()
        assert data["status"] == "in_progress"
        assert data["priority"] == "P0"
        assert len(data["subtasks"]) == 2
        assert data["subtasks"][0]["title"] == "准备PPT"

    async def test_create_task_empty_title(self, auth_client: AsyncClient):
        """测试: 空标题创建失败"""
        resp = await auth_client.post("/api/v1/tasks", json={"title": ""})
        assert resp.status_code == 422

    async def test_create_task_invalid_priority(self, auth_client: AsyncClient):
        """测试: 无效优先级创建失败"""
        resp = await auth_client.post(
            "/api/v1/tasks",
            json={"title": "test", "priority": "P5"},
        )
        assert resp.status_code == 422


class TestTaskRead:
    """任务读取测试"""

    async def test_get_task(self, auth_client: AsyncClient):
        """测试: 获取单个任务"""
        create_resp = await auth_client.post(
            "/api/v1/tasks", json={"title": "待查看任务"}
        )
        task_id = create_resp.json()["id"]

        resp = await auth_client.get(f"/api/v1/tasks/{task_id}")
        assert resp.status_code == 200
        assert resp.json()["title"] == "待查看任务"

    async def test_get_task_not_found(self, auth_client: AsyncClient):
        """测试: 获取不存在任务 404"""
        resp = await auth_client.get("/api/v1/tasks/nonexistent-id")
        assert resp.status_code == 404

    async def test_list_tasks(self, auth_client: AsyncClient):
        """测试: 任务列表"""
        await auth_client.post("/api/v1/tasks", json={"title": "任务A"})
        await auth_client.post("/api/v1/tasks", json={"title": "任务B"})

        resp = await auth_client.get("/api/v1/tasks")
        assert resp.status_code == 200
        data = resp.json()
        assert data["total"] >= 2
        assert len(data["items"]) >= 2

    async def test_list_tasks_filter_status(self, auth_client: AsyncClient):
        """测试: 按状态筛选任务"""
        await auth_client.post("/api/v1/tasks", json={"title": "筛选任务", "status": "done"})

        resp = await auth_client.get("/api/v1/tasks?status=done")
        assert resp.status_code == 200
        for item in resp.json()["items"]:
            assert item["status"] == "done"

    async def test_list_tasks_search(self, auth_client: AsyncClient):
        """测试: 搜索任务"""
        await auth_client.post("/api/v1/tasks", json={"title": "独特搜索关键词任务"})

        resp = await auth_client.get("/api/v1/tasks?q=独特搜索关键词")
        assert resp.status_code == 200
        data = resp.json()
        assert data["total"] >= 1


class TestTaskUpdate:
    """任务更新测试"""

    async def test_update_task_title(self, auth_client: AsyncClient):
        """测试: 更新任务标题"""
        create_resp = await auth_client.post(
            "/api/v1/tasks", json={"title": "旧标题"}
        )
        task_id = create_resp.json()["id"]

        resp = await auth_client.put(
            f"/api/v1/tasks/{task_id}",
            json={"title": "新标题"},
        )
        assert resp.status_code == 200
        assert resp.json()["title"] == "新标题"

    async def test_update_task_status_to_done(self, auth_client: AsyncClient):
        """测试: 更新状态为完成"""
        create_resp = await auth_client.post(
            "/api/v1/tasks", json={"title": "待完成任务"}
        )
        task_id = create_resp.json()["id"]

        resp = await auth_client.put(
            f"/api/v1/tasks/{task_id}/status",
            json={"status": "done"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "done"
        assert data["completed_at"] is not None

    async def test_update_task_priority(self, auth_client: AsyncClient):
        """测试: 更新优先级"""
        create_resp = await auth_client.post(
            "/api/v1/tasks", json={"title": "优先级任务", "priority": "P3"}
        )
        task_id = create_resp.json()["id"]

        resp = await auth_client.put(
            f"/api/v1/tasks/{task_id}",
            json={"priority": "P0"},
        )
        assert resp.status_code == 200
        assert resp.json()["priority"] == "P0"


class TestTaskDelete:
    """任务删除测试"""

    async def test_delete_task(self, auth_client: AsyncClient):
        """测试: 删除任务"""
        create_resp = await auth_client.post(
            "/api/v1/tasks", json={"title": "待删除任务"}
        )
        task_id = create_resp.json()["id"]

        resp = await auth_client.delete(f"/api/v1/tasks/{task_id}")
        assert resp.status_code == 204

        get_resp = await auth_client.get(f"/api/v1/tasks/{task_id}")
        assert get_resp.status_code == 404

    async def test_delete_nonexistent_task(self, auth_client: AsyncClient):
        """测试: 删除不存在任务"""
        resp = await auth_client.delete("/api/v1/tasks/nonexistent-id")
        assert resp.status_code == 404


class TestTaskBatch:
    """批量操作测试"""

    async def test_batch_update_status(self, auth_client: AsyncClient):
        """测试: 批量更新状态"""
        t1 = (await auth_client.post("/api/v1/tasks", json={"title": "批量1"})).json()["id"]
        t2 = (await auth_client.post("/api/v1/tasks", json={"title": "批量2"})).json()["id"]

        resp = await auth_client.post(
            "/api/v1/tasks/batch",
            json={"task_ids": [t1, t2], "status": "done"},
        )
        assert resp.status_code == 200
        data = resp.json()
        for task in data:
            assert task["status"] == "done"


class TestSubtask:
    """子任务测试"""

    async def test_create_subtask(self, auth_client: AsyncClient):
        """测试: 创建子任务"""
        task_id = (await auth_client.post(
            "/api/v1/tasks", json={"title": "父任务", "subtasks": ["子任务1"]}
        )).json()["id"]

        resp = await auth_client.post(
            f"/api/v1/tasks/{task_id}/subtasks",
            json={"title": "子任务2"},
        )
        assert resp.status_code == 201
        assert resp.json()["title"] == "子任务2"

    async def test_update_subtask_toggle(self, auth_client: AsyncClient):
        """测试: 切换子任务完成状态"""
        task_id = (await auth_client.post(
            "/api/v1/tasks", json={"title": "子任务切换", "subtasks": ["待切换"]}
        )).json()["id"]

        create_resp = await auth_client.get(f"/api/v1/tasks/{task_id}")
        subtask_id = create_resp.json()["subtasks"][0]["id"]

        resp = await auth_client.put(
            f"/api/v1/tasks/subtasks/{subtask_id}",
            json={"is_completed": True},
        )
        assert resp.status_code == 200
        assert resp.json()["is_completed"] is True

    async def test_delete_subtask(self, auth_client: AsyncClient):
        """测试: 删除子任务"""
        task_id = (await auth_client.post(
            "/api/v1/tasks", json={"title": "删子任务", "subtasks": ["待删除子任务"]}
        )).json()["id"]

        create_resp = await auth_client.get(f"/api/v1/tasks/{task_id}")
        subtask_id = create_resp.json()["subtasks"][0]["id"]

        resp = await auth_client.delete(f"/api/v1/tasks/subtasks/{subtask_id}")
        assert resp.status_code == 204
