# TodoMaster Pro - 项目概览

## 项目简介

TodoMaster Pro 是一款智能待办管理全栈应用，支持多端访问（Web 前端 + 微信小程序），提供任务管理、项目协作、习惯追踪、数据统计等核心功能，帮助用户高效管理日常待办与长期目标。

## 技术栈

| 层级 | 技术 | 说明 |
|------|------|------|
| 后端 | FastAPI + SQLAlchemy | Python 异步 Web 框架，异步 ORM |
| 数据库 | SQLite (aiosqlite) | 开发阶段使用 SQLite，可切换至 PostgreSQL |
| 认证 | JWT (HS256) | 基于 Token 的无状态认证 |
| Web 前端 | Vue 3 + Vite | 组合式 API，响应式架构 |
| 小程序 | 微信原生小程序 | 独立客户端 |
| 部署 | Docker Compose + Nginx | 容器化部署，Nginx 反向代理 |

## 端口配置

| 服务 | 端口 |
|------|------|
| 后端 API | 51200 |
| 前端开发服务器 | 51212 |
| Nginx | 80 |

## 项目结构

```
todo-app/
├── backend/                  # 后端服务
│   ├── app/
│   │   ├── main.py          # 应用入口
│   │   ├── config.py        # 配置管理
│   │   ├── database.py      # 数据库连接
│   │   ├── dependencies.py   # 依赖注入
│   │   ├── api/v1/          # API 路由层
│   │   ├── core/            # 核心模块（安全、异常、错误码）
│   │   ├── models/          # 数据模型层
│   │   ├── schemas/         # Pydantic Schema 层
│   │   ├── services/        # 业务逻辑层
│   │   └── utils/           # 工具函数
│   ├── tests/               # 测试用例
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/                 # Web 前端
│   ├── src/
│   │   ├── App.vue          # 根组件
│   │   ├── api/             # API 调用
│   │   ├── components/      # 组件
│   │   ├── composables/     # 组合式函数
│   │   └── assets/          # 静态资源
│   ├── vite.config.js
│   └── package.json
├── miniprogram/              # 微信小程序
│   ├── pages/               # 页面
│   ├── services/            # API 服务
│   └── utils/                # 工具函数
├── docs/                     # 项目文档
├── docker-compose.yml
├── nginx.conf
└── .gitignore
```

## 快速启动

### 本地开发

```bash
# 后端
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 51200

# 前端
cd frontend
npm install
npm run dev

# 小程序
使用微信开发者工具打开 miniprogram/ 目录
```

### Docker 部署

```bash
docker-compose up -d
```
