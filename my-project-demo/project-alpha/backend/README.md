# Project Alpha Backend

FastAPI 后端服务，提供 Ticket 管理系统的 RESTful API。

## 安装

1. 创建虚拟环境:
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

2. 安装依赖:
```bash
pip install -r requirements.txt
```

或者使用 pyproject.toml:
```bash
pip install -e .
```

## 配置

1. 复制 `env.example` 为 `.env`:
```bash
cd project-alpha/backend
cp env.example .env
```

2. 根据你的环境修改 `.env` 文件中的配置。

## 启动 PostgreSQL 数据库
在项目根目录（specs/my-w1/project-alpha/）运行：
```bash
docker-compose up -d
```
这会启动 PostgreSQL 容器。等待几秒后，可以验证：
```bash
docker-compose ps
```

## 数据库迁移

1. 初始化 Alembic (如果还没有):
```bash
alembic init alembic
```

2. 创建迁移:
```bash
alembic revision --autogenerate -m "Initial migration"
```

3. 应用迁移:
```bash
alembic upgrade head
```

## 运行

```bash
uvicorn app.main:app --reload
```

API 文档: http://localhost:8000/docs

## 测试

```bash
pytest
```
