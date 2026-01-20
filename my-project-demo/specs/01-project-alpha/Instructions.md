# project alpha 需求和设计文档

构建一个简单的，使用标签分类和管理 ticket 的工具。
它基于 Postgres 数据库，使用 Fast API 作为后端，使用 TypeScript/Vite/Tailwind/Shadcn 作为前端。无需用户系统。当前用户可以：

- 创建/编辑/删除/完成/取消完成 ticket
- 创建/编辑/删除 ticket标签
- 按照不同的标签查看 ticket 列表
- 按 title 搜索 ticket

按照这个想法帮我生成详细的需求和设计文档，放在 ./specs/my-w1 文件中，输出为中文。

## implementation plan
按照 ./specs/my-w1/design.md 中的需求和设计文档，生成一个详细的实现计划，放在 ./specs/my-w1/implementation-plan.md 文件中，输出为中文。
项目文档放在 ./specs/my-w1/project-alpha 下


## phased implementation
按照 ./specs/my-w1/implementation-plan.md 完整实现这个项目的 phase 1 代码

开发 phase 2 的全部功能

帮我根据 rest client 撰写一个 test.rest 文件，里面包含对所有支持的 API 的测试


添加一个 seed.sql 里面放 50个 meaningful 的 ticket 和几十个 tags（包含platform tag，如 ios，project tag 如 viking，功能性 tag 如 autocomplete，等等）。要求 seed 文件正确可以通过 pgsql 执行。

开发 phase 3 的全部功能

开发 phase 4 的全部功能

开发 phase 5 & 6 的全部功能

## 优化 UI
按照 apple website 的设计风格，think ultra hard，优化 UI 和 UX。

## 启动方式
在根目录下 Makefile 里添加启动 app 的方法，不要使用 start.sh 的方式
更新 Makefile，为所有 target 天街 “w1-” 前缀，并重构合并的 target

## 代码提交
1、将原有的远程仓库地址设置为新项目fork地址（即该代码是从哪个仓库fork的）
2、将项目远程仓库设置为git@github.com:muyu-ml/jk-bootcamp-ai.git
3、从fork的仓库中更新最新代码到当前远程仓库，并拉取到本地
4、将本地代码提交到新远程仓库