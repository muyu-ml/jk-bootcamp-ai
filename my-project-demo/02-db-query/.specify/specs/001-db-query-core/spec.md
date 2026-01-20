# 功能规格说明：数据库查询工具核心功能

**版本：** 1.0.0  
**日期：** 2026-01-20  
**作者：** 系统生成  
**状态：** 草案

---

## 章程一致性

本规格说明遵循数据库查询工具项目章程（v1.0.0）。适用的关键原则：

- **原则 3：** 使用 Pydantic 定义所有数据模型（数据库连接、元数据、查询请求/响应）
- **原则 4：** API 响应使用 camelCase 格式，符合前端 TypeScript 约定
- **原则 7：** SQL 查询通过 sqlglot 解析验证，仅允许 SELECT 语句，自动注入 LIMIT
- **原则 8：** 数据库元数据缓存到 SQLite，支持复用和离线访问
- **原则 9：** 所有响应为结构化 JSON，前端展示为表格

---

## 概述

### 目的

构建一个数据库查询工具，允许用户通过数据库连接字符串连接到 PostgreSQL 数据库，自动获取并展示数据库的表和视图元数据，支持用户直接输入 SQL 查询或通过自然语言生成 SQL 查询并执行，将查询结果以表格形式展示。

### 用户故事

**作为** 数据分析师或开发者  
**我想要** 快速连接到数据库并执行查询  
**以便** 探索数据、验证数据质量、生成报告，而无需安装笨重的客户端工具

### 范围

**在范围内：**
- 添加和管理 PostgreSQL 数据库连接
- 自动提取并缓存数据库元数据（表、视图、列信息）
- 手动输入 SQL 查询并执行（仅 SELECT）
- 通过 LLM 将自然语言转换为 SQL 查询
- 以表格形式展示查询结果
- SQL 语法验证和安全检查
- 自动添加 LIMIT 限制防止大规模数据返回

**不在范围内：**
- 支持其他数据库（MySQL、MongoDB 等）- 未来版本考虑
- 数据修改操作（INSERT、UPDATE、DELETE、DROP）
- 用户认证和权限管理
- 查询历史记录和收藏功能 - 未来版本考虑
- 查询性能分析和优化建议 - 未来版本考虑
- 数据导出功能（CSV、Excel）- 未来版本考虑

---

## 功能需求

### FR1: 数据库连接管理

**优先级：** 必须有

**描述：**  
用户可以通过提供 PostgreSQL 连接字符串（如 `postgresql://user:password@host:port/dbname`）来添加数据库连接。系统验证连接有效性，成功后保存连接信息到本地 SQLite 数据库。

**验收标准：**
- [ ] 给定有效的 PostgreSQL 连接字符串，当用户提交连接请求，则系统成功连接并保存连接信息
- [ ] 给定无效的连接字符串，当用户提交请求，则返回明确的错误消息（如"无法连接：认证失败"）
- [ ] 给定已保存的连接，当用户查看连接列表，则显示连接名称、主机、数据库名称（密码已隐藏）
- [ ] 给定已保存的连接，当用户删除连接，则从 SQLite 中移除连接及其关联的元数据

**章程检查：**
- 与原则 3 一致：连接信息使用 Pydantic 模型定义，包含验证规则（URL 格式、必填字段）
- 与原则 8 一致：连接信息持久化到 SQLite 数据库

---

### FR2: 数据库元数据提取与缓存

**优先级：** 必须有

**描述：**  
成功连接数据库后，系统自动查询 PostgreSQL 系统目录（`information_schema` 或 `pg_catalog`），提取所有表和视图的元数据，包括表名、列名、数据类型、约束等信息。提取的元数据使用 LLM 转换为结构化 JSON 格式并存储到 SQLite，后续可复用而无需重复查询。

**验收标准：**
- [ ] 给定新建的数据库连接，当连接成功后，则系统自动触发元数据提取
- [ ] 给定 PostgreSQL 数据库包含 N 个表和 M 个视图，当元数据提取完成，则 SQLite 中存储 N+M 条表/视图记录及所有列信息
- [ ] 给定已缓存的元数据，当用户浏览数据库结构，则从 SQLite 读取数据而不查询目标数据库
- [ ] 给定用户主动触发刷新，当元数据刷新完成，则更新 SQLite 中的缓存数据
- [ ] 给定元数据提取失败（如权限不足），当提取过程出错，则记录错误信息并通知用户

**章程检查：**
- 与原则 8 一致：元数据持久化到 SQLite，支持离线访问和快速加载
- 与原则 3 一致：元数据结构使用 Pydantic 模型定义（Table、Column、View 等）

---

### FR3: SQL 查询验证与执行

**优先级：** 必须有

**描述：**  
用户在 SQL 编辑器（Monaco Editor）中输入查询语句，点击执行前，系统使用 sqlglot 解析并验证 SQL 语法。仅允许 SELECT 语句执行，拒绝任何修改数据的操作（INSERT、UPDATE、DELETE、DROP 等）。如果查询不包含 LIMIT 子句，自动注入 `LIMIT 1000` 以防止返回过多数据。

**验收标准：**
- [ ] 给定有效的 SELECT 查询，当用户执行查询，则返回查询结果（最多 1000 行）
- [ ] 给定 SELECT 查询不含 LIMIT，当系统解析查询，则自动追加 `LIMIT 1000`
- [ ] 给定 SELECT 查询已含 LIMIT N（N < 1000），当用户执行查询，则保持原 LIMIT 值
- [ ] 给定非 SELECT 语句（如 DELETE、DROP），当用户尝试执行，则拒绝执行并返回错误"仅允许 SELECT 查询"
- [ ] 给定语法错误的 SQL，当系统解析查询，则返回具体的语法错误信息（如"第 3 行：缺少 FROM 子句"）
- [ ] 给定查询执行超时或数据库错误，当执行失败，则返回友好的错误消息

**章程检查：**
- 与原则 7 一致：使用 sqlglot 解析和验证 SQL，强制 SELECT-only 策略，自动注入 LIMIT
- 与原则 9 一致：查询结果以结构化 JSON 返回（列定义 + 数据行）

---

### FR4: 自然语言转 SQL（LLM 集成）

**优先级：** 应该有

**描述：**  
用户可以用自然语言描述查询需求（如"查询销售额最高的 10 个产品"），系统将数据库的表和列元数据作为上下文传递给 LLM（OpenAI API），生成对应的 SQL 查询。生成的 SQL 自动填充到编辑器中，用户可以审查和修改后再执行。

**验收标准：**
- [ ] 给定用户输入自然语言查询，当点击"生成 SQL"按钮，则调用 LLM API 并返回 SQL 语句
- [ ] 给定数据库元数据已缓存，当调用 LLM，则将相关表和列信息作为 prompt 上下文
- [ ] 给定 LLM 返回的 SQL，当生成成功，则自动填充到 SQL 编辑器并高亮显示
- [ ] 给定 LLM 无法理解用户意图，当生成失败，则返回提示"无法生成查询，请尝试更具体的描述"
- [ ] 给定 LLM API 调用失败（如网络错误、配额超限），当出错，则显示错误消息

**章程检查：**
- 与原则 8 一致：利用缓存的元数据构建 LLM 上下文，减少延迟
- 与原则 3 一致：LLM 请求和响应使用 Pydantic 模型封装

---

### FR5: 查询结果展示

**优先级：** 必须有

**描述：**  
查询执行成功后，系统将结果以 JSON 格式返回给前端，前端使用 Ant Design 的 Table 组件展示为表格，支持列排序、分页（前端分页，初始显示全部数据）。表格显示列名、数据类型、每行数据，同时显示查询执行时间和返回行数。

**验收标准：**
- [ ] 给定查询返回 N 行数据，当结果加载，则表格显示所有 N 行（N ≤ 1000）
- [ ] 给定表格列数超过屏幕宽度，当表格渲染，则支持横向滚动
- [ ] 给定用户点击列标题，当触发排序，则按升序/降序重新排列数据
- [ ] 给定查询返回空结果，当执行完成，则显示"无数据"提示
- [ ] 给定查询执行时间和行数，当结果展示，则在表格上方显示"执行时间：120ms，返回 42 行"

**章程检查：**
- 与原则 4 一致：后端返回 camelCase 格式的 JSON（如 `columnName`, `rowData`）
- 与原则 9 一致：响应为结构化 JSON，包含列定义和数据行数组

---

### FR6: 数据库结构浏览

**优先级：** 应该有

**描述：**  
用户可以在侧边栏浏览当前连接数据库的所有表和视图，展开表节点查看列信息（列名、类型、是否可空、主键等）。点击表名或列名，可以快速插入到 SQL 编辑器中，减少手动输入。

**验收标准：**
- [ ] 给定数据库有多个表和视图，当用户选择连接，则侧边栏以树形结构展示所有对象
- [ ] 给定用户点击展开表节点，当展开，则显示该表的所有列及其数据类型
- [ ] 给定用户点击表名，当点击，则在编辑器光标位置插入表名
- [ ] 给定用户点击列名，当点击，则在编辑器光标位置插入 `表名.列名`
- [ ] 给定元数据尚未加载，当侧边栏显示，则显示加载状态（骨架屏或 spinner）

**章程检查：**
- 与原则 8 一致：从 SQLite 缓存读取元数据，快速渲染树形结构
- 与原则 2 一致：前端树形组件使用 TypeScript 严格类型定义

---

## 非功能需求

### NFR1: 类型安全

**需求：**  
所有 TypeScript 代码必须通过严格类型检查（`strict: true`）。所有 Python 代码必须通过 mypy 验证，函数签名包含完整类型标注。

**章程一致性：** 原则 1（Ergonomic Python & Strict TypeScript）、原则 2（全面的类型标注）

---

### NFR2: 性能

**需求：**  
- 元数据提取完成后，浏览数据库结构的响应时间 < 100ms（从 SQLite 读取）
- SQL 查询验证时间 < 50ms（sqlglot 解析）
- 查询结果返回时间取决于数据库性能，但 API 响应构建时间 < 200ms

**章程一致性：** 原则 8（在 SQLite 中缓存元数据，减少网络往返）

---

### NFR3: 安全

**需求：**  
- 所有 SQL 查询必须在执行前通过 sqlglot 解析。仅允许 SELECT 语句。
- 连接字符串中的密码在前端显示时必须隐藏（显示为 `****`）
- 后端不记录包含明文密码的日志

**章程一致性：** 原则 7（SQL 安全与查询限制）

---

### NFR4: 可用性

**需求：**  
- SQL 编辑器支持语法高亮、自动补全（表名、列名）、括号匹配
- 查询错误消息清晰具体，指出错误位置和原因
- 界面响应式设计，支持桌面和平板设备

**章程一致性：** 通用 UX 最佳实践

---

## 用户界面

### 线框图/原型

**布局结构：**

```
+----------------------------------------------------------+
|  [Logo] 数据库查询工具           [连接选择器 ▼] [+ 新连接] |
+----------------------------------------------------------+
| 侧边栏       |  主内容区域                                 |
| (元数据树)   |                                            |
|             |  [自然语言查询输入框]  [生成 SQL]            |
|  📁 public  |  +----------------------------------+       |
|    📄 users |  | SQL 编辑器 (Monaco)              |       |
|    📄 posts |  |                                  |       |
|  📁 auth    |  | SELECT * FROM users              |       |
|    📄 roles |  |                                  |       |
|             |  +----------------------------------+       |
|             |  [执行 (Ctrl+Enter)]  [清空]                |
|             |                                            |
|             |  执行时间: 120ms  |  返回: 42 行             |
|             |  +------------------------------------+    |
|             |  | id | name    | email       | ...  |    |
|             |  |----|---------|-------------|------|    |
|             |  | 1  | Alice   | a@ex.com    | ...  |    |
|             |  | 2  | Bob     | b@ex.com    | ...  |    |
|             |  +------------------------------------+    |
+----------------------------------------------------------+
```

### 用户流程

**流程 1：添加数据库连接并浏览元数据**

1. 用户点击"+ 新连接"按钮
2. 弹出对话框，输入连接字符串 `postgresql://user:pass@host:5432/mydb`
3. 点击"测试连接"，系统验证连接
4. 验证成功后，点击"保存"
5. 系统自动提取元数据（显示进度条）
6. 侧边栏展示数据库结构，用户可展开浏览表和列

**流程 2：执行 SQL 查询**

1. 用户在 SQL 编辑器输入 `SELECT * FROM users WHERE age > 25`
2. 点击"执行"按钮或按 `Ctrl+Enter`
3. 系统解析 SQL（自动添加 `LIMIT 1000` 如果缺失）
4. 执行查询并返回结果
5. 表格展示查询结果，显示执行时间和行数

**流程 3：使用自然语言生成 SQL**

1. 用户在自然语言输入框输入"查询年龄大于 25 岁的用户"
2. 点击"生成 SQL"按钮
3. 系统调用 LLM，传入数据库元数据作为上下文
4. LLM 返回生成的 SQL：`SELECT * FROM users WHERE age > 25`
5. SQL 自动填充到编辑器，用户可审查和修改
6. 用户点击"执行"运行查询

### 无障碍性

- [ ] 支持键盘导航（Tab 切换、Enter 执行、Esc 关闭对话框）
- [ ] 为屏幕阅读器提供 ARIA 标签（按钮、输入框、表格）
- [ ] 颜色对比度满足 WCAG 2.1 AA 标准
- [ ] 表格支持键盘导航（方向键移动焦点）

---

## API 契约

### 端点 1：添加数据库连接

**端点：** `POST /api/connections`

**请求体（camelCase）：**
```json
{
  "connectionString": "postgresql://user:password@localhost:5432/mydb",
  "displayName": "本地开发数据库"
}
```

**Pydantic 模型（内部 snake_case）：**
```python
from pydantic import BaseModel, Field, validator
from pydantic_core import to_camel

class ConnectionCreateRequest(BaseModel):
    connection_string: str = Field(..., min_length=1)
    display_name: str = Field(..., min_length=1, max_length=100)
    
    @validator('connection_string')
    def validate_postgres_url(cls, v):
        if not v.startswith('postgresql://'):
            raise ValueError('仅支持 PostgreSQL 连接')
        return v
    
    class Config:
        alias_generator = to_camel
        populate_by_name = True
```

**响应（200 OK）：**
```json
{
  "connectionId": "uuid-1234",
  "displayName": "本地开发数据库",
  "host": "localhost",
  "database": "mydb",
  "status": "connected",
  "metadataStatus": "extracting"
}
```

**错误响应：**
- `400 Bad Request`: 连接字符串格式无效
- `500 Internal Server Error`: 无法连接到数据库

---

### 端点 2：刷新元数据

**端点：** `POST /api/connections/{connectionId}/refresh`

**响应（200 OK）：**
```json
{
  "connectionId": "uuid-1234",
  "metadataStatus": "completed",
  "tablesCount": 15,
  "viewsCount": 3,
  "updatedAt": "2026-01-20T10:30:00Z"
}
```

---

### 端点 3：获取数据库元数据

**端点：** `GET /api/connections/{connectionId}/metadata`

**响应（200 OK）：**
```json
{
  "tables": [
    {
      "tableName": "users",
      "tableType": "table",
      "columns": [
        {
          "columnName": "id",
          "dataType": "integer",
          "isNullable": false,
          "isPrimaryKey": true
        },
        {
          "columnName": "name",
          "dataType": "varchar",
          "isNullable": false,
          "isPrimaryKey": false
        }
      ]
    }
  ],
  "views": [
    {
      "viewName": "active_users",
      "columns": [...]
    }
  ]
}
```

---

### 端点 4：执行 SQL 查询

**端点：** `POST /api/connections/{connectionId}/query`

**请求体（camelCase）：**
```json
{
  "sqlQuery": "SELECT * FROM users WHERE age > 25"
}
```

**Pydantic 模型：**
```python
class QueryExecuteRequest(BaseModel):
    sql_query: str = Field(..., min_length=1)
    
    class Config:
        alias_generator = to_camel
```

**响应（200 OK）：**
```json
{
  "columns": [
    {"name": "id", "type": "integer"},
    {"name": "name", "type": "varchar"},
    {"name": "age", "type": "integer"}
  ],
  "rows": [
    {"id": 1, "name": "Alice", "age": 30},
    {"id": 2, "name": "Bob", "age": 28}
  ],
  "rowCount": 2,
  "executionTimeMs": 120
}
```

**错误响应：**
- `400 Bad Request` (INVALID_SQL): SQL 语法错误
- `400 Bad Request` (FORBIDDEN_OPERATION): 非 SELECT 语句
- `500 Internal Server Error` (QUERY_EXECUTION_ERROR): 查询执行失败

---

### 端点 5：自然语言转 SQL

**端点：** `POST /api/connections/{connectionId}/nl2sql`

**请求体（camelCase）：**
```json
{
  "naturalLanguageQuery": "查询年龄大于 25 岁的用户"
}
```

**响应（200 OK）：**
```json
{
  "generatedSql": "SELECT * FROM users WHERE age > 25",
  "explanation": "查询 users 表中 age 字段大于 25 的所有记录"
}
```

---

## 数据模型

### SQLite 模式

**连接表：**
```sql
CREATE TABLE IF NOT EXISTS connections (
    id TEXT PRIMARY KEY,  -- UUID
    connection_string TEXT NOT NULL,
    display_name TEXT NOT NULL,
    host TEXT,
    port INTEGER,
    database_name TEXT,
    username TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**表元数据：**
```sql
CREATE TABLE IF NOT EXISTS tables (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    connection_id TEXT NOT NULL,
    table_name TEXT NOT NULL,
    table_type TEXT NOT NULL,  -- 'table' or 'view'
    row_count INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (connection_id) REFERENCES connections(id) ON DELETE CASCADE,
    UNIQUE(connection_id, table_name)
);
```

**列元数据：**
```sql
CREATE TABLE IF NOT EXISTS columns (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    table_id INTEGER NOT NULL,
    column_name TEXT NOT NULL,
    data_type TEXT NOT NULL,
    is_nullable BOOLEAN NOT NULL,
    is_primary_key BOOLEAN DEFAULT FALSE,
    column_default TEXT,
    ordinal_position INTEGER,
    FOREIGN KEY (table_id) REFERENCES tables(id) ON DELETE CASCADE
);
```

**理由：** 
- 使用 SQLite 作为本地缓存，轻量且无需额外服务
- 外键约束确保数据一致性（删除连接时级联删除元数据）
- `connection_string` 存储完整连接信息（包含密码），但前端展示时隐藏
- 元数据结构支持快速查询和 LLM 上下文构建

---

## 业务逻辑

### 验证规则

1. **规则：** SQL 查询必须仅包含 SELECT 语句
   - **实施：** 使用 sqlglot 解析 SQL，检查 AST 根节点类型是否为 `Select`
   - **错误处理：** 返回 400 错误，消息"仅允许 SELECT 查询，不允许修改数据的操作"

2. **规则：** SELECT 查询必须包含 LIMIT 子句（或自动注入）
   - **实施：** 解析 SQL AST，检查是否存在 LIMIT 节点，如无则追加 `LIMIT 1000`
   - **错误处理：** 无（自动修复）

3. **规则：** 连接字符串必须是有效的 PostgreSQL URL
   - **实施：** Pydantic validator 检查格式 `postgresql://...`，尝试连接测试
   - **错误处理：** 返回 400 错误，消息"连接字符串格式无效"或"无法连接到数据库：[详细错误]"

4. **规则：** 自然语言查询不能为空
   - **实施：** Pydantic 模型字段验证 `min_length=1`
   - **错误处理：** 返回 400 错误，消息"查询不能为空"

---

## 错误处理

| 错误场景 | HTTP 状态 | 错误代码 | 用户消息 |
| ------- | --------- | ------- | -------- |
| SQL 语法无效 | 400 | INVALID_SQL | "SQL 查询包含语法错误：[详情]" |
| 非 SELECT 语句 | 400 | FORBIDDEN_OPERATION | "仅允许 SELECT 查询，不允许修改数据的操作" |
| 数据库连接失败 | 500 | DB_CONNECTION_ERROR | "无法连接到数据库：[详情]" |
| 连接字符串格式无效 | 400 | INVALID_CONNECTION_STRING | "连接字符串格式无效，应为 postgresql://..." |
| 元数据提取失败 | 500 | METADATA_EXTRACTION_ERROR | "无法提取数据库元数据：[详情]" |
| 查询执行超时 | 500 | QUERY_TIMEOUT | "查询执行超时，请尝试优化查询或添加更严格的 LIMIT" |
| LLM API 调用失败 | 500 | LLM_API_ERROR | "无法生成 SQL 查询，请稍后重试" |
| 连接不存在 | 404 | CONNECTION_NOT_FOUND | "指定的数据库连接不存在" |

---

## 依赖项

### 后端依赖
- `fastapi>=0.104.0` - Web 框架
- `uvicorn>=0.24.0` - ASGI 服务器
- `sqlglot>=20.0.0` - SQL 解析和验证
- `pydantic>=2.0` - 数据验证和序列化
- `psycopg2-binary>=2.9.9` - PostgreSQL 驱动
- `openai>=1.0.0` - OpenAI API 客户端（用于自然语言转 SQL）
- `python-dotenv>=1.0.0` - 环境变量管理

### 前端依赖
- `react>=18.0.0`
- `typescript>=5.0.0`
- `@refinedev/core>=4.0.0` - Refine 框架核心
- `@refinedev/antd>=5.0.0` - Ant Design 集成
- `antd>=5.0.0` - UI 组件库
- `@monaco-editor/react>=4.6.0` - SQL 编辑器
- `tailwindcss>=3.0.0` - CSS 框架

### 开发依赖
- `mypy` - Python 类型检查
- `pytest` - Python 单元测试
- `ruff` 或 `black` - Python 代码格式化
- `vitest` - 前端单元测试
- `@testing-library/react` - React 组件测试

---

## 测试需求

### 单元测试（最低覆盖率：80%）

**后端：**
- [ ] Pydantic 模型验证
  - 有效的连接字符串格式
  - 无效的连接字符串（非 PostgreSQL）
  - SQL 查询字段验证（空字符串、超长字符串）
- [ ] SQL 解析逻辑
  - 有效的 SELECT 查询
  - 无效的语法
  - 非 SELECT 语句（INSERT、DELETE、DROP）
  - SELECT 查询自动注入 LIMIT
  - SELECT 查询已有 LIMIT 不重复注入
- [ ] 元数据提取逻辑（使用 mock PostgreSQL 连接）
  - 提取表列表
  - 提取列信息
  - 处理空数据库（无表）
  - 处理权限不足错误

**前端：**
- [ ] 连接管理组件
  - 添加连接表单验证
  - 连接列表渲染
  - 删除连接确认对话框
- [ ] SQL 编辑器组件
  - 语法高亮正常工作
  - 快捷键绑定（Ctrl+Enter 执行）
  - 插入表名/列名功能
- [ ] 结果表格组件
  - 数据正确渲染
  - 列排序功能
  - 空结果显示
- [ ] API 集成（mock 响应）
  - 查询执行成功
  - 查询执行失败（错误消息显示）
  - 自然语言转 SQL 成功

### 集成测试

- [ ] 端到端 API 调用
  - 添加连接 → 提取元数据 → 查看元数据
  - 执行 SQL 查询 → 返回结果
  - 自然语言转 SQL → 执行生成的 SQL
- [ ] 数据库操作（使用测试 SQLite 实例）
  - 保存连接信息
  - 缓存元数据
  - 查询缓存的元数据
- [ ] CORS 行为验证
  - 前端从不同端口调用后端 API
  - 验证 CORS 头正确设置

### 手动测试

- [ ] UI 在 Chrome、Firefox、Safari 上正确显示
- [ ] API 返回 camelCase JSON（使用浏览器开发者工具检查）
- [ ] 在编译时捕获类型错误（TypeScript 和 mypy 无错误）
- [ ] SQL 编辑器语法高亮和自动补全正常工作
- [ ] 表格横向滚动在窄屏幕上正常工作
- [ ] 自然语言转 SQL 生成合理的查询
- [ ] 错误消息清晰易懂

---

## 假设与约束

### 假设
1. 用户拥有 PostgreSQL 数据库的只读权限（至少可以查询 `information_schema`）
2. 用户环境可以访问互联网（调用 OpenAI API）
3. 用户了解基本的 SQL 语法
4. 数据库规模适中（表数 < 1000，单表行数 < 100 万）
5. 用户在受信任的网络环境中使用（无需认证）

### 约束
1. 仅支持 PostgreSQL（版本 >= 10）
2. 查询结果限制最多 1000 行
3. 不支持事务和多语句执行
4. 元数据刷新是手动触发，不自动同步
5. LLM 生成的 SQL 质量依赖于 OpenAI 模型能力

---

## 成功标准

本功能满足以下标准即视为成功：

1. **功能完整性**
   - 用户可以在 2 分钟内添加数据库连接并查看元数据
   - 95% 的有效 SQL 查询能成功执行并返回结果
   - 自然语言转 SQL 功能对简单查询（单表、常见条件）准确率 > 80%

2. **性能**
   - 元数据浏览响应时间 < 100ms（从缓存加载）
   - SQL 查询验证时间 < 50ms
   - 查询结果渲染时间 < 500ms（1000 行数据）

3. **安全性**
   - 100% 的非 SELECT 语句被阻止执行
   - 所有 SQL 查询通过 sqlglot 验证
   - 连接字符串密码在 UI 中隐藏

4. **用户体验**
   - 错误消息具体且可操作（指出问题和解决方案）
   - SQL 编辑器支持语法高亮和自动补全
   - 界面响应式，支持桌面和平板设备

5. **代码质量**
   - 后端和前端类型检查 100% 通过
   - 单元测试覆盖率 > 80%
   - 所有 API 端点有集成测试

---

## 待解决问题

- [ ] **问：** 如果用户的 PostgreSQL 数据库包含大量表（如 500+ 个），元数据提取和展示性能如何优化？  
  **答：** 待定 - 考虑分页加载或按 schema 分组，需要在实施阶段进行性能测试

- [ ] **问：** 自然语言转 SQL 功能是否需要支持多轮对话（用户可以修正查询意图）？  
  **答：** 不在当前范围，记录为未来增强功能

- [ ] **问：** 是否需要支持查询结果导出（CSV、JSON 文件）？  
  **答：** 不在当前范围，记录为未来增强功能

---

## 变更历史

| 版本 | 日期 | 作者 | 变更 |
| ---- | ---- | ---- | ---- |
| 1.0.0 | 2026-01-20 | 系统生成 | 初始规格说明，基于 Instructions.md 生成 |

---

## 参考

- 章程：`.specify/memory/constitution.md`
- 用户指引：`my-project-demo/specs/02-db-query/Instructions.md`
- 实施计划：待创建（`.specify/plans/001-db-query-core/plan.md`）
- 任务列表：待创建（`.specify/tasks/001-db-query-core/tasks.md`）
