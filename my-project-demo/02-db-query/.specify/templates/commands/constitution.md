---
description: 从交互式或提供的原则输入创建或更新项目章程，确保所有依赖模板保持同步。
handoffs: 
  - label: 构建规格说明
    agent: speckit.specify
    prompt: 基于更新的章程实施功能规格说明。我想构建...
---

## 用户输入

```text
{user_input}
```

您**必须**在继续之前考虑用户输入（如果非空）。

## 大纲

您正在更新位于 `.specify/memory/constitution.md` 的项目章程。此文件包含数据库查询工具项目不可妥协的工程原则。

遵循此执行流程：

1. **加载现有章程**，位于 `.specify/memory/constitution.md`
   - 如果不存在，使用当前版本作为基础模板
   
2. **收集/推导值：**
   - 使用对话中的用户输入
   - 从项目上下文推断（README、文档、代码库）
   - 对于日期：`RATIFICATION_DATE` 是原始采用日期，`LAST_AMENDED_DATE` 是今天（如果有变更）
   - `CONSTITUTION_VERSION` 遵循语义版本控制：
     - MAJOR：向后不兼容的变更（移除/重新定义原则）
     - MINOR：新原则或实质性扩展
     - PATCH：澄清、错别字、非语义修复

3. **起草更新的章程：**
   - 保留标题层次结构
   - 每个原则：名称、规则、理由、实施指导
   - 确保治理部分包括修订程序、版本控制策略、合规审查期望

4. **一致性传播：**
   - 验证 `.specify/templates/plan-template.md` 的章程检查与原则一致
   - 验证 `.specify/templates/spec-template.md` 的章程一致性部分是最新的
   - 验证 `.specify/templates/tasks-template.md` 的任务分类反映原则结构
   - 如需要更新命令文件

5. **生成同步影响报告**（作为 HTML 注释前置）：
   - 版本变更（旧 → 新）
   - 修改的原则
   - 新增/删除的章节
   - 模板状态（✅ 已更新 / ⚠ 待处理）
   - 后续待办事项

6. **验证：**
   - 无未解释的占位符标记
   - 版本与报告匹配
   - 日期为 ISO 格式（YYYY-MM-DD）
   - 原则是声明性的和可测试的

7. **写回** `.specify/memory/constitution.md`

8. **输出摘要：**
   - 新版本和升级理由
   - 标记为需手动跟进的文件
   - 建议的提交消息

## 格式要求

- 使用模板中显示的 Markdown 标题
- 换行长行（约 100 字符）
- 章节之间使用单个空行
- 无尾随空格

如果缺少关键信息，在报告中插入 `TODO(<字段名>): 说明`。

始终操作现有的 `.specify/memory/constitution.md` 文件。
