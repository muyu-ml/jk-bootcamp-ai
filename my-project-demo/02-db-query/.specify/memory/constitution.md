<!--
同步影响报告 (2026-01-20):
- 版本: 新建 → 1.0.0 (初始批准)
- 修改的原则: 无 (初始创建)
- 新增章节: 全部 (初始创建)
  - 核心开发原则 (9项原则)
  - 架构指导原则
  - 治理机制
- 删除章节: 无
- 模板状态:
  ✅ .specify/templates/plan-template.md (已创建)
  ✅ .specify/templates/spec-template.md (已创建)
  ✅ .specify/templates/tasks-template.md (已创建)
  ✅ .specify/templates/commands/constitution.md (已创建)
  ✅ .specify/templates/commands/specify.md (已创建)
  ✅ .specify/templates/commands/plan.md (已创建)
  ✅ .specify/templates/commands/tasks.md (已创建)
  ✅ .specify/README.md (已创建)
- 后续待办事项: 无 (所有模板已创建并同步)
-->

# 项目章程：数据库查询工具

**版本：** 1.0.0  
**批准日期：** 2026-01-20  
**最后修订：** 2026-01-20

---

## 目的

本章程为数据库查询工具项目确立了不可妥协的工程原则和治理框架。它作为所有设计决策、实施标准和架构选择的权威参考。

---

## 项目标识

**项目名称：** 数据库查询工具 (DB Query Tool)  
**项目路径：** `my-project-demo/02-db-query`  
**项目描述：** 一个数据库查询工具，使用户能够连接数据库、查看元数据、执行 SQL 查询，并从自然语言提示生成 SQL。

**技术栈：**
- **后端：** Python (uv)、FastAPI、SQLglot、OpenAI SDK、Pydantic、SQLite
- **前端：** React、Refine 5、TypeScript、Tailwind CSS、Ant Design、Monaco Editor
- **目标数据库：** PostgreSQL (主要)，可扩展至其他 SQL 数据库

---

## 核心开发原则

### 原则 1：Ergonomic Python 与严格的 TypeScript

**规则：**  
后端必须使用 Ergonomic Python 风格编写——强调清晰、明确和现代 Python 习惯用法（类型提示、dataclasses、上下文管理器、PEP 8 合规）。前端必须使用启用严格类型检查的 TypeScript（`tsconfig.json` 中 `strict: true`）。

**理由：**  
- Python 工效学减少认知负荷，提高可维护性
- TypeScript 严格模式在编译时捕获类型错误，防止运行时故障
- 代码库的一致风格加速入职培训和代码审查

**实施方式：**
- 后端：使用 `ruff` 或 `black` 进行格式化，使用 `mypy` 进行类型检查
- 前端：启用 TypeScript 严格模式，使用 ESLint 配合 TypeScript 插件
- 所有函数、方法和模块必须包含类型注解

---

### 原则 2：全面的类型标注

**规则：**  
后端和前端代码都必须有严格的类型标注。TypeScript 中不允许使用 `Any` 类型；Python 中不允许无类型函数（除非类型标注根本不可能，必须记录理由）。

**理由：**  
强类型是防御 bug 的第一道防线，作为活文档，并支持强大的 IDE 工具（自动补全、重构、导航）。

**实施方式：**
- Python：每个函数签名必须声明参数和返回类型
- TypeScript：对所有 props、state、API 契约使用 interfaces/types
- 在专用模块中定义共享类型（`types.py`、`types.ts`）

---

### 原则 3：使用 Pydantic 进行数据建模

**规则：**  
所有后端数据模型（API 请求/响应模式、数据库模型、配置）必须使用 Pydantic 模型定义。禁止对结构化数据进行直接字典操作。

**理由：**  
Pydantic 提供运行时验证、自动文档生成（通过 FastAPI）以及与类型检查器的无缝集成。这消除了整类数据验证 bug。

**实施方式：**
- 将请求/响应模型定义为 Pydantic `BaseModel` 子类
- 对复杂约束使用 Pydantic 验证器
- 利用 FastAPI 的自动 OpenAPI 文档生成

---

### 原则 4：camelCase JSON 约定

**规则：**  
从后端发送到前端的所有 JSON 负载必须对属性名使用 `camelCase`。后端内部命名（Python）使用 `snake_case`；转换发生在序列化边界。

**理由：**  
JavaScript/TypeScript 约定是 `camelCase`。一致的 API 命名减少认知摩擦，消除前端转换逻辑的需求。

**实施方式：**
- 使用 `alias_generator=to_camel` 配置 Pydantic 模型
- 使用 FastAPI 的 `response_model` 配合 Pydantic 的 `by_alias=True`
- 前端接口以 camelCase 镜像后端模式

---

### 原则 5：无身份验证（开放访问）

**规则：**  
应用程序不得实施身份验证或授权机制。所有端点都是公开访问的。没有用户账户、会话或令牌。

**理由：**  
这是一个面向单用户或受信任环境使用的开发/演示工具。移除身份验证复杂性减少范围并加快交付。安全性委托给部署环境（例如 VPN、防火墙、仅本地绑定）。

**实施方式：**
- 不使用 JWT、OAuth 或会话中间件
- 在 README 中明确记录这不适用于不受信任的网络生产环境
- 未来：如果需要多用户支持，可以作为 v2.0 功能添加身份验证

---

### 原则 6：宽松的 CORS 策略

**规则：**  
后端 API 必须为所有来源启用 CORS（`Access-Control-Allow-Origin: *`）。没有域限制。

**理由：**  
前端可能从不同端口（开发服务器）或域（静态托管）提供服务。开放 CORS 简化本地开发和部署灵活性。鉴于无身份验证姿态，这是可接受的。

**实施方式：**
- 使用 FastAPI 的 `CORSMiddleware`，配置 `allow_origins=["*"]`
- 在应用程序启动时包含在中间件栈中

---

## 架构指导原则

### 原则 7：SQL 安全与查询限制

**规则：**  
所有用户提供的 SQL 必须在执行前使用 SQLglot 解析和验证。仅允许 `SELECT` 语句。不合规的查询必须被拒绝并给出明确的错误消息。如果不存在 `LIMIT` 子句，必须注入一个（默认：`LIMIT 1000`）。

**理由：**  
防止破坏性操作（DROP、DELETE、UPDATE）和可能压垮数据库或前端的失控查询。保护免受意外数据丢失和拒绝服务攻击。

**实施方式：**
- 使用 `sqlglot.parse_one()` 解析 SQL
- 检查 AST 语句类型（仅允许 `Select`）
- 如果缺少则注入 `LIMIT 1000`
- 对于无效 SQL 返回 400 Bad Request 并带详细错误信息

---

### 原则 8：在 SQLite 中缓存元数据

**规则：**  
数据库连接字符串和模式元数据（表、视图、列、类型）必须持久化在本地 SQLite 数据库中。元数据刷新是显式的，不是自动的。缓存的元数据用于 LLM 上下文生成。

**理由：**  
减少延迟和数据库负载（元数据查询代价高昂）。启用离线浏览和更快的 LLM 提示构建。显式刷新让用户控制。

**实施方式：**
- SQLite 模式：`connections`、`tables`、`columns` 表
- API 端点：`POST /connections`（添加）、`POST /connections/{id}/refresh`（元数据同步）
- LLM 上下文：将缓存的元数据序列化为 JSON 用于提示注入

---

### 原则 9：仅结构化数据响应

**规则：**  
所有 API 响应必须使用结构化 JSON。不允许纯文本、HTML 或 CSV 响应（除非 CSV 导出是显式功能，单独记录）。

**理由：**  
JSON 是机器可读的、类型安全的且普遍支持的。简化前端解析和错误处理。

**实施方式：**
- FastAPI 响应模型返回 Pydantic 对象
- 错误遵循 JSON:API 或 RFC 7807 (Problem Details) 格式
- 前端期望 JSON，无回退解析逻辑

---

## 治理机制

### 修订程序

1. **提案：** 任何团队成员都可以通过 pull request 提出章程修订
2. **审查：** 修订必须由至少一名其他贡献者审查
3. **论证：** 提案必须包括：
   - 变更的明确理由
   - 影响分析（什么会损坏，什么会改进）
   - 迁移路径（如果向后不兼容）
4. **批准：** 需要达成共识（没有阻止性反对意见）
5. **版本升级：** 根据语义版本控制更新版本
6. **传播：** 根据检查清单更新所有依赖模板和文档

### 版本控制策略

- **MAJOR** (X.0.0)：向后不兼容的变更（移除/重新定义原则，更改技术栈）
- **MINOR** (0.X.0)：添加新原则，实质性扩展指导
- **PATCH** (0.0.X)：澄清、错别字修复、非语义编辑

### 合规审查

- 合并任何功能分支前，验证遵守章程
- 违反原则的 PR 需要明确的豁免理由（临时技术债务、紧急热修复）
- 季度审查：检查原则是否仍服务于项目目标；如果过时则提出修订

---

## 原则摘要（快速参考）

1. **Ergonomic Python 与严格的 TypeScript** – 现代习惯用法，严格类型
2. **全面的类型标注** – 无无类型代码
3. **使用 Pydantic 进行数据建模** – 所有模式通过 Pydantic
4. **camelCase JSON 约定** – 前端友好的 API 响应
5. **无身份验证** – 开放访问（仅受信任环境）
6. **宽松的 CORS 策略** – 允许所有来源
7. **SQL 安全与查询限制** – 解析、验证、注入 LIMIT
8. **在 SQLite 中缓存元数据** – 本地持久化模式
9. **仅结构化数据响应** – 处处使用 JSON

---

**章程结束**
