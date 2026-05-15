# TodoMaster Pro

智能待办管理全栈应用，支持 Web 端和微信小程序。

## 项目结构

```
todo-app/
├── backend/          # FastAPI 后端服务
├── frontend/         # Vue 3 前端应用
├── miniprogram/      # 微信小程序
├── docs/             # 项目文档
├── docker-compose.yml
└── nginx.conf
```

## 快速启动

### 1. 启动后端

```bash
cd backend

# 创建并激活虚拟环境（推荐）
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 启动服务（端口 51200）
uvicorn app.main:app --reload --port 51200
```

启动成功后可访问：
- API 服务：http://localhost:51200
- Swagger 文档：http://localhost:51200/docs
- 健康检查：http://localhost:51200/health

### 2. 启动前端

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器（端口 51212）
npm run dev
```

启动成功后访问：http://localhost:51212

### 3. 启动微信小程序

1. 使用微信开发者工具导入 `miniprogram/` 目录
2. 填入 AppID（测试可使用测试号）
3. 点击编译运行

> 小程序默认连接 `http://localhost:51200`，如需修改请编辑 `miniprogram/app.js` 中的 `baseUrl`。

### 4. Docker 一键部署

```bash
docker-compose up -d
```

## 端口说明

| 服务 | 端口 |
|------|------|
| 后端 API | 51200 |
| 前端开发服务器 | 51212 |
| Nginx（Docker 部署） | 80 |

## 技术栈

- **后端**：FastAPI + SQLAlchemy + SQLite (aiosqlite)
- **前端**：Vue 3 + Vite + Axios
- **小程序**：微信原生开发
- **部署**：Docker Compose + Nginx
