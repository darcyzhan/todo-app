# TodoMaster Pro - API 接口文档

> 基础路径: `http://localhost:51200/api/v1`
> 认证方式: Bearer Token (JWT)
> 在线文档: `http://localhost:51200/docs`

## 一、认证模块 `/auth`

### 1.1 用户注册

```
POST /auth/register
```

**请求参数 (Query):**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| nickname | string | 是 | 用户昵称 |
| password | string | 是 | 密码 (≥6位) |

**响应示例:**

```json
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "nickname": "testuser",
    "created_at": "2026-01-01T00:00:00"
  }
}
```

### 1.2 用户登录

```
POST /auth/login
```

**请求参数 (Query):**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| nickname | string | 是 | 用户昵称 |
| password | string | 是 | 密码 |

**响应:** 同注册接口

### 1.3 刷新令牌

```
POST /auth/refresh
```

**请求体:**

```json
{
  "refresh_token": "eyJ..."
}
```

**响应:**

```json
{
  "access_token": "eyJ...",
  "token_type": "bearer"
}
```

---

## 二、用户模块 `/users`

### 2.1 获取当前用户信息

```
GET /users/me
Authorization: Bearer <access_token>
```

### 2.2 更新用户信息

```
PUT /users/me
Authorization: Bearer <access_token>
```

---

## 三、任务模块 `/tasks`

### 3.1 获取任务列表

```
GET /tasks
Authorization: Bearer <access_token>
```

**查询参数:**

| 参数 | 类型 | 说明 |
|------|------|------|
| skip | int | 偏移量，默认 0 |
| limit | int | 每页数量，默认 20 |
| status | string | 筛选状态: pending/in_progress/completed/cancelled |
| priority | string | 筛选优先级: low/medium/high/urgent |
| project_id | int | 筛选所属项目 |
| tag_id | int | 筛选标签 |
| search | string | 搜索关键词 |

**响应示例:**

```json
{
  "items": [
    {
      "id": 1,
      "title": "完成项目报告",
      "description": "整理Q2季度项目进展报告",
      "status": "pending",
      "priority": "high",
      "due_date": "2026-05-20T00:00:00",
      "project_id": 1,
      "creator_id": 1,
      "created_at": "2026-05-16T10:00:00",
      "updated_at": "2026-05-16T10:00:00"
    }
  ],
  "total": 1
}
```

### 3.2 创建任务

```
POST /tasks
Authorization: Bearer <access_token>
```

**请求体:**

```json
{
  "title": "完成项目报告",
  "description": "整理Q2季度项目进展报告",
  "priority": "high",
  "due_date": "2026-05-20T00:00:00",
  "project_id": 1,
  "tag_ids": [1, 2]
}
```

### 3.3 获取任务详情

```
GET /tasks/{task_id}
Authorization: Bearer <access_token>
```

### 3.4 更新任务

```
PUT /tasks/{task_id}
Authorization: Bearer <access_token>
```

### 3.5 删除任务

```
DELETE /tasks/{task_id}
Authorization: Bearer <access_token>
```

### 3.6 更新任务状态

```
PUT /tasks/{task_id}/status
Authorization: Bearer <access_token>
```

**请求体:**

```json
{
  "status": "completed"
}
```

**状态枚举:** `pending` → `in_progress` → `completed` / `cancelled`

---

## 四、项目模块 `/projects`

| 接口 | 方法 | 说明 |
|------|------|------|
| `/projects` | GET | 获取项目列表 |
| `/projects` | POST | 创建项目 |
| `/projects/{id}` | GET | 获取项目详情 |
| `/projects/{id}` | PUT | 更新项目 |
| `/projects/{id}` | DELETE | 删除项目 |

**项目对象:**

```json
{
  "id": 1,
  "name": "Q2项目",
  "description": "第二季度重点推进项目",
  "color": "#4A90D9",
  "created_at": "2026-05-16T10:00:00"
}
```

---

## 五、标签模块 `/tags`

| 接口 | 方法 | 说明 |
|------|------|------|
| `/tags` | GET | 获取标签列表 |
| `/tags` | POST | 创建标签 |
| `/tags/{id}` | PUT | 更新标签 |
| `/tags/{id}` | DELETE | 删除标签 |

**标签对象:**

```json
{
  "id": 1,
  "name": "紧急",
  "color": "#E74C3C",
  "user_id": 1
}
```

---

## 六、习惯模块 `/habits`

| 接口 | 方法 | 说明 |
|------|------|------|
| `/habits` | GET | 获取习惯列表 |
| `/habits` | POST | 创建习惯 |
| `/habits/{id}` | PUT | 更新习惯 |
| `/habits/{id}` | DELETE | 删除习惯 |
| `/habits/{id}/check-in` | POST | 习惯打卡 |
| `/habits/{id}/logs` | GET | 获取打卡记录 |

**习惯对象:**

```json
{
  "id": 1,
  "name": "每日阅读",
  "frequency": "daily",
  "description": "每天阅读30分钟",
  "user_id": 1
}
```

---

## 七、统计与通知 `/stats` `/notifications`

| 接口 | 方法 | 说明 |
|------|------|------|
| `/stats/overview` | GET | 获取统计概览 |
| `/stats/habits` | GET | 获取习惯统计 |
| `/notifications` | GET | 获取通知列表 |
| `/notifications/{id}/read` | PUT | 标记通知已读 |

---

## 八、通用响应格式

### 成功响应

```json
{
  "data": {},
  "message": "success"
}
```

### 错误响应

```json
{
  "code": 1001,
  "message": "认证失败：令牌无效或已过期",
  "detail": null
}
```

### 错误码范围

| 范围 | 类别 |
|------|------|
| 1000-1999 | 认证错误 |
| 2000-2999 | 参数错误 |
| 3000-3999 | 用户错误 |
| 4000-4999 | 任务错误 |
| 5000-5999 | 项目错误 |
| 6000-6999 | 标签错误 |
| 7000-7999 | 习惯错误 |
| 8000-8999 | AI 错误 |
