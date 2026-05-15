# TodoMaster Pro - 部署指南

## 一、环境要求

| 依赖 | 版本要求 | 说明 |
|------|---------|------|
| Python | ≥ 3.11 | 后端运行环境 |
| Node.js | ≥ 18 | 前端构建 |
| Docker | ≥ 20.0 | 容器化部署 |
| Docker Compose | ≥ 2.0 | 服务编排 |
| 微信开发者工具 | 最新 | 小程序开发调试 |

## 二、本地开发部署

### 2.1 后端启动

```bash
# 进入后端目录
cd backend

# 创建虚拟环境（推荐）
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 启动开发服务器
uvicorn app.main:app --reload --host 0.0.0.0 --port 51200
```

启动后可访问：
- API 服务: `http://localhost:51200`
- API 文档 (Swagger): `http://localhost:51200/docs`
- 健康检查: `http://localhost:51200/health`

### 2.2 前端启动

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

启动后访问: `http://localhost:51212`

### 2.3 小程序启动

1. 打开微信开发者工具
2. 选择"导入项目"
3. 项目路径选择 `miniprogram/` 目录
4. 填入 AppID（测试可使用测试号）
5. 点击编译运行

> 注意：小程序需要后端服务运行在可访问的地址，修改 `miniprogram/app.js` 中的 `baseUrl` 为实际后端地址。

## 三、Docker 容器部署

### 3.1 使用 Docker Compose 一键部署

```bash
# 在项目根目录执行
docker-compose up -d
```

该命令将启动：
- **backend** 服务: FastAPI 后端 (内部端口 51200)
- **nginx** 服务: Nginx 反向代理 (对外端口 80)

### 3.2 服务访问

| 服务 | 地址 | 说明 |
|------|------|------|
| Nginx 入口 | `http://localhost:80` | 统一入口，代理 API 请求 |
| API 直连 | `http://localhost:51200` | 后端直连（开发调试用） |
| API 文档 | `http://localhost:80/docs` | Swagger 文档 |
| 健康检查 | `http://localhost:80/health` | 服务健康状态 |

### 3.3 常用 Docker 命令

```bash
# 查看运行状态
docker-compose ps

# 查看日志
docker-compose logs -f backend
docker-compose logs -f nginx

# 重启服务
docker-compose restart

# 停止服务
docker-compose down

# 停止并删除数据卷
docker-compose down -v

# 重新构建并启动
docker-compose up -d --build
```

### 3.4 环境变量配置

通过 `docker-compose.yml` 中的 `environment` 字段配置：

| 变量 | 默认值 | 说明 |
|------|--------|------|
| DATABASE_URL | `sqlite+aiosqlite:///./todomaster.db` | 数据库连接 |
| SECRET_KEY | `change-this-in-production-2026-todomaster` | JWT 签名密钥（生产环境务必修改） |

**生产环境建议** 使用 `.env` 文件管理环境变量：

```bash
# .env 文件示例
DATABASE_URL=postgresql+asyncpg://user:pass@db:5432/todomaster
SECRET_KEY=your-very-secure-random-secret-key
REDIS_URL=redis://redis:6379/0
```

## 四、Nginx 配置说明

当前 `nginx.conf` 配置了以下代理规则：

```
/api/        → http://backend:51200/api/      # API 接口
/health      → http://backend:51200/health     # 健康检查
/docs        → http://backend:51200/docs        # Swagger 文档
/openapi.json → http://backend:51200/openapi.json  # OpenAPI 规范
```

**生产环境建议** 增加：
- HTTPS 配置（SSL 证书）
- 前端静态文件托管
- 请求限流
- Gzip 压缩

## 五、数据库管理

### 5.1 开发环境

开发环境默认使用 SQLite，数据库文件自动创建在 `backend/todomaster.db`。

### 5.2 生产环境建议

推荐切换至 PostgreSQL：

1. 修改 `docker-compose.yml` 添加 PostgreSQL 服务
2. 修改环境变量 `DATABASE_URL` 为 PostgreSQL 连接串
3. 在 `requirements.txt` 中添加 `asyncpg` 和 `psycopg2-binary` 依赖

### 5.3 数据备份

```bash
# SQLite 备份
cp backend/todomaster.db backend/backup/todomaster_$(date +%Y%m%d).db

# PostgreSQL 备份
docker-compose exec db pg_dump -U user todomaster > backup.sql
```

## 六、生产环境检查清单

- [ ] 修改 `SECRET_KEY` 为随机安全密钥
- [ ] 切换数据库为 PostgreSQL
- [ ] 配置 HTTPS 证书
- [ ] 修改 Nginx 配置关闭 `server_tokens`
- [ ] 配置 CORS 允许的源（替换 `*`）
- [ ] 设置日志收集和监控
- [ ] 配置数据库定期备份
- [ ] 修改默认管理员密码
- [ ] 配置防火墙规则，仅开放必要端口
