# Project Alpha - Ticket 管理系统 实现计划

## 1. 项目概述

本文档详细描述了 Project Alpha Ticket 管理系统的实现步骤和计划。项目采用前后端分离架构，使用 FastAPI 作为后端，React + TypeScript + Vite + Tailwind + Shadcn UI 作为前端。

**预计开发周期**: 5-7 个工作日

---

## 2. 项目初始化阶段

### 2.1 项目结构搭建

#### 2.1.1 创建项目根目录结构

```
project-alpha/
├── backend/          # FastAPI 后端
├── frontend/         # React 前端
├── docker-compose.yml
├── README.md
└── .gitignore
```

#### 2.1.2 后端项目初始化

**步骤**:
1. 创建 `backend/` 目录
2. 初始化 Python 虚拟环境
3. 创建 `pyproject.toml` 或 `requirements.txt`
4. 安装核心依赖：
   - fastapi
   - uvicorn
   - sqlalchemy
   - psycopg2-binary
   - alembic
   - pydantic
   - python-dotenv

**命令**:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install fastapi uvicorn sqlalchemy psycopg2-binary alembic pydantic python-dotenv
```

#### 2.1.3 前端项目初始化

**步骤**:
1. 创建 `frontend/` 目录
2. 使用 Vite 创建 React + TypeScript 项目
3. 安装 Tailwind CSS
4. 初始化 Shadcn UI
5. 安装状态管理库（Zustand）和 HTTP 客户端（Axios）

**命令**:
```bash
cd frontend
npm create vite@latest . -- --template react-ts
npm install
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
npm install @radix-ui/react-*  # Shadcn UI 依赖
npm install zustand axios
npx shadcn-ui@latest init
```

---

## 3. 数据库设计与迁移阶段

### 3.1 PostgreSQL 数据库设置

**步骤**:
1. 安装并启动 PostgreSQL（或使用 Docker）
2. 创建数据库 `ticket_db`
3. 配置数据库连接信息

**Docker 方式**:
```yaml
# docker-compose.yml
version: '3.8'
services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: ticket_db
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

### 3.2 Alembic 迁移配置

**步骤**:
1. 初始化 Alembic
2. 配置 `alembic.ini` 和 `alembic/env.py`
3. 创建初始迁移脚本

**命令**:
```bash
cd backend
alembic init alembic
# 配置 alembic.ini 和 alembic/env.py
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

### 3.3 数据库表创建

**实现内容**:
1. 创建 `tickets` 表
2. 创建 `tags` 表
3. 创建 `ticket_tags` 关联表
4. 创建必要的索引
5. 创建数据库触发器（自动更新 `updated_at` 和 `completed_at`）

**迁移脚本位置**: `backend/alembic/versions/`

---

## 4. 后端开发阶段

### 4.1 项目结构搭建

**目录结构**:
```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI 应用入口
│   ├── config.py            # 配置管理
│   ├── database.py          # 数据库连接
│   ├── models/              # SQLAlchemy 模型
│   │   ├── __init__.py
│   │   ├── ticket.py
│   │   └── tag.py
│   ├── schemas/             # Pydantic 模型
│   │   ├── __init__.py
│   │   ├── ticket.py
│   │   └── tag.py
│   ├── api/                 # API 路由
│   │   ├── __init__.py
│   │   ├── tickets.py
│   │   └── tags.py
│   ├── crud/                # CRUD 操作
│   │   ├── __init__.py
│   │   ├── ticket.py
│   │   └── tag.py
│   └── utils/               # 工具函数
│       ├── __init__.py
│       └── color_generator.py
├── tests/                   # 测试文件
├── alembic/                 # 数据库迁移
├── .env.example
└── README.md
```

### 4.2 核心模块实现顺序

#### 阶段 4.2.1: 基础配置模块

**优先级**: P0（最高）

**实现内容**:
1. `app/config.py`: 环境变量配置
   - 数据库连接字符串
   - API 配置
   - CORS 设置
2. `app/database.py`: 数据库连接和会话管理
   - SQLAlchemy engine
   - SessionLocal
   - Base 类

**预计时间**: 0.5 天

#### 阶段 4.2.2: 数据模型层

**优先级**: P0

**实现内容**:
1. `app/models/tag.py`: Tag 模型
   - Tag 表定义
   - ticket_tags 关联表定义
2. `app/models/ticket.py`: Ticket 模型
   - Ticket 表定义
   - 状态枚举
   - 关系定义
3. `app/utils/color_generator.py`: 颜色生成工具
   - 随机颜色生成函数

**预计时间**: 0.5 天

#### 阶段 4.2.3: Schema 层

**优先级**: P0

**实现内容**:
1. `app/schemas/tag.py`:
   - TagBase
   - TagCreate
   - TagUpdate
   - TagResponse
2. `app/schemas/ticket.py`:
   - TicketBase
   - TicketCreate
   - TicketUpdate
   - TicketResponse

**预计时间**: 0.5 天

#### 阶段 4.2.4: CRUD 操作层

**优先级**: P0

**实现内容**:
1. `app/crud/tag.py`:
   - `create_tag()`
   - `get_tag()`
   - `get_tags()`
   - `update_tag()`
   - `delete_tag()`
   - `get_tag_ticket_count()`
2. `app/crud/ticket.py`:
   - `create_ticket()`
   - `get_ticket()`
   - `get_tickets()` (支持过滤、搜索、排序、分页)
   - `update_ticket()`
   - `delete_ticket()`
   - `complete_ticket()`
   - `uncomplete_ticket()`
   - `add_tags_to_ticket()`
   - `remove_tag_from_ticket()`

**预计时间**: 1.5 天

#### 阶段 4.2.5: API 路由层

**优先级**: P0

**实现内容**:
1. `app/api/tags.py`:
   - `GET /api/v1/tags` - 获取所有标签
   - `POST /api/v1/tags` - 创建标签
   - `PUT /api/v1/tags/{tag_id}` - 更新标签
   - `DELETE /api/v1/tags/{tag_id}` - 删除标签
2. `app/api/tickets.py`:
   - `GET /api/v1/tickets` - 获取所有 Tickets（支持查询参数）
   - `GET /api/v1/tickets/{ticket_id}` - 获取单个 Ticket
   - `POST /api/v1/tickets` - 创建 Ticket
   - `PUT /api/v1/tickets/{ticket_id}` - 更新 Ticket
   - `DELETE /api/v1/tickets/{ticket_id}` - 删除 Ticket
   - `PATCH /api/v1/tickets/{ticket_id}/complete` - 完成 Ticket
   - `PATCH /api/v1/tickets/{ticket_id}/uncomplete` - 取消完成 Ticket
   - `POST /api/v1/tickets/{ticket_id}/tags` - 添加标签到 Ticket
   - `DELETE /api/v1/tickets/{ticket_id}/tags/{tag_id}` - 从 Ticket 移除标签
3. `app/main.py`: FastAPI 应用入口
   - 注册路由
   - 配置 CORS
   - 配置中间件
   - 启动事件

**预计时间**: 1.5 天

#### 阶段 4.2.6: 错误处理和验证

**优先级**: P1

**实现内容**:
1. 自定义异常类
2. 全局异常处理器
3. 请求验证
4. 响应格式化

**预计时间**: 0.5 天

---

## 5. 前端开发阶段

### 5.1 项目结构搭建

**目录结构**:
```
frontend/
├── src/
│   ├── main.tsx              # 应用入口
│   ├── App.tsx               # 根组件
│   ├── components/           # React 组件
│   │   ├── tickets/
│   │   │   ├── TicketList.tsx
│   │   │   ├── TicketCard.tsx
│   │   │   └── TicketForm.tsx
│   │   ├── tags/
│   │   │   ├── TagSelector.tsx
│   │   │   └── TagBadge.tsx
│   │   ├── layout/
│   │   │   ├── Header.tsx
│   │   │   └── FilterSidebar.tsx
│   │   ├── ui/               # Shadcn UI 组件
│   │   └── common/
│   │       ├── SearchBar.tsx
│   │       └── ConfirmDialog.tsx
│   ├── lib/                  # 工具函数
│   │   ├── api.ts            # API 客户端
│   │   └── utils.ts
│   ├── store/                # 状态管理
│   │   └── useTicketStore.ts
│   ├── types/                # TypeScript 类型定义
│   │   ├── ticket.ts
│   │   └── tag.ts
│   └── styles/
│       └── globals.css
├── public/
├── index.html
├── package.json
├── tsconfig.json
├── vite.config.ts
├── tailwind.config.js
└── components.json
```

### 5.2 核心模块实现顺序

#### 阶段 5.2.1: 基础配置和类型定义

**优先级**: P0

**实现内容**:
1. 配置 Tailwind CSS
2. 初始化 Shadcn UI 组件
3. `src/types/ticket.ts`: Ticket 类型定义
4. `src/types/tag.ts`: Tag 类型定义
5. `src/lib/api.ts`: API 客户端封装
   - Axios 实例配置
   - API 请求函数（tickets 和 tags）

**预计时间**: 0.5 天

#### 阶段 5.2.2: 状态管理

**优先级**: P0

**实现内容**:
1. `src/store/useTicketStore.ts`: Zustand store
   - Tickets 状态
   - Tags 状态
   - 过滤状态（statusFilter, selectedTagIds, searchQuery）
   - Actions（fetchTickets, createTicket, updateTicket, deleteTicket, toggleComplete 等）
   - Tags Actions（fetchTags, createTag, updateTag, deleteTag 等）
   - Filter Actions（setStatusFilter, setSelectedTagIds, setSearchQuery）

**预计时间**: 1 天

#### 阶段 5.2.3: UI 基础组件

**优先级**: P0

**实现内容**:
1. 安装和配置 Shadcn UI 组件：
   - Button
   - Input
   - Dialog
   - AlertDialog
   - Badge
   - Card
   - Combobox
   - Checkbox
   - ScrollArea
   - Skeleton
   - Toast
2. `src/components/common/SearchBar.tsx`: 搜索栏组件
3. `src/components/common/ConfirmDialog.tsx`: 确认对话框组件

**预计时间**: 0.5 天

#### 阶段 5.2.4: 标签相关组件

**优先级**: P0

**实现内容**:
1. `src/components/tags/TagBadge.tsx`: 标签徽章组件
   - 显示标签名称和颜色
   - 可选的移除按钮
2. `src/components/tags/TagSelector.tsx`: 标签选择器组件
   - 多选下拉
   - 搜索功能
   - 创建新标签功能

**预计时间**: 1 天

#### 阶段 5.2.5: Ticket 相关组件

**优先级**: P0

**实现内容**:
1. `src/components/tickets/TicketCard.tsx`: Ticket 卡片组件
   - 显示 Ticket 信息
   - 编辑/删除按钮
   - 完成状态切换
   - 标签展示
2. `src/components/tickets/TicketList.tsx`: Ticket 列表组件
   - 列表渲染
   - 加载状态
   - 空状态
   - 错误处理
3. `src/components/tickets/TicketForm.tsx`: Ticket 表单组件
   - 创建/编辑模式
   - 表单验证
   - 标签选择集成

**预计时间**: 1.5 天

#### 阶段 5.2.6: 布局组件

**优先级**: P0

**实现内容**:
1. `src/components/layout/Header.tsx`: 顶部导航栏
   - Logo
   - 搜索栏
   - 新建 Ticket 按钮
2. `src/components/layout/FilterSidebar.tsx`: 过滤侧边栏
   - 状态过滤器（全部/待完成/已完成）
   - 标签列表（带计数）
   - 清除过滤按钮
   - 响应式设计（移动端抽屉式）

**预计时间**: 1 天

#### 阶段 5.2.7: 主应用集成

**优先级**: P0

**实现内容**:
1. `src/App.tsx`: 主应用组件
   - 布局结构
   - 路由集成（如需要）
   - 全局状态初始化
2. `src/main.tsx`: 应用入口
   - React 渲染
   - 全局样式导入
3. 响应式布局实现
4. 动画和过渡效果

**预计时间**: 1 天

#### 阶段 5.2.8: 交互优化

**优先级**: P1

**实现内容**:
1. 防抖处理（搜索）
2. 加载状态（Skeleton）
3. Toast 通知
4. 键盘快捷键
5. 空状态和错误状态优化

**预计时间**: 0.5 天

---

## 6. 测试阶段

### 6.1 后端测试

**优先级**: P1

**测试内容**:
1. 单元测试（CRUD 操作）
2. API 集成测试
3. 数据库操作测试

**测试框架**: pytest

**预计时间**: 1 天

### 6.2 前端测试

**优先级**: P2（可选）

**测试内容**:
1. 组件单元测试
2. 集成测试

**测试框架**: Vitest + React Testing Library

**预计时间**: 0.5 天

---

## 7. 集成与联调阶段

### 7.1 前后端联调

**步骤**:
1. 配置 CORS
2. 测试所有 API 端点
3. 验证数据流
4. 修复跨域问题
5. 错误处理验证

**预计时间**: 1 天

### 7.2 端到端测试

**步骤**:
1. 完整用户流程测试
2. 边界情况测试
3. 性能测试
4. 浏览器兼容性测试

**预计时间**: 0.5 天

---

## 8. 部署准备阶段

### 8.1 环境配置

**步骤**:
1. 创建 `.env.example` 文件
2. 配置生产环境变量
3. 数据库迁移脚本准备
4. Docker 配置优化

**预计时间**: 0.5 天

### 8.2 文档编写

**步骤**:
1. README.md（项目说明、安装步骤、运行指南）
2. API 文档（FastAPI 自动生成）
3. 开发文档

**预计时间**: 0.5 天

---

## 9. 开发时间表

| 阶段 | 任务 | 预计时间 | 优先级 |
|------|------|----------|--------|
| 1 | 项目初始化 | 0.5 天 | P0 |
| 2 | 数据库设计与迁移 | 1 天 | P0 |
| 3 | 后端开发 | 4.5 天 | P0 |
| 4 | 前端开发 | 6 天 | P0 |
| 5 | 测试 | 1 天 | P1 |
| 6 | 集成与联调 | 1.5 天 | P0 |
| 7 | 部署准备 | 1 天 | P1 |
| **总计** | | **15.5 天** | |

**注意**: 实际开发时间可能因个人经验和并行开发而有所不同。

---

## 10. 关键技术实现要点

### 10.1 后端关键点

1. **数据库触发器**: 使用 PostgreSQL 触发器自动更新 `updated_at` 和 `completed_at`
2. **全文搜索**: 使用 PostgreSQL 的 `to_tsvector` 实现标题搜索
3. **关联查询优化**: 使用 SQLAlchemy 的 `joinedload` 避免 N+1 查询
4. **分页实现**: 使用 `limit` 和 `offset` 实现分页
5. **颜色生成**: 实现随机颜色生成算法

### 10.2 前端关键点

1. **状态管理**: 使用 Zustand 管理全局状态
2. **防抖处理**: 搜索输入使用防抖（300ms）
3. **响应式设计**: 使用 Tailwind 的响应式类实现移动端适配
4. **组件复用**: 合理拆分组件，提高复用性
5. **错误处理**: 统一的错误处理和用户提示

---

## 11. 风险与应对

### 11.1 技术风险

| 风险 | 影响 | 应对措施 |
|------|------|----------|
| 数据库连接问题 | 高 | 使用连接池，添加重试机制 |
| CORS 配置错误 | 中 | 仔细配置 CORS，使用环境变量 |
| 性能问题 | 中 | 添加数据库索引，优化查询 |
| 状态管理复杂 | 低 | 使用成熟的 Zustand 库 |

### 11.2 进度风险

| 风险 | 影响 | 应对措施 |
|------|------|----------|
| 开发时间超期 | 中 | 优先实现核心功能，次要功能可延后 |
| 技术难点卡住 | 高 | 提前研究技术难点，寻求帮助 |

---

## 12. 验收标准

### 12.1 功能验收

- ✅ 可以创建、编辑、删除 Ticket
- ✅ 可以完成和取消完成 Ticket
- ✅ 可以创建、编辑、删除标签
- ✅ 可以为 Ticket 添加和移除标签
- ✅ 可以按标签过滤 Ticket 列表
- ✅ 可以按标题搜索 Ticket
- ✅ 可以按状态过滤 Ticket

### 12.2 质量验收

- ✅ 所有功能正常工作，无严重 Bug
- ✅ 前端界面美观，交互流畅
- ✅ API 响应正常，错误处理完善
- ✅ 代码结构清晰，注释完整
- ✅ 文档齐全（README、API 文档等）
- ✅ 响应式设计，移动端友好

---

## 13. 后续优化方向

1. **性能优化**:
   - 前端添加 React Query 缓存
   - 后端添加 Redis 缓存
   - 数据库查询优化

2. **功能扩展**:
   - 添加 Ticket 优先级
   - 添加截止日期
   - 添加批量操作
   - 添加导出功能

3. **用户体验**:
   - 添加拖拽排序
   - 添加键盘快捷键
   - 添加暗色模式

---

**文档版本**: 1.0  
**创建日期**: 2025-01-27  
**状态**: 待实施
