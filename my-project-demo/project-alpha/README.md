# Project Alpha - Ticket 管理系统

一个基于标签的 Ticket 管理工具，使用 FastAPI 作为后端，React + TypeScript + Vite + Tailwind + Shadcn UI 作为前端。

## 项目结构

```
project-alpha/
├── backend/          # FastAPI 后端
├── frontend/         # React 前端
├── docker-compose.yml
├── README.md
└── .gitignore
```

## 快速开始

### 前置要求

- Python 3.9+
- Node.js 18+
- PostgreSQL 15+ (或使用 Docker)
- Docker 和 Docker Compose (可选)

### 启动数据库

使用 Docker Compose 启动 PostgreSQL:

```bash
docker-compose up -d postgres
```

### 启动后端

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

后端 API 文档: http://localhost:8000/docs

### 启动前端

```bash
cd frontend
npm install
npm run dev
```

前端应用: http://localhost:5173

## 测试

### 后端测试

```bash
cd backend
pytest                    # 运行所有测试
pytest -v                # 详细输出
pytest --cov=app         # 带覆盖率报告
pytest tests/test_api_tickets.py  # 运行特定测试文件
```

### 前端测试

```bash
cd frontend
npm test                  # 运行测试
npm run test:ui          # 使用 UI 界面
npm run test:coverage    # 带覆盖率报告
```

### E2E 测试

```bash
# 确保后端运行在 http://localhost:8000
./e2e_test.sh
```

## 开发状态

- [x] Phase 1: 项目初始化
- [x] Phase 2: 数据库设计与迁移
- [x] Phase 3: 后端开发
- [x] Phase 4: 前端开发
- [x] Phase 5: 测试
- [x] Phase 6: 集成与联调

## 技术栈

### 后端
- FastAPI
- SQLAlchemy
- Alembic
- PostgreSQL
- Pydantic

### 前端
- React
- TypeScript
- Vite
- Tailwind CSS
- Shadcn UI
- Zustand
- Axios

## 许可证

MIT
