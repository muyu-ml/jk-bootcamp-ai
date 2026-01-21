# 实施计划：数据库查询工具核心功能

**日期：** 2026-01-20  
**作者：** 系统生成  
**状态：** 草案

---

## 章程检查

继续之前，验证与项目章程（v1.0.0）的一致性：

- [ ] **原则 1：** 代码遵循 Ergonomic Python 和严格 TypeScript 模式
- [ ] **原则 2：** 所有函数都有全面的类型标注
- [ ] **原则 3：** 后端模型仅使用 Pydantic
- [ ] **原则 4：** API 响应使用 camelCase JSON 格式
- [ ] **原则 5：** 未引入身份验证机制
- [ ] **原则 6：** CORS 保持宽松（所有来源）
- [ ] **原则 7：** SQL 查询经过验证和限制
- [ ] **原则 8：** 元数据适当地缓存在 SQLite 中
- [ ] **原则 9：** 所有响应都是结构化 JSON

---

## 概述

### 功能摘要

构建一个完整的数据库查询工具，支持 PostgreSQL 连接管理、元数据提取与缓存、SQL 查询验证与执行、自然语言转 SQL、查询结果展示、以及数据库结构浏览。

### 业务价值

- **开发者效率：** 无需安装笨重的数据库客户端工具，快速执行查询和探索数据
- **降低门槛：** 通过自然语言生成 SQL，非专业人员也能查询数据
- **安全性：** 强制 SELECT-only 策略，防止意外的数据修改
- **性能：** 元数据缓存减少数据库负载，加快响应速度

### 依赖项

**外部服务：**
- PostgreSQL 数据库（测试和生产环境）
- OpenAI API（自然语言转 SQL 功能）

**技术栈：**
- 后端：Python 3.10+, uv, FastAPI, SQLglot, Pydantic, SQLite, OpenAI SDK
- 前端：Node.js 18+, React 18, TypeScript 5, Refine 5, Ant Design 5, Monaco Editor, Tailwind CSS

---

## 技术方法

### 架构

**整体架构：**

```
┌─────────────┐
│   Browser   │
│  (React UI) │
└──────┬──────┘
       │ HTTP/JSON (camelCase)
       ▼
┌─────────────────────┐
│  FastAPI Backend    │
│  ┌───────────────┐  │
│  │ API Layer     │  │  ← CORS, Pydantic validation
│  ├───────────────┤  │
│  │ Business      │  │  ← SQL validation (sqlglot)
│  │ Logic         │  │  ← LLM integration (OpenAI)
│  ├───────────────┤  │
│  │ Data Layer    │  │  ← SQLite (metadata cache)
│  │               │  │  ← PostgreSQL (query execution)
│  └───────────────┘  │
└─────────────────────┘
```

**数据流：**

1. **连接管理流程：**
   - 用户输入连接字符串 → FastAPI 验证 → 测试连接 → 保存到 SQLite → 触发元数据提取

2. **元数据提取流程：**
   - 查询 PostgreSQL 系统目录 → 获取表/视图/列信息 → （可选）LLM 格式化 → 存储到 SQLite

3. **SQL 查询流程：**
   - 用户输入 SQL → sqlglot 解析验证 → 检查 SELECT-only → 注入 LIMIT → 执行查询 → 返回 JSON 结果

4. **自然语言流程：**
   - 用户输入自然语言 → 获取元数据上下文 → 调用 OpenAI API → 生成 SQL → 返回给前端

### 关键设计决策

#### 决策 1：使用 SQLite 缓存元数据

**理由：**
- 减少对目标数据库的查询压力
- 支持离线浏览数据库结构
- 加快元数据加载速度（< 100ms）

**考虑的替代方案：**
- 内存缓存（Redis）：增加部署复杂度，对单用户工具过度设计
- 每次实时查询：网络延迟高，用户体验差

**章程一致性：** 
- 原则 8（元数据适当地缓存在 SQLite 中）

#### 决策 2：使用 sqlglot 进行 SQL 验证

**理由：**
- 纯 Python 实现，无需额外二进制依赖
- 支持多种 SQL 方言（PostgreSQL、MySQL 等）
- 能够解析 AST 并修改查询（注入 LIMIT）

**考虑的替代方案：**
- 正则表达式：不可靠，无法处理复杂嵌套查询
- PostgreSQL EXPLAIN：需要数据库往返，延迟高

**章程一致性：**
- 原则 7（SQL 查询经过验证和限制）

#### 决策 3：Monaco Editor 作为 SQL 编辑器

**理由：**
- VS Code 同款编辑器，用户体验好
- 内置语法高亮、自动补全、括号匹配
- 支持自定义语言服务（未来可集成表名/列名补全）

**考虑的替代方案：**
- CodeMirror：功能类似，但 Monaco 社区更活跃
- Textarea + highlight.js：功能太基础，不适合复杂查询

**章程一致性：**
- 原则 2（前端使用 TypeScript 严格类型）

#### 决策 4：Refine 5 + Ant Design 作为前端框架

**理由：**
- Refine 提供开箱即用的 CRUD 模式
- Ant Design 组件库完善（Table、Tree、Modal 等）
- 与 TypeScript 集成良好

**考虑的替代方案：**
- Material-UI：设计风格不符合数据工具定位
- 纯 React：需要从零搭建表单、表格等组件，工作量大

**章程一致性：**
- 原则 1（严格的 TypeScript）、原则 2（全面的类型标注）

---

## 实施阶段

### 阶段 1：项目脚手架与基础设施（2 天）

**目标：** 搭建开发环境，配置工具链，创建项目骨架

**任务：**
- [ ] 初始化后端项目（uv、FastAPI、pyproject.toml）
- [ ] 配置 mypy、ruff、pytest
- [ ] 初始化前端项目（Vite + React + TypeScript）
- [ ] 配置 ESLint、Prettier、TypeScript strict mode
- [ ] 创建 SQLite 数据库模式（connections、tables、columns）
- [ ] 编写数据库迁移脚本或初始化脚本
- [ ] 配置 CORS 中间件（allow all origins）
- [ ] 创建基础 Pydantic 配置（camelCase alias generator）
- [ ] 搭建 Docker Compose（PostgreSQL 测试数据库 + 后端 + 前端）

**成功标准：**
- 后端启动成功（uvicorn 运行无错误）
- 前端启动成功（Vite dev server 运行无错误）
- mypy 和 TypeScript 编译通过（0 errors）
- SQLite 数据库初始化成功

**预估工作量：** 16 小时

---

### 阶段 2：数据库连接管理（2-3 天）

**目标：** 实现连接添加、列表、删除功能

**任务：**
- [ ] 定义 Pydantic 模型（ConnectionCreate、ConnectionResponse）
- [ ] 实现 POST /api/connections（添加连接）
- [ ] 实现连接字符串验证和测试连接逻辑
- [ ] 实现 GET /api/connections（列表）
- [ ] 实现 DELETE /api/connections/{id}（删除）
- [ ] 编写单元测试（Pydantic 验证、数据库 CRUD）
- [ ] 编写集成测试（API 端点）
- [ ] 创建前端连接表单（React + Ant Design Form）
- [ ] 创建连接列表页面（Refine ListPage + Ant Design Table）
- [ ] 实现前端 API 调用（axios 或 fetch）
- [ ] 定义 TypeScript 接口（Connection, ConnectionFormData）
- [ ] 密码隐藏显示逻辑（前端显示 ****）

**成功标准：**
- 用户可以添加有效的 PostgreSQL 连接
- 无效连接返回明确错误消息
- 连接列表正确显示，密码已隐藏
- 删除连接成功并更新列表

**预估工作量：** 20 小时

---

### 阶段 3：元数据提取与缓存（3-4 天）

**目标：** 实现元数据提取、存储、刷新功能

**任务：**
- [ ] 定义 Pydantic 模型（TableMetadata、ColumnMetadata）
- [ ] 编写 PostgreSQL 元数据查询逻辑（information_schema）
- [ ] 实现元数据存储到 SQLite（表、列、类型、约束）
- [ ] 实现 POST /api/connections/{id}/refresh（刷新元数据）
- [ ] 实现 GET /api/connections/{id}/metadata（获取缓存的元数据）
- [ ] 编写单元测试（元数据解析、存储）
- [ ] 编写集成测试（完整提取流程）
- [ ] 创建前端侧边栏树形组件（Ant Design Tree）
- [ ] 实现树形节点展开/折叠
- [ ] 实现点击表名/列名插入到编辑器
- [ ] 加载状态和错误处理
- [ ] （可选）集成 OpenAI API 格式化元数据为 JSON

**成功标准：**
- 连接成功后自动提取元数据
- 元数据正确存储到 SQLite
- 侧边栏显示完整的数据库结构
- 刷新功能正常工作

**预估工作量：** 28 小时

---

### 阶段 4：SQL 查询验证与执行（3-4 天）

**目标：** 实现 SQL 编辑器、验证、执行、结果展示

**任务：**
- [ ] 集成 Monaco Editor 到 React 组件
- [ ] 配置 SQL 语法高亮和主题
- [ ] 定义 Pydantic 模型（QueryRequest、QueryResponse）
- [ ] 实现 sqlglot SQL 解析逻辑
- [ ] 实现 SELECT-only 验证（拒绝 INSERT/UPDATE/DELETE/DROP）
- [ ] 实现自动注入 LIMIT 1000 逻辑
- [ ] 实现 POST /api/queries/execute（执行查询）
- [ ] 实现查询超时控制（如 30 秒）
- [ ] 编写单元测试（SQL 验证、LIMIT 注入）
- [ ] 编写集成测试（查询执行流程）
- [ ] 创建查询结果表格组件（Ant Design Table）
- [ ] 实现列排序、横向滚动
- [ ] 显示执行时间和行数统计
- [ ] 错误消息展示（语法错误、执行错误）
- [ ] 空结果提示

**成功标准：**
- 有效的 SELECT 查询成功执行并返回结果
- 非 SELECT 语句被拒绝
- 无 LIMIT 的查询自动添加 LIMIT 1000
- 语法错误返回清晰的错误信息
- 查询结果以表格形式正确展示

**预估工作量：** 30 小时

---

### 阶段 5：自然语言转 SQL（LLM 集成）（2-3 天）

**目标：** 实现自然语言输入，生成 SQL 查询

**任务：**
- [ ] 配置 OpenAI API 客户端（环境变量管理）
- [ ] 定义 Pydantic 模型（NLQueryRequest、NLQueryResponse）
- [ ] 实现元数据上下文构建逻辑（表/列信息序列化为 prompt）
- [ ] 实现 POST /api/queries/generate（自然语言转 SQL）
- [ ] 编写 prompt 模板（包含元数据、用户意图、输出格式）
- [ ] 实现 LLM 调用和响应解析
- [ ] 编写单元测试（prompt 构建、响应解析）
- [ ] 编写集成测试（端到端 LLM 调用，使用 mock）
- [ ] 创建自然语言输入框和"生成 SQL"按钮
- [ ] 实现生成成功后自动填充到编辑器
- [ ] 实现加载状态（spinner）
- [ ] 错误处理（API 失败、配额超限、无法理解意图）

**成功标准：**
- 用户输入自然语言后成功生成 SQL
- 生成的 SQL 自动填充到编辑器
- LLM 调用失败时显示友好错误消息
- 元数据上下文正确传递给 LLM

**预估工作量：** 22 小时

---

### 阶段 6：UI 优化与集成测试（2 天）

**目标：** 完善用户体验，运行端到端测试

**任务：**
- [ ] 实现响应式布局（桌面和平板）
- [ ] 添加键盘快捷键（Ctrl+Enter 执行查询，Ctrl+K 清空编辑器）
- [ ] 优化加载状态和骨架屏
- [ ] 统一错误提示样式（Toast 或 Notification）
- [ ] 添加用户引导（首次使用提示）
- [ ] 编写 E2E 测试脚本（Playwright 或 Cypress）
  - 添加连接 → 浏览元数据 → 执行查询 → 查看结果
- [ ] 性能测试（元数据加载 < 100ms，SQL 验证 < 50ms）
- [ ] 可访问性测试（键盘导航、ARIA 标签）
- [ ] 浏览器兼容性测试（Chrome、Firefox、Safari）

**成功标准：**
- 所有功能流程端到端测试通过
- 性能指标满足 NFR2 要求
- 界面在不同屏幕尺寸下正常显示
- 无明显的可访问性问题

**预估工作量：** 16 小时

---

### 阶段 7：文档与部署（1-2 天）

**目标：** 编写文档，准备生产部署

**任务：**
- [ ] 编写 README.md（项目介绍、快速开始、功能说明）
- [ ] 编写 API 文档（利用 FastAPI 自动生成的 OpenAPI 文档）
- [ ] 编写开发者指南（环境搭建、代码规范、测试运行）
- [ ] 编写部署指南（Docker Compose、环境变量配置）
- [ ] 创建示例数据库和种子数据（用于演示）
- [ ] 配置生产环境（环境变量、日志、监控）
- [ ] 部署到测试环境并验证
- [ ] 记录已知问题和未来改进计划

**成功标准：**
- 新开发者可以根据文档在 30 分钟内启动项目
- API 文档完整且准确
- 生产环境部署成功并可访问

**预估工作量：** 12 小时

---

## 总工作量估算

| 阶段 | 预估工作量 | 累计工作量 |
|-----|----------|----------|
| 阶段 1：项目脚手架 | 16 小时 | 16 小时 |
| 阶段 2：连接管理 | 20 小时 | 36 小时 |
| 阶段 3：元数据提取 | 28 小时 | 64 小时 |
| 阶段 4：SQL 执行 | 30 小时 | 94 小时 |
| 阶段 5：LLM 集成 | 22 小时 | 116 小时 |
| 阶段 6：UI 优化 | 16 小时 | 132 小时 |
| 阶段 7：文档部署 | 12 小时 | 144 小时 |
| **总计** | **144 小时** | **约 18 工作日** |

**备注：** 按每天 8 小时计算，单人开发约需 3-4 周完成。实际时间可能因经验水平、技术难点、需求变更而有所调整。

---

## API 契约

### 1. 添加数据库连接

**端点：** `POST /api/connections`

**请求模式（Pydantic）：**

```python
class ConnectionCreate(BaseModel):
    name: str  # 连接名称（用户友好）
    connection_string: str  # PostgreSQL 连接字符串
    
    class Config:
        alias_generator = to_camel
        populate_by_name = True
```

**响应模式（Pydantic）：**

```python
class ConnectionResponse(BaseModel):
    id: int
    name: str
    host: str  # 从连接字符串解析
    database: str
    created_at: datetime
    
    class Config:
        alias_generator = to_camel
```

**错误响应：**
- `400 Bad Request`：连接字符串格式无效或无法连接
- `500 Internal Server Error`：服务器内部错误

---

### 2. 获取连接列表

**端点：** `GET /api/connections`

**响应模式：**

```python
class ConnectionListResponse(BaseModel):
    connections: List[ConnectionResponse]
    
    class Config:
        alias_generator = to_camel
```

---

### 3. 刷新元数据

**端点：** `POST /api/connections/{id}/refresh`

**响应模式：**

```python
class MetadataRefreshResponse(BaseModel):
    connection_id: int
    tables_count: int
    views_count: int
    refreshed_at: datetime
    
    class Config:
        alias_generator = to_camel
```

**错误响应：**
- `404 Not Found`：连接不存在
- `500 Internal Server Error`：元数据提取失败（权限不足、数据库错误）

---

### 4. 执行 SQL 查询

**端点：** `POST /api/queries/execute`

**请求模式：**

```python
class QueryRequest(BaseModel):
    connection_id: int
    sql: str  # 用户输入的 SQL
    
    class Config:
        alias_generator = to_camel
```

**响应模式：**

```python
class QueryResponse(BaseModel):
    columns: List[ColumnInfo]  # 列定义（name, type）
    rows: List[Dict[str, Any]]  # 数据行
    row_count: int
    execution_time_ms: int
    
    class Config:
        alias_generator = to_camel

class ColumnInfo(BaseModel):
    name: str
    type: str  # PostgreSQL 类型（如 VARCHAR, INTEGER）
```

**错误响应：**
- `400 Bad Request`：SQL 语法错误或非 SELECT 语句
- `404 Not Found`：连接不存在
- `500 Internal Server Error`：查询执行失败

---

### 5. 自然语言生成 SQL

**端点：** `POST /api/queries/generate`

**请求模式：**

```python
class NLQueryRequest(BaseModel):
    connection_id: int
    natural_language: str  # 用户输入的自然语言
    
    class Config:
        alias_generator = to_camel
```

**响应模式：**

```python
class NLQueryResponse(BaseModel):
    generated_sql: str
    explanation: str  # 可选：解释生成的 SQL
    
    class Config:
        alias_generator = to_camel
```

**错误响应：**
- `400 Bad Request`：无法理解用户意图
- `404 Not Found`：连接不存在
- `500 Internal Server Error`：LLM API 调用失败

---

## 数据库变更

### SQLite 模式

```sql
-- 连接表
CREATE TABLE IF NOT EXISTS connections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    connection_string TEXT NOT NULL,  -- 加密存储（可选）
    host TEXT NOT NULL,
    port INTEGER DEFAULT 5432,
    database TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 表和视图元数据
CREATE TABLE IF NOT EXISTS tables (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    connection_id INTEGER NOT NULL,
    schema_name TEXT DEFAULT 'public',
    table_name TEXT NOT NULL,
    table_type TEXT NOT NULL,  -- 'TABLE' or 'VIEW'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (connection_id) REFERENCES connections(id) ON DELETE CASCADE,
    UNIQUE(connection_id, schema_name, table_name)
);

-- 列元数据
CREATE TABLE IF NOT EXISTS columns (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    table_id INTEGER NOT NULL,
    column_name TEXT NOT NULL,
    data_type TEXT NOT NULL,
    is_nullable BOOLEAN DEFAULT TRUE,
    is_primary_key BOOLEAN DEFAULT FALSE,
    column_default TEXT,
    ordinal_position INTEGER,
    FOREIGN KEY (table_id) REFERENCES tables(id) ON DELETE CASCADE
);

-- 索引（加速查询）
CREATE INDEX idx_tables_connection_id ON tables(connection_id);
CREATE INDEX idx_columns_table_id ON columns(table_id);
```

**理由：** 
- 使用外键级联删除保持数据一致性
- 唯一约束防止重复元数据
- 索引加速元数据查询

---

## 测试策略

### 单元测试

**后端：**
- [ ] Pydantic 模型验证（有效和无效输入）
- [ ] 连接字符串解析逻辑
- [ ] sqlglot SQL 验证（SELECT-only、LIMIT 注入）
- [ ] 元数据提取和序列化
- [ ] LLM prompt 构建逻辑
- [ ] 数据库 CRUD 操作（使用内存 SQLite）

**前端：**
- [ ] React 组件渲染（快照测试）
- [ ] 用户交互处理器（点击、输入）
- [ ] API 调用逻辑（使用 MSW mock）
- [ ] TypeScript 类型定义准确性

**目标覆盖率：** 80%

---

### 集成测试

- [ ] 端到端 API 调用（请求 → 业务逻辑 → 数据库 → 响应）
- [ ] 数据库连接测试流程（添加 → 列表 → 删除）
- [ ] 元数据提取完整流程（连接 → 提取 → 存储 → 查询）
- [ ] SQL 查询执行流程（验证 → 执行 → 格式化响应）
- [ ] CORS 行为验证（跨域请求成功）

---

### 手动测试清单

- [ ] 添加有效和无效的数据库连接
- [ ] 浏览元数据树形结构
- [ ] 执行各种 SELECT 查询（简单、复杂、JOIN）
- [ ] 尝试执行非 SELECT 语句（验证拒绝）
- [ ] 自然语言生成 SQL
- [ ] UI 在 Chrome、Firefox、Safari 上显示正常
- [ ] API 返回 camelCase JSON
- [ ] TypeScript 和 mypy 类型检查通过
- [ ] 响应时间满足性能要求

---

## 风险评估

| 风险 | 可能性 | 影响 | 缓解措施 |
|-----|-------|------|---------|
| OpenAI API 配额超限或不可用 | 中 | 高 | 实现 LLM fallback 逻辑，使用本地模型（如 Ollama）作为备选 |
| sqlglot 无法解析某些复杂 SQL | 中 | 中 | 记录失败案例，更新 sqlglot 版本或手动处理边缘情况 |
| 大型数据库元数据提取慢 | 低 | 中 | 增量提取策略，只提取常用 schema，提供手动刷新按钮 |
| 查询结果过大导致前端卡顿 | 中 | 中 | 强制 LIMIT 1000，未来实现服务端分页 |
| PostgreSQL 连接字符串密码泄漏 | 低 | 高 | 加密存储连接字符串，日志脱敏，前端隐藏密码 |

---

## 发布计划

1. **开发：** 按阶段 1-7 顺序完成，每个阶段独立测试
2. **代码审查：** 每个阶段完成后进行 PR 审查，验证章程合规性
3. **测试：** 单元测试 + 集成测试 + E2E 测试 + 手动测试
4. **部署：** 
   - 测试环境部署（Docker Compose）
   - 功能验收测试（UAT）
   - 生产环境部署（Docker 或云平台）
5. **监控：** 
   - 观察 API 响应时间
   - 监控错误率和日志
   - 收集用户反馈

---

## 待解决问题

- [ ] **问：** 是否需要支持查询历史记录功能？  
  **答：** 当前版本不在范围内，v2.0 考虑

- [ ] **问：** 是否需要支持导出查询结果（CSV/Excel）？  
  **答：** 当前版本不在范围内，v2.0 考虑

- [ ] **问：** OpenAI API Key 如何管理（用户自己提供 or 系统统一配置）？  
  **答：** 系统统一配置（环境变量），未来可支持用户自定义

- [ ] **问：** 是否需要支持多个并发连接（同时查询多个数据库）？  
  **答：** 当前版本不支持，用户需手动切换连接

---

## 参考

- **章程：** `.specify/memory/constitution.md`
- **规格说明：** `.specify/specs/001-db-query-core/spec.md`
- **外部文档：**
  - FastAPI: https://fastapi.tiangolo.com/
  - sqlglot: https://github.com/tobymao/sqlglot
  - Monaco Editor: https://microsoft.github.io/monaco-editor/
  - Refine: https://refine.dev/
  - Ant Design: https://ant.design/
