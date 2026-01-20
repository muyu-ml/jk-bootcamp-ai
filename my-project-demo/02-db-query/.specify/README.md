# .specify 目录

本目录包含数据库查询工具项目的治理框架、模板和规格说明。

## 目录结构

```
.specify/
├── memory/
│   └── constitution.md       # 项目章程（不可妥协的原则）
├── templates/
│   ├── plan-template.md      # 实施计划模板
│   ├── spec-template.md      # 功能规格说明模板
│   ├── tasks-template.md     # 任务列表模板
│   └── commands/             # AI 代理的命令模板
│       ├── constitution.md   # 章程更新命令
│       ├── specify.md        # 规格说明创建命令
│       ├── plan.md           # 实施计划命令
│       └── tasks.md          # 任务生成命令
├── specs/                    # 功能规格说明（从模板创建）
├── plans/                    # 实施计划（从模板创建）
└── tasks/                    # 任务列表（从模板创建）
```

## 目的

`.specify` 框架确保：

1. **一致的工程标准：** 所有功能遵循章程原则
2. **系统化规划：** 规格说明、计划和任务遵循经过验证的模板
3. **章程合规性：** 每个制品都明确检查与原则的一致性
4. **可追溯性：** 从原则→规格→计划→任务→实施的清晰路径

## 章程

章程（`.specify/memory/constitution.md`）定义了 9 项核心原则：

1. **Ergonomic Python 与严格的 TypeScript** – 现代习惯用法，严格类型
2. **全面的类型标注** – 无无类型代码
3. **使用 Pydantic 进行数据建模** – 所有模式通过 Pydantic
4. **camelCase JSON 约定** – 前端友好的 API 响应
5. **无身份验证** – 开放访问（仅受信任环境）
6. **宽松的 CORS 策略** – 允许所有来源
7. **SQL 安全与查询限制** – 解析、验证、注入 LIMIT
8. **在 SQLite 中缓存元数据** – 本地持久化模式
9. **仅结构化数据响应** – 处处使用 JSON

详情请参阅 `memory/constitution.md`。

## 工作流程

### 1. 创建/更新章程

```bash
# 使用 constitution 命令更新原则
# 更新: .specify/memory/constitution.md
```

### 2. 编写功能规格说明

```bash
# 使用 specify 命令提供功能描述
# 创建: .specify/specs/{功能名称}-spec.md
# 验证: 每个需求的章程一致性
```

### 3. 创建实施计划

```bash
# 使用 plan 命令引用规格说明
# 创建: .specify/plans/{功能名称}-plan.md
# 包括: 章程检查、阶段、API 契约、测试
```

### 4. 生成任务列表

```bash
# 使用 tasks 命令引用计划
# 创建: .specify/tasks/{功能名称}-tasks.md
# 组织: 按章程原则组织任务
```

### 5. 实施与审查

- 按顺序完成任务
- 任务通过后标记为完成：
  - 类型检查（mypy、TypeScript）
  - 章程合规性
  - 测试通过

## 模板

### 规格说明模板

定义功能规格说明的结构：
- 章程一致性检查
- 带验收标准的功能需求
- 非功能需求（性能、安全、类型安全）
- API 契约（Pydantic + JSON）
- 数据模型
- 测试需求（最低 80% 覆盖率）

### 计划模板

定义实施计划的结构：
- 章程检查清单
- 带设计决策的技术方法
- 分阶段实施（目标、任务、成功标准）
- API 契约（snake_case → camelCase）
- 数据库变更
- 测试策略
- 风险评估

### 任务模板

定义任务列表的结构：
- 按章程原则组织的任务
- 每个任务：ID、描述、负责人、工作量、状态、依赖
- 横切任务（前端、集成、文档）
- 任务汇总表

## 命令

命令文件指导 AI 代理通过标准工作流程：

- **constitution.md:** 更新章程、升级版本、同步模板
- **specify.md:** 创建与章程一致的功能规格说明
- **plan.md:** 构建带阶段和检查的实施计划
- **tasks.md:** 生成按原则组织的可执行任务

## 最佳实践

1. **始终从章程开始：** 设计前了解适用原则
2. **每个制品中的章程检查：** 规格说明、计划、任务必须引用原则
3. **类型安全优先：** Mypy 和 TypeScript 严格模式不可妥协
4. **SQL 安全：** 所有查询在执行前通过 sqlglot 验证
5. **API 使用 camelCase：** 后端使用 snake_case，JSON 使用 camelCase
6. **80% 测试覆盖率：** 需要单元测试 + 集成测试
7. **记录假设：** 如果不清楚，在"待解决问题"部分注明

## 版本控制

- 章程版本遵循语义版本控制（MAJOR.MINOR.PATCH）
- 每次修订更新 `LAST_AMENDED_DATE` 并递增版本
- 同步影响报告跟踪变更和受影响的模板

## 参考

- 项目根目录：`my-project-demo/02-db-query/`
- 说明文档：`my-project-demo/specs/02-db-query/Instructions.md`
- 主 README：`my-project-demo/02-db-query/README.md`（待创建）
