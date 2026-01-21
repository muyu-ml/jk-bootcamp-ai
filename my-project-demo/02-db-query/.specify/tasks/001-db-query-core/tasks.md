# 任务列表：数据库查询工具核心功能

**特性编号：** 001-db-query-core  
**创建日期：** 2026-01-20  
**相关文档：**
- 规格说明：`.specify/specs/001-db-query-core/spec.md`
- 实施计划：`.specify/plans/001-db-query-core/plan.md`

---

## 任务组织说明

本任务列表按照3个阶段组织，每个阶段都是可独立测试的功能增量：

- **Phase 1：基础设施与核心后端** - 搭建项目骨架，实现连接管理和元数据提取
- **Phase 2：查询功能与前端** - 实现SQL查询执行和结果展示
- **Phase 3：增值功能与优化** - 添加LLM集成和UI优化

**标记说明：**
- `[P]` = 可并行执行的任务（不同文件，无依赖）
- 无 `[P]` = 需按顺序执行

**总工作量估算：** 约 144 小时（18 工作日）

---

## Phase 1: 基础设施与核心后端（FR1, FR2）

**目标：** 搭建开发环境，实现数据库连接管理和元数据提取功能

**成功标准：**
- 后端和前端项目可启动
- 用户可以添加、查看、删除数据库连接
- 元数据自动提取并缓存到 SQLite
- 类型检查通过（mypy, TypeScript）

---

### 1.1 项目初始化

- [ ] T001 初始化后端项目结构 `backend/` 使用 uv 和 FastAPI
- [ ] T002 创建 `backend/pyproject.toml` 定义依赖（fastapi, uvicorn, sqlglot, pydantic, psycopg2, openai, sqlalchemy）
- [ ] T003 配置 `backend/.python-version` 为 Python 3.10+
- [ ] T004 配置 mypy 严格模式在 `backend/pyproject.toml`
- [ ] T005 配置 ruff 格式化工具在 `backend/pyproject.toml`
- [ ] T006 配置 pytest 在 `backend/pytest.ini`
- [ ] T007 初始化前端项目 `frontend/` 使用 Vite + React + TypeScript
- [ ] T008 配置 TypeScript strict mode 在 `frontend/tsconfig.json`
- [ ] T009 安装前端依赖（react, @refinedev/core, @refinedev/antd, antd, @monaco-editor/react, tailwindcss）
- [ ] T010 配置 ESLint 和 Prettier 在 `frontend/`
- [ ] T011 创建 `docker-compose.yml` 包含 PostgreSQL 测试数据库

---

### 1.2 后端基础设施

- [ ] T012 创建 FastAPI 应用入口 `backend/app/main.py`
- [ ] T013 配置 CORS 中间件允许所有来源在 `backend/app/main.py`
- [ ] T014 创建 Pydantic 基础配置类在 `backend/app/core/config.py` 包含 camelCase alias generator
- [ ] T015 创建 SQLite 数据库初始化脚本 `backend/app/db/init_db.py`
- [ ] T016 定义 SQLite 模式在 `backend/app/db/schema.sql`（connections, tables, columns 表）
- [ ] T017 创建数据库连接工具 `backend/app/db/session.py` 用于 SQLite 操作
- [ ] T018 创建 PostgreSQL 连接测试工具 `backend/app/db/postgres.py`

---

### 1.3 数据库连接管理（FR1）

- [ ] T019 [P] 定义 Connection Pydantic 模型在 `backend/app/models/connection.py`
- [ ] T020 [P] 定义 ConnectionCreate 请求模型在 `backend/app/schemas/connection.py`
- [ ] T021 [P] 定义 ConnectionResponse 响应模型在 `backend/app/schemas/connection.py`
- [ ] T022 实现连接字符串解析工具在 `backend/app/utils/connection_parser.py`
- [ ] T023 实现 ConnectionService 在 `backend/app/services/connection_service.py`
  - 测试连接有效性
  - CRUD 操作（创建、读取、删除）
  - 密码加密存储（可选）
- [ ] T024 实现 POST /api/connections 端点在 `backend/app/api/endpoints/connections.py`
- [ ] T025 实现 GET /api/connections 端点在 `backend/app/api/endpoints/connections.py`
- [ ] T026 实现 DELETE /api/connections/{id} 端点在 `backend/app/api/endpoints/connections.py`
- [ ] T027 编写单元测试 `backend/tests/services/test_connection_service.py`
- [ ] T028 编写集成测试 `backend/tests/api/test_connections.py`

---

### 1.4 元数据提取与缓存（FR2）

- [ ] T029 [P] 定义 TableMetadata Pydantic 模型在 `backend/app/models/metadata.py`
- [ ] T030 [P] 定义 ColumnMetadata Pydantic 模型在 `backend/app/models/metadata.py`
- [ ] T031 [P] 定义 MetadataRefreshResponse 响应模型在 `backend/app/schemas/metadata.py`
- [ ] T032 实现 PostgreSQL 元数据提取器在 `backend/app/services/metadata_extractor.py`
  - 查询 information_schema.tables
  - 查询 information_schema.columns
  - 解析数据类型和约束
- [ ] T033 实现 MetadataService 在 `backend/app/services/metadata_service.py`
  - 存储元数据到 SQLite
  - 读取缓存的元数据
  - 刷新元数据
- [ ] T034 实现 POST /api/connections/{id}/refresh 端点在 `backend/app/api/endpoints/metadata.py`
- [ ] T035 实现 GET /api/connections/{id}/metadata 端点在 `backend/app/api/endpoints/metadata.py`
- [ ] T036 实现连接成功后自动触发元数据提取在 `backend/app/services/connection_service.py`
- [ ] T037 编写单元测试 `backend/tests/services/test_metadata_service.py`
- [ ] T038 编写集成测试 `backend/tests/api/test_metadata.py`

---

### 1.5 前端基础设施

- [ ] T039 创建前端入口 `frontend/src/main.tsx` 配置 Refine 和 Ant Design
- [ ] T040 创建 API 客户端 `frontend/src/api/client.ts` 使用 axios
- [ ] T041 定义 Connection TypeScript 接口在 `frontend/src/types/connection.ts`
- [ ] T042 定义 Metadata TypeScript 接口在 `frontend/src/types/metadata.ts`
- [ ] T043 创建主布局组件 `frontend/src/components/Layout.tsx`
- [ ] T044 创建连接表单组件 `frontend/src/components/ConnectionForm.tsx`
- [ ] T045 创建连接列表页面 `frontend/src/pages/ConnectionList.tsx`
- [ ] T046 实现连接添加、删除功能在连接列表页面
- [ ] T047 实现密码隐藏显示逻辑在连接列表
- [ ] T048 编写前端类型检查脚本 `frontend/package.json` (tsc --noEmit)

---

### Phase 1 验收测试

- [ ] T049 手动测试：添加有效的 PostgreSQL 连接
- [ ] T050 手动测试：添加无效连接并验证错误消息
- [ ] T051 手动测试：查看连接列表，密码已隐藏
- [ ] T052 手动测试：删除连接并验证从列表中移除
- [ ] T053 手动测试：触发元数据刷新并验证 SQLite 中的数据
- [ ] T054 验证后端 mypy 类型检查通过
- [ ] T055 验证前端 TypeScript 编译通过
- [ ] T056 验证 API 响应为 camelCase 格式

---

## Phase 2: 查询功能与前端（FR3, FR5, FR6）

**目标：** 实现 SQL 查询验证、执行、结果展示和数据库结构浏览

**成功标准：**
- 用户可以在 SQL 编辑器中输入和执行查询
- 仅允许 SELECT 语句，自动注入 LIMIT
- 查询结果以表格形式展示
- 侧边栏显示数据库结构树

---

### 2.1 SQL 查询验证（FR3）

- [ ] T057 [P] 定义 QueryRequest Pydantic 模型在 `backend/app/schemas/query.py`
- [ ] T058 [P] 定义 QueryResponse Pydantic 模型在 `backend/app/schemas/query.py`
- [ ] T059 [P] 定义 ColumnInfo Pydantic 模型在 `backend/app/schemas/query.py`
- [ ] T060 实现 SQL 解析器在 `backend/app/services/sql_validator.py`
  - 使用 sqlglot.parse_one() 解析 SQL
  - 验证仅为 SELECT 语句
  - 检查和注入 LIMIT 1000
- [ ] T061 实现 QueryService 在 `backend/app/services/query_service.py`
  - 验证 SQL
  - 执行查询（带超时控制）
  - 格式化结果为 JSON
- [ ] T062 实现 POST /api/queries/execute 端点在 `backend/app/api/endpoints/queries.py`
- [ ] T063 编写 SQL 验证单元测试 `backend/tests/services/test_sql_validator.py`
  - 测试 SELECT 语句通过
  - 测试 INSERT/UPDATE/DELETE 被拒绝
  - 测试自动注入 LIMIT
- [ ] T064 编写查询执行集成测试 `backend/tests/api/test_queries.py`

---

### 2.2 Monaco Editor 集成

- [ ] T065 创建 SQL 编辑器组件 `frontend/src/components/SqlEditor.tsx` 使用 @monaco-editor/react
- [ ] T066 配置 SQL 语法高亮和主题在 SqlEditor
- [ ] T067 实现"执行查询"按钮和快捷键（Ctrl+Enter）
- [ ] T068 实现"清空编辑器"功能
- [ ] T069 创建查询执行状态管理（loading, error, success）

---

### 2.3 查询结果展示（FR5）

- [ ] T070 [P] 定义 QueryResult TypeScript 接口在 `frontend/src/types/query.ts`
- [ ] T071 创建查询结果表格组件 `frontend/src/components/QueryResults.tsx` 使用 Ant Design Table
- [ ] T072 实现列排序功能
- [ ] T073 实现横向滚动（列数过多时）
- [ ] T074 实现空结果提示
- [ ] T075 显示执行时间和行数统计在表格上方
- [ ] T076 创建查询页面 `frontend/src/pages/QueryPage.tsx` 集成编辑器和结果表格

---

### 2.4 数据库结构浏览（FR6）

- [ ] T077 创建侧边栏组件 `frontend/src/components/Sidebar.tsx`
- [ ] T078 创建元数据树组件 `frontend/src/components/MetadataTree.tsx` 使用 Ant Design Tree
- [ ] T079 实现树形节点数据转换（从元数据到树形结构）
- [ ] T080 实现展开/折叠表节点查看列信息
- [ ] T081 实现点击表名插入到编辑器光标位置
- [ ] T082 实现点击列名插入 `表名.列名` 到编辑器
- [ ] T083 实现加载状态（骨架屏或 spinner）
- [ ] T084 实现元数据树与编辑器的交互逻辑

---

### 2.5 错误处理与用户体验

- [ ] T085 [P] 实现统一错误响应格式在 `backend/app/core/errors.py`
- [ ] T086 [P] 创建错误消息展示组件 `frontend/src/components/ErrorMessage.tsx`
- [ ] T087 实现 SQL 语法错误展示（高亮错误行）
- [ ] T088 实现查询超时处理和友好提示
- [ ] T089 实现网络错误处理和重试机制
- [ ] T090 添加用户操作确认对话框（删除连接等）

---

### Phase 2 验收测试

- [ ] T091 手动测试：执行有效的 SELECT 查询并验证结果
- [ ] T092 手动测试：执行不含 LIMIT 的查询，验证自动添加 LIMIT 1000
- [ ] T093 手动测试：尝试执行 DELETE 语句，验证被拒绝
- [ ] T094 手动测试：执行语法错误的 SQL，验证错误消息清晰
- [ ] T095 手动测试：查看查询结果表格，测试列排序和横向滚动
- [ ] T096 手动测试：浏览侧边栏数据库结构树
- [ ] T097 手动测试：点击表名/列名插入到编辑器
- [ ] T098 手动测试：测试空结果和错误场景的显示

---

## Phase 3: 增值功能与优化（FR4 + Polish）

**目标：** 添加自然语言转 SQL 功能，优化 UI，完善文档

**成功标准：**
- 用户可以通过自然语言生成 SQL
- 界面响应式且支持键盘快捷键
- 文档完整，便于部署

---

### 3.1 自然语言转 SQL（FR4）

- [ ] T099 [P] 定义 NLQueryRequest Pydantic 模型在 `backend/app/schemas/nl_query.py`
- [ ] T100 [P] 定义 NLQueryResponse Pydantic 模型在 `backend/app/schemas/nl_query.py`
- [ ] T101 配置 OpenAI API 客户端在 `backend/app/core/openai_client.py`
- [ ] T102 实现元数据上下文构建器在 `backend/app/services/context_builder.py`
  - 序列化表和列信息为 prompt
  - 优化上下文大小（仅包含相关表）
- [ ] T103 实现 prompt 模板在 `backend/app/prompts/sql_generation.py`
- [ ] T104 实现 NLQueryService 在 `backend/app/services/nl_query_service.py`
  - 调用 OpenAI API
  - 解析响应并提取 SQL
  - 错误处理（API 失败、配额超限）
- [ ] T105 实现 POST /api/queries/generate 端点在 `backend/app/api/endpoints/queries.py`
- [ ] T106 编写单元测试 `backend/tests/services/test_nl_query_service.py` (使用 mock)
- [ ] T107 编写集成测试 `backend/tests/api/test_nl_queries.py`

---

### 3.2 前端 LLM 集成

- [ ] T108 创建自然语言输入组件 `frontend/src/components/NaturalLanguageInput.tsx`
- [ ] T109 实现"生成 SQL"按钮和加载状态
- [ ] T110 实现生成成功后自动填充到编辑器并高亮
- [ ] T111 实现 LLM 错误处理和友好提示
- [ ] T112 添加自然语言输入历史记录（LocalStorage）
- [ ] T113 集成自然语言输入到查询页面

---

### 3.3 UI 优化与响应式设计

- [ ] T114 实现响应式布局适配桌面和平板在 `frontend/src/components/Layout.tsx`
- [ ] T115 添加键盘快捷键提示（Ctrl+Enter 执行，Ctrl+K 清空）
- [ ] T116 优化加载状态和骨架屏
- [ ] T117 统一 Toast/Notification 样式
- [ ] T118 添加首次使用引导（连接添加提示）
- [ ] T119 优化侧边栏折叠/展开动画
- [ ] T120 添加暗色主题支持（可选）

---

### 3.4 文档与部署

- [ ] T121 [P] 编写项目 README.md 在 `README.md`
  - 项目介绍
  - 快速开始
  - 功能说明
  - 环境变量配置
- [ ] T122 [P] 编写开发者指南在 `docs/DEVELOPMENT.md`
  - 环境搭建
  - 代码规范
  - 测试运行
- [ ] T123 [P] 编写部署指南在 `docs/DEPLOYMENT.md`
  - Docker Compose 部署
  - 环境变量配置
  - 生产环境注意事项
- [ ] T124 [P] 编写 API 文档在 `docs/API.md`（或利用 FastAPI 自动生成）
- [ ] T125 创建示例数据库种子数据 `backend/seeds/sample_data.sql`
- [ ] T126 配置生产环境 Docker 镜像 `Dockerfile`（后端和前端）
- [ ] T127 更新 `docker-compose.yml` 支持生产模式

---

### 3.5 测试与验收

- [ ] T128 编写 E2E 测试脚本（可选，使用 Playwright 或 Cypress）
- [ ] T129 性能测试：元数据加载 < 100ms
- [ ] T130 性能测试：SQL 验证 < 50ms
- [ ] T131 可访问性测试：键盘导航
- [ ] T132 浏览器兼容性测试（Chrome、Firefox、Safari）
- [ ] T133 记录已知问题和未来改进计划在 `docs/ROADMAP.md`

---

### Phase 3 验收测试

- [ ] T134 手动测试：输入自然语言生成 SQL
- [ ] T135 手动测试：验证生成的 SQL 自动填充到编辑器
- [ ] T136 手动测试：测试 LLM API 失败场景
- [ ] T137 手动测试：测试响应式布局（调整窗口大小）
- [ ] T138 手动测试：测试键盘快捷键
- [ ] T139 手动测试：在不同浏览器中测试
- [ ] T140 部署测试：使用 Docker Compose 部署并验证

---

## 任务统计

### 按阶段统计

| 阶段 | 任务数量 | 预估工作量 |
|-----|---------|----------|
| Phase 1: 基础设施与核心后端 | 56 | 64 小时 |
| Phase 2: 查询功能与前端 | 42 | 46 小时 |
| Phase 3: 增值功能与优化 | 42 | 34 小时 |
| **总计** | **140** | **144 小时** |

### 按类型统计

| 类型 | 任务数量 |
|-----|---------|
| 后端开发 | 52 |
| 前端开发 | 43 |
| 测试 | 28 |
| 文档 | 7 |
| 配置/基础设施 | 10 |

### 并行执行机会

以下任务可以并行执行（标记为 `[P]`）：

**Phase 1 并行组：**
- T019-T021: Pydantic 模型定义（3个任务）
- T029-T031: 元数据模型定义（3个任务）

**Phase 2 并行组：**
- T057-T059: 查询模型定义（3个任务）
- T070: QueryResult 接口定义
- T085: 错误响应格式
- T086: 错误消息组件

**Phase 3 并行组：**
- T099-T100: NL 查询模型定义（2个任务）
- T121-T124: 文档编写（4个任务）

**总并行机会：** 约 16 个任务可与其他任务并行，节省约 10-15% 的时间。

---

## 依赖关系图

```
Phase 1 (基础设施)
  ├─ 项目初始化 (T001-T011)
  ├─ 后端基础设施 (T012-T018)
  ├─ 连接管理 (T019-T028) ← 依赖后端基础设施
  ├─ 元数据提取 (T029-T038) ← 依赖连接管理
  └─ 前端基础设施 (T039-T048)
       ↓
Phase 2 (查询功能)
  ├─ SQL 验证 (T057-T064) ← 依赖 Phase 1 后端
  ├─ Monaco Editor (T065-T069) ← 依赖 Phase 1 前端
  ├─ 结果展示 (T070-T076) ← 依赖 SQL 验证 + Monaco
  ├─ 结构浏览 (T077-T084) ← 依赖元数据提取
  └─ 错误处理 (T085-T090)
       ↓
Phase 3 (增值功能)
  ├─ LLM 集成 (T099-T113) ← 依赖 Phase 2
  ├─ UI 优化 (T114-T120) ← 依赖 Phase 2
  └─ 文档部署 (T121-T140) ← 可提前开始
```

---

## 实施建议

### MVP 范围（最小可行产品）

**建议 MVP：Phase 1 + Phase 2 核心功能**

包含的功能：
- ✅ 连接管理（添加、列表、删除）
- ✅ 元数据提取与缓存
- ✅ SQL 查询验证与执行
- ✅ 查询结果展示
- ✅ 数据库结构浏览

**不包含：**
- ❌ 自然语言转 SQL（Phase 3）
- ❌ UI 高级优化（Phase 3）

**理由：** MVP 涵盖所有"必须有"的功能需求（FR1, FR2, FR3, FR5, FR6），可以作为独立可用的产品发布。

### 增量交付策略

1. **第1周：** Phase 1（基础设施与核心后端）
   - 里程碑：可以添加连接并查看元数据

2. **第2周：** Phase 2（查询功能与前端）
   - 里程碑：可以执行查询并查看结果（MVP 完成）

3. **第3周：** Phase 3（增值功能与优化）
   - 里程碑：添加 LLM 功能，优化 UI，完成文档

### 质量门控

每个 Phase 完成后进行验收测试：
- ✅ 所有功能测试通过
- ✅ 类型检查通过（mypy, TypeScript）
- ✅ API 响应为 camelCase
- ✅ 章程合规性检查

---

## 注意事项

1. **环境变量：** 确保 `OPENAI_API_KEY` 配置正确（Phase 3）
2. **SQLite 位置：** 默认使用 `~/.db_query/db_query.db`，确保目录可写
3. **测试数据库：** Docker Compose 提供的 PostgreSQL 仅用于开发测试
4. **性能目标：** 元数据加载 < 100ms，SQL 验证 < 50ms
5. **安全性：** 密码存储加密（可选但推荐）
6. **类型检查：** 所有代码必须通过 mypy 和 TypeScript 严格模式

---

**任务列表生成时间：** 2026-01-20  
**预计完成时间：** 3 周（按 18 工作日计算）
