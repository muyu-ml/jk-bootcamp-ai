# Project Alpha - Ticket 管理系统 设计文档

## 1. 数据模型设计

### 1.1 数据库架构

#### 1.1.1 Tickets 表

```sql
CREATE TABLE tickets (
    id BIGSERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP WITH TIME ZONE,
    CONSTRAINT check_status CHECK (status IN ('pending', 'completed'))
);

CREATE INDEX idx_tickets_status ON tickets(status);
CREATE INDEX idx_tickets_created_at ON tickets(created_at DESC);
CREATE INDEX idx_tickets_title ON tickets USING gin(to_tsvector('english', title));
```

**字段说明**:

- `id`: 主键，自增整数
- `title`: Ticket 标题，必填
- `description`: Ticket 描述，可选
- `status`: 状态，枚举值 ('pending', 'completed')
- `created_at`: 创建时间，自动设置
- `updated_at`: 更新时间，自动更新
- `completed_at`: 完成时间，仅在状态为 completed 时设置

#### 1.1.2 Tags 表

```sql
CREATE TABLE tags (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    color VARCHAR(7) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE UNIQUE INDEX idx_tags_name ON tags(name);
```

**字段说明**:

- `id`: 主键，自增整数
- `name`: 标签名称，唯一
- `color`: 标签颜色，十六进制格式 (#RRGGBB)
- `created_at`: 创建时间

#### 1.1.3 Ticket_Tags 关联表

```sql
CREATE TABLE ticket_tags (
    ticket_id INTEGER NOT NULL,
    tag_id INTEGER NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (ticket_id, tag_id),
    FOREIGN KEY (ticket_id) REFERENCES tickets(id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
);

CREATE INDEX idx_ticket_tags_ticket_id ON ticket_tags(ticket_id);
CREATE INDEX idx_ticket_tags_tag_id ON ticket_tags(tag_id);
```

**字段说明**:

- `ticket_id`: Ticket ID，外键
- `tag_id`: Tag ID，外键
- `created_at`: 关联创建时间
- 联合主键确保同一个 Ticket 不会重复添加同一个标签

### 1.2 数据库触发器

#### 1.2.1 自动更新 updated_at

```sql
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_tickets_updated_at
    BEFORE UPDATE ON tickets
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
```

#### 1.2.2 自动设置 completed_at

```sql
CREATE OR REPLACE FUNCTION set_completed_at()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.status = 'completed' AND OLD.status != 'completed' THEN
        NEW.completed_at = CURRENT_TIMESTAMP;
    ELSIF NEW.status = 'pending' AND OLD.status = 'completed' THEN
        NEW.completed_at = NULL;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_set_completed_at
    BEFORE UPDATE ON tickets
    FOR EACH ROW
    EXECUTE FUNCTION set_completed_at();
```

---

## 2. API 设计

### 2.1 API 约定

- **基础 URL**: `/api/v1`
- **响应格式**: JSON
- **状态码**:
  - 200: 成功
  - 201: 创建成功
  - 204: 删除成功（无内容）
  - 400: 请求参数错误
  - 404: 资源未找到
  - 500: 服务器错误

### 2.2 Ticket 端点

#### 2.2.1 获取所有 Tickets

```
GET /api/v1/tickets
```

**查询参数**:

- `status` (可选): 过滤状态 ('pending', 'completed', 'all')
- `tag_ids` (可选): 标签 ID 列表，逗号分隔
- `search` (可选): 搜索关键词
- `sort_by` (可选): 排序字段 ('created_at', 'updated_at', 'title')
- `order` (可选): 排序方向 ('asc', 'desc')
- `limit` (可选): 返回数量限制
- `offset` (可选): 偏移量（分页）

**响应示例**:

```json
{
  "tickets": [
    {
      "id": 1,
      "title": "实现用户登录功能",
      "description": "需要实现基于 JWT 的用户认证",
      "status": "pending",
      "tags": [
        {
          "id": 1,
          "name": "backend",
          "color": "#3B82F6"
        }
      ],
      "created_at": "2025-01-27T10:00:00Z",
      "updated_at": "2025-01-27T10:00:00Z",
      "completed_at": null
    }
  ],
  "total": 1,
  "limit": 50,
  "offset": 0
}
```

#### 2.2.2 获取单个 Ticket

```
GET /api/v1/tickets/{ticket_id}
```

**路径参数**:

- `ticket_id`: Ticket ID

**响应**: 单个 Ticket 对象

#### 2.2.3 创建 Ticket

```
POST /api/v1/tickets
```

**请求体**:

```json
{
  "title": "实现用户登录功能",
  "description": "需要实现基于 JWT 的用户认证",
  "tag_ids": [1, 2]
}
```

**响应**: 创建的 Ticket 对象（状态码 201）

#### 2.2.4 更新 Ticket

```
PUT /api/v1/tickets/{ticket_id}
```

**请求体**:

```json
{
  "title": "更新后的标题",
  "description": "更新后的描述"
}
```

**响应**: 更新后的 Ticket 对象

#### 2.2.5 删除 Ticket

```
DELETE /api/v1/tickets/{ticket_id}
```

**响应**: 状态码 204（无内容）

#### 2.2.6 完成 Ticket

```
PATCH /api/v1/tickets/{ticket_id}/complete
```

**响应**: 更新后的 Ticket 对象

#### 2.2.7 取消完成 Ticket

```
PATCH /api/v1/tickets/{ticket_id}/uncomplete
```

**响应**: 更新后的 Ticket 对象

### 2.3 标签端点

#### 2.3.1 获取所有标签

```
GET /api/v1/tags
```

**响应示例**:

```json
{
  "tags": [
    {
      "id": 1,
      "name": "backend",
      "color": "#3B82F6",
      "ticket_count": 5,
      "created_at": "2025-01-27T10:00:00Z"
    }
  ],
  "total": 1
}
```

#### 2.3.2 创建标签

```
POST /api/v1/tags
```

**请求体**:

```json
{
  "name": "frontend",
  "color": "#10B981"
}
```

**响应**: 创建的标签对象（状态码 201）

- 如果 color 未提供，自动生成随机颜色

#### 2.3.3 更新标签

```
PUT /api/v1/tags/{tag_id}
```

**请求体**:

```json
{
  "name": "updated-name",
  "color": "#EF4444"
}
```

**响应**: 更新后的标签对象

#### 2.3.4 删除标签

```
DELETE /api/v1/tags/{tag_id}
```

**响应**: 状态码 204

#### 2.3.5 添加标签到 Ticket

```
POST /api/v1/tickets/{ticket_id}/tags
```

**请求体**:

```json
{
  "tag_ids": [1, 2, 3]
}
```

**响应**: 更新后的 Ticket 对象

#### 2.3.6 从 Ticket 移除标签

```
DELETE /api/v1/tickets/{ticket_id}/tags/{tag_id}
```

**响应**: 状态码 204

---

## 3. 后端设计

### 3.1 项目结构

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI 应用入口
│   ├── config.py            # 配置文件
│   ├── database.py          # 数据库连接
│   ├── models/
│   │   ├── __init__.py
│   │   ├── ticket.py        # Ticket 模型
│   │   └── tag.py           # Tag 模型
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── ticket.py        # Ticket Pydantic 模型
│   │   └── tag.py           # Tag Pydantic 模型
│   ├── api/
│   │   ├── __init__.py
│   │   ├── tickets.py       # Ticket 路由
│   │   └── tags.py          # Tag 路由
│   ├── crud/
│   │   ├── __init__.py
│   │   ├── ticket.py        # Ticket CRUD 操作
│   │   └── tag.py           # Tag CRUD 操作
│   └── utils/
│       ├── __init__.py
│       └── color_generator.py  # 颜色生成工具
├── tests/
│   ├── __init__.py
│   ├── test_tickets.py
│   └── test_tags.py
├── alembic/                 # 数据库迁移
│   ├── versions/
│   └── env.py
├── alembic.ini
├── pyproject.toml
├── .env.example
└── README.md
```

### 3.2 核心模块设计

#### 3.2.1 SQLAlchemy 模型

**Ticket Model**:

```python
from sqlalchemy import Column, Integer, String, Text, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base
import enum

class TicketStatus(str, enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    status = Column(Enum(TicketStatus), default=TicketStatus.PENDING, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    completed_at = Column(DateTime(timezone=True))

    tags = relationship("Tag", secondary="ticket_tags", back_populates="tickets")
```

**Tag Model**:

```python
from sqlalchemy import Column, Integer, String, DateTime, Table, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base

ticket_tags = Table(
    'ticket_tags',
    Base.metadata,
    Column('ticket_id', Integer, ForeignKey('tickets.id', ondelete='CASCADE'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id', ondelete='CASCADE'), primary_key=True),
    Column('created_at', DateTime(timezone=True), server_default=func.now())
)

class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False, index=True)
    color = Column(String(7), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    tickets = relationship("Ticket", secondary=ticket_tags, back_populates="tags")
```

#### 3.2.2 Pydantic Schemas

**Ticket Schemas**:

```python
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from .tag import TagResponse

class TicketBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=10000)

class TicketCreate(TicketBase):
    tag_ids: Optional[List[int]] = []

class TicketUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=10000)

class TicketResponse(TicketBase):
    id: int
    status: str
    tags: List[TagResponse]
    created_at: datetime
    updated_at: Optional[datetime]
    completed_at: Optional[datetime]

    class Config:
        from_attributes = True
```

**Tag Schemas**:

```python
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class TagBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    color: Optional[str] = Field(None, pattern="^#[0-9A-Fa-f]{6}$")

class TagCreate(TagBase):
    pass

class TagUpdate(TagBase):
    pass

class TagResponse(TagBase):
    id: int
    created_at: datetime
    ticket_count: Optional[int] = 0

    class Config:
        from_attributes = True
```

---

## 4. 前端设计

### 4.1 页面结构

```
+----------------------------------------------------------+
|                        Header                             |
|  [Logo] [Search Bar]                    [New Ticket Btn] |
+----------------------------------------------------------+
|          |                                                 |
|  Sidebar |              Ticket List                       |
|          |                                                 |
|  Filters |  +------------------------------------------+  |
|          |  | Ticket Title              [Edit] [Delete]|  |
|  [ ] All |  | Description preview                      |  |
|  [ ] To  |  | [Tag1] [Tag2]                            |  |
|      Do  |  | Created: 2025-01-27                      |  |
|  [ ] Done|  +------------------------------------------+  |
|          |  +------------------------------------------+  |
|  Tags:   |  | Another Ticket            [Edit] [Delete]|  |
|  [Tag1]  |  | ...                                      |  |
|  [Tag2]  |  +------------------------------------------+  |
|          |                                                 |
+----------------------------------------------------------+
```

### 4.2 主要组件

#### 4.2.1 TicketList 组件

- **功能**: 展示 Ticket 列表
- **Props**:
  - `tickets`: Ticket 数组
  - `onEdit`: 编辑回调
  - `onDelete`: 删除回调
  - `onToggleComplete`: 完成状态切换回调
- **状态**:
  - 加载状态
  - 错误状态
  - 空状态

#### 4.2.2 TicketCard 组件

- **功能**: 单个 Ticket 的卡片展示
- **Props**:
  - `ticket`: Ticket 对象
  - `onEdit`: 编辑回调
  - `onDelete`: 删除回调
  - `onToggleComplete`: 完成状态切换回调
- **交互**:
  - 点击展开详情
  - 快速完成按钮

#### 4.2.3 TicketForm 组件

- **功能**: 创建/编辑 Ticket 的表单
- **模式**:
  - 创建模式：空表单
  - 编辑模式：预填充数据
- **字段**:
  - 标题输入框（必填）
  - 描述文本域（可选）
  - 标签选择器（多选）
- **验证**:
  - 实时验证
  - 错误提示
  - 提交前验证

#### 4.2.4 TagSelector 组件

- **功能**: 标签选择器
- **特性**:
  - 下拉多选
  - 搜索标签
  - 创建新标签（输入不存在的标签名）
  - 颜色预览
- **UI**: 使用 Shadcn 的 Combobox 或 Multi-Select 组件

#### 4.2.5 TagBadge 组件

- **功能**: 标签徽章展示
- **Props**:
  - `tag`: 标签对象
  - `removable`: 是否可移除
  - `onRemove`: 移除回调
- **样式**: 使用标签颜色作为背景

#### 4.2.6 SearchBar 组件

- **功能**: 搜索输入框
- **特性**:
  - 防抖处理（300ms）
  - 清除按钮
  - 搜索图标
  - 键盘快捷键（Ctrl/Cmd + K）

#### 4.2.7 FilterSidebar 组件

- **功能**: 过滤侧边栏
- **内容**:
  - 状态过滤器（全部/待完成/已完成）
  - 标签列表（带 Ticket 计数）
  - 清除所有过滤按钮
- **交互**:
  - 单选/多选标签
  - 实时更新列表

### 4.3 状态管理

使用 Zustand 或 Context API 进行状态管理：

```typescript
interface AppState {
  // Tickets
  tickets: Ticket[];
  isLoading: boolean;
  error: string | null;

  // Tags
  tags: Tag[];

  // Filters
  statusFilter: 'all' | 'pending' | 'completed';
  selectedTagIds: number[];
  searchQuery: string;

  // Actions
  fetchTickets: () => Promise<void>;
  createTicket: (data: CreateTicketData) => Promise<void>;
  updateTicket: (id: number, data: UpdateTicketData) => Promise<void>;
  deleteTicket: (id: number) => Promise<void>;
  toggleComplete: (id: number) => Promise<void>;

  fetchTags: () => Promise<void>;
  createTag: (data: CreateTagData) => Promise<void>;
  updateTag: (id: number, data: UpdateTagData) => Promise<void>;
  deleteTag: (id: number) => Promise<void>;
  addTagToTicket: (ticketId: number, tagIds: number[]) => Promise<void>;
  removeTagFromTicket: (ticketId: number, tagId: number) => Promise<void>;

  setStatusFilter: (status: 'all' | 'pending' | 'completed') => void;
  setSelectedTagIds: (ids: number[]) => void;
  setSearchQuery: (query: string) => void;
}
```

### 4.4 UI/UX 设计要点

#### 4.4.1 响应式设计

- **移动端**（< 768px）:
  - 隐藏侧边栏，使用抽屉式菜单
  - 堆叠布局
  - 简化卡片信息
- **平板**（768px - 1024px）:
  - 收缩侧边栏
  - 两列布局
- **桌面**（> 1024px）:
  - 完整侧边栏
  - 三列布局（可选）

#### 4.4.2 交互反馈

- **加载状态**: Skeleton 占位符
- **操作反馈**: Toast 通知（成功/失败）
- **动画**:
  - 列表项进入/退出动画
  - 完成状态过渡动画
  - 标签添加/移除动画
- **空状态**: 友好的空状态提示和插图

#### 4.4.3 键盘快捷键

- `Ctrl/Cmd + K`: 聚焦搜索框
- `N`: 创建新 Ticket
- `Esc`: 关闭对话框/清除搜索

#### 4.4.4 颜色方案

- **主色**: Tailwind 的 blue-600
- **成功**: green-600
- **警告**: yellow-500
- **错误**: red-600
- **灰度**: slate 系列
- **标签颜色**: 预定义调色板 + 随机生成

---

## 5. 项目结构

### 5.1 前端项目结构

```
frontend/
├── src/
│   ├── main.tsx          # 应用入口
│   ├── App.tsx           # 根组件
│   ├── components/       # React 组件
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
│   │   ├── ui/           # Shadcn UI 组件
│   │   └── common/
│   │       ├── SearchBar.tsx
│   │       └── ConfirmDialog.tsx
│   ├── lib/              # 工具函数
│   │   ├── api.ts        # API 客户端
│   │   └── utils.ts
│   ├── store/            # 状态管理
│   │   └── useTicketStore.ts
│   ├── types/            # TypeScript 类型定义
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
└── components.json       # Shadcn UI 配置
```

---

## 6. 技术选型说明

### 6.1 后端技术选型

- **FastAPI**: 现代、快速的 Python Web 框架，自动生成 API 文档
- **SQLAlchemy**: Python ORM，提供数据库抽象层
- **Pydantic**: 数据验证和序列化
- **Alembic**: 数据库迁移工具
- **PostgreSQL**: 强大的关系型数据库

### 6.2 前端技术选型

- **React**: 流行的 UI 库
- **TypeScript**: 类型安全
- **Vite**: 快速的构建工具
- **Tailwind CSS**: 实用优先的 CSS 框架
- **Shadcn UI**: 高质量的组件库
- **Zustand**: 轻量级状态管理
- **Axios**: HTTP 客户端

---

## 7. 安全考虑

### 7.1 输入验证

- 前后端都进行输入验证
- 防止 SQL 注入（使用 ORM）
- 防止 XSS 攻击（React 自动转义）

### 7.2 API 安全

- 设置合理的请求频率限制
- 验证请求来源（CORS）
- 使用 HTTPS（生产环境）

---

## 8. 性能优化

### 8.1 后端优化

- **数据库索引**: 在常用查询字段上创建索引
- **查询优化**: 使用 JOIN 避免 N+1 查询
- **连接池**: 配置合适的数据库连接池大小

### 8.2 前端优化

- **代码拆分**: 使用 Vite 的动态导入
- **懒加载**: 图片和组件懒加载
- **防抖节流**: 搜索和过滤使用防抖
- **缓存**: 使用 React Query 或 SWR 缓存 API 请求

---

**文档版本**: 1.0  
**创建日期**: 2025-01-27  
**状态**: 待实施
