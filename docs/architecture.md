# TodoMaster Pro - 架构设计文档

## 一、整体架构

TodoMaster Pro 采用前后端分离架构，通过 RESTful API 通信，支持多客户端接入：

```
┌──────────────┐     ┌──────────────┐     ┌──────────────────┐
│  Web 前端     │────▶│   Nginx      │────▶│  FastAPI 后端     │
│  Vue3 + Vite │     │  反向代理     │     │  (端口 51200)     │
│  (端口 51212) │     │  (端口 80)    │     │                  │
└──────────────┘     └──────────────┘     └────────┬─────────┘
                                                   │
┌──────────────┐                                   │
│  微信小程序   │───────────────────────────────────▶│
│  原生开发     │         直连后端 API                │
└──────────────┘                                   │
                                                   ▼
                                          ┌────────────────┐
                                          │  SQLite 数据库  │
                                          │  (aiosqlite)    │
                                          └────────────────┘
```

## 二、后端架构

### 2.1 分层设计

```
┌─────────────────────────────────────┐
│          API 路由层 (api/v1/)         │  请求校验、路由分发
├─────────────────────────────────────┤
│          Schema 层 (schemas/)         │  请求/响应数据模型
├─────────────────────────────────────┤
│          服务层 (services/)           │  业务逻辑处理
├─────────────────────────────────────┤
│          模型层 (models/)             │  ORM 数据模型
├─────────────────────────────────────┤
│          数据库层 (database.py)        │  连接管理、会话工厂
└─────────────────────────────────────┘
```

### 2.2 核心模块

| 模块 | 路径 | 职责 |
|------|------|------|
| 应用入口 | `app/main.py` | FastAPI 实例创建、中间件注册、路由挂载、启动事件 |
| 配置管理 | `app/config.py` | Pydantic Settings，支持环境变量和 .env 文件 |
| 数据库 | `app/database.py` | 异步引擎、会话工厂、Base 声明、建表工具 |
| 依赖注入 | `app/dependencies.py` | 数据库会话等公共依赖 |
| 安全模块 | `app/core/security.py` | JWT 令牌生成/验证、密码哈希/校验 |
| 异常处理 | `app/core/exceptions.py` | 统一业务异常 AppException |
| 错误码 | `app/core/error_codes.py` | 错误码常量定义 |

### 2.3 API 版本控制

采用 URL 路径前缀 `/api/v1/` 实现版本控制，所有路由注册在 `api/v1/` 目录下：

```
/api/v1/auth/          → 认证相关
/api/v1/users/         → 用户管理
/api/v1/tasks/         → 任务管理
/api/v1/projects/      → 项目管理
/api/v1/tags/          → 标签管理
/api/v1/habits/        → 习惯管理
/api/v1/stats/         → 统计数据
/api/v1/notifications/ → 通知管理
```

### 2.4 认证流程

```
客户端                     后端
  │                        │
  │── POST /auth/login ──▶│  验证用户名密码
  │                        │  生成 access_token (30min)
  │◀── { access_token,   │  生成 refresh_token (7d)
  │      refresh_token }──│
  │                        │
  │── GET /tasks ─────────▶│  Authorization: Bearer <token>
  │                        │  验证 JWT 签名和过期时间
  │◀── { tasks } ─────────│
  │                        │
  │── POST /auth/refresh ─▶│  验证 refresh_token
  │◀── { access_token } ──│  签发新的 access_token
```

## 三、前端架构

### 3.1 技术选型

- **框架**: Vue 3 (Composition API)
- **构建工具**: Vite
- **HTTP 客户端**: Axios
- **日期处理**: lunar-javascript (农历支持)
- **工具库**: VueUse

### 3.2 组合式函数 (Composables)

| 函数 | 文件 | 职责 |
|------|------|------|
| `useAuth` | `composables/useAuth.js` | 认证状态管理、登录/注册/登出、Token 持久化 |
| `useTasks` | `composables/useTasks.js` | 任务 CRUD、状态更新、按日期筛选 |
| `useStats` | `composables/useStats.js` | 统计数据计算（完成率、优先级分布） |
| `useCalendar` | `composables/useCalendar.js` | 日历逻辑、农历转换、任务映射 |
| `useDragDrop` | `composables/useDragDrop.js` | 拖拽排序功能 |

### 3.3 组件结构

```
App.vue (根组件)
├── 登录/注册界面
└── 主界面
    ├── TaskCard       → 任务卡片
    ├── QuickAdd       → 快速添加
    ├── TodoForm       → 新建/编辑表单
    ├── CalendarView   → 日历视图
    ├── StatsPanel     → 统计面板
    └── PriorityBadge  → 优先级标签
```

## 四、小程序架构

### 4.1 页面结构

| 页面 | 路径 | 功能 |
|------|------|------|
| 首页 | `pages/index/` | 待办任务列表 |
| 创建任务 | `pages/task-create/` | 任务创建表单 |
| 任务详情 | `pages/task-detail/` | 任务详情与操作 |
| 看板 | `pages/kanban/` | 看板视图 |
| 日历 | `pages/calendar/` | 日历视图 |
| 专注 | `pages/focus/` | 番茄钟专注模式 |
| 项目 | `pages/project/` | 项目管理 |
| 习惯 | `pages/habit/` | 习惯追踪打卡 |
| 统计 | `pages/stats/` | 数据统计 |
| 搜索 | `pages/search/` | 全局搜索 |
| 通知 | `pages/notifications/` | 通知列表 |
| 设置 | `pages/settings/` | 应用设置 |
| 个人中心 | `pages/profile/` | 用户信息 |

### 4.2 服务层封装

```
services/
├── request.js    → wx.request 封装（统一鉴权、错误处理）
├── auth.js       → 认证 API
├── task.js       → 任务 API
├── project.js    → 项目 API
├── tag.js        → 标签 API
├── habit.js      → 习惯 API
└── stats.js      → 统计 API
```

## 五、部署架构

### 5.1 Docker Compose 编排

```yaml
services:
  backend:          # FastAPI 后端服务 (端口 51200)
  nginx:            # Nginx 反向代理 (端口 80)
```

### 5.2 Nginx 路由规则

| 路径 | 代理目标 | 说明 |
|------|---------|------|
| `/api/` | `http://backend:51200` | API 请求 |
| `/health` | `http://backend:51200` | 健康检查 |
| `/docs` | `http://backend:51200` | API 文档 |
| `/openapi.json` | `http://backend:51200` | OpenAPI 规范 |

## 六、数据库设计

### 6.1 核心表

| 表名 | 说明 | 关键字段 |
|------|------|---------|
| users | 用户 | id, nickname, hashed_password |
| tasks | 任务 | id, title, status, priority, due_date, project_id, creator_id |
| projects | 项目 | id, name, description, color |
| project_members | 项目成员 | user_id, project_id, role |
| tags | 标签 | id, name, color, user_id |
| task_tags | 任务-标签关联 | task_id, tag_id |
| subtasks | 子任务 | id, title, completed, task_id |
| comments | 评论 | id, content, task_id, user_id |
| reminders | 提醒 | id, remind_at, task_id |
| attachments | 附件 | id, filename, url, task_id |
| task_assignees | 任务指派 | task_id, user_id |
| habits | 习惯 | id, name, frequency, user_id |
| habit_logs | 习惯打卡记录 | id, habit_id, completed_at |
| notifications | 通知 | id, type, title, message, user_id |
| focus_sessions | 专注会话 | id, start_time, end_time, task_id, user_id |
| activity_logs | 活动日志 | id, action, user_id, task_id |
