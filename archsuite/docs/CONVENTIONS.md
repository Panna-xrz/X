# ArchSuite 编码规范

> 前后端命名、分层职责、主题令牌、Git 流程的统一约定。新增代码必须遵守。

## 1. 总则

- 注释统一中文；变量/函数名英文。
- 优先复用成熟库，不重复造轮子；通用工具进 `utils`，避免散落。
- 类型优先：后端全类型注解 + mypy；前端 `strict` TypeScript。
- 不做无谓抽象：一次性逻辑内联，重复 ≥3 次再抽公共。
- 错误处理只在系统边界（HTTP / 外部 AI / 文件 IO）做；内部信任框架与类型。

## 2. 后端规范（Python / FastAPI）

### 2.1 命名
- 包/模块：`snake_case`，单数名词（`project.py`、`contract_service.py`）。
- 类：`PascalCase`（`ProjectService`、`CRUDProject`）。
- 函数/变量：`snake_case`，动词开头（`get_project`、`create_contract`）。
- 常量：`UPPER_SNAKE`（`BORDER_NONE`、`DEFAULT_PAGE_SIZE`）。
- 路由文件名用资源复数（`projects.py`、`contracts.py`）。

### 2.2 分层职责（严禁跨层）
| 层 | 文件 | 职责 | 禁止 |
|---|---|---|---|
| api | `api/v1/*.py` | 入参校验、调 service、组装响应 schema | 直接调 crud / models |
| service | `services/*.py` | 业务规则、事务、编排 CRUD 与 AI | 直接处理 HTTP |
| crud | `crud/*.py` | 单模型原子读写 | 含业务规则 |
| models | `models/*.py` | 表结构、关系 | 依赖上层 |

### 2.3 API 路由
- 资源复数、RESTful：`GET /projects`、`POST /projects`、`GET /projects/{id}`、`PUT /projects/{id}`、`DELETE /projects/{id}`。
- 自定义动作用子路径：`POST /projects/{id}/ai-extract`。
- 所有路由组挂 `prefix` 与 `tags`，统一在 `router.py` 聚合到 `/api/v1`。
- 入参出参一律 Pydantic schema，禁用裸 dict。
- 全异步 `async def`，数据库操作用 `AsyncSession`。

### 2.4 ORM / 数据库
- 统一继承 `Base(DeclarativeBase)`，混入 `TimestampMixin`。
- 关系用 `relationship` 显式声明，避免隐式 join 行为。
- 迁移走 Alembic：`alembic revision --autogenerate -m "msg"` + `alembic upgrade head`；禁止手改库结构。
- 长事务在 service 层管理；crud 保持原子。

### 2.5 AI 层
- 业务只调 `ai.factory.get_provider()`，不直接 new 具体 provider。
- prompt 构造放 `ai/prompts/`，为纯函数返回 `list[AIMessage]`，便于单测与复用。
- 新增厂商：实现 `AIProvider` 子类 + 在 `factory` 注册分支，禁止改业务代码。

### 2.6 格式化与质量
- `black` 格式化、`ruff` 检查、`mypy` 严格类型；提交前本地跑 `black . && ruff check . && mypy app`。

## 3. 前端规范（Vue 3 / Naive UI）

### 3.1 命名
- 组件文件与组件名 `PascalCase`（`ProjectList.vue`、`AppSidebar.vue`）。
- 组合式变量/函数 `camelCase`；常量 `UPPER_SNAKE`。
- 类型名 `PascalCase`（`interface Project`）。
- 页面按模块归目录：`views/<module>/<Page>.vue`。

### 3.2 组件
- 统一 `<script setup lang="ts">` 组合式 API，禁用 Options API。
- 单文件组件顺序：`<script setup>` → `<template>` → `<style scoped>`。
- props 用 `defineProps<{ ... }>()` 类型声明；事件用 `defineEmits<{ ... }>()`。
- 公共组件入 `components/`；页面专属子组件随页面就近放置。

### 3.3 分层职责
| 层 | 位置 | 职责 |
|---|---|---|
| views | `views/<module>/*.vue` | 页面交互、组装数据与组件 |
| stores | `stores/*.ts` | 跨页面共享状态（如主题） |
| api | `api/*.ts` | 接口请求与数据类型化，禁在 views 内裸调 axios |
| styles | `styles/*` | 令牌、主题覆盖、全局样式 |

- views 调 `api/*` 拿数据；跨页共享状态走 Pinia store；纯组件无业务逻辑。

### 3.4 路由与侧栏
- 每个业务模块在 `router/index.ts` 独立路由组，懒加载 `() => import(...)`。
- 侧栏 `AppSidebar` 每模块独立分组（n-menu group），子项可展开；新增模块同步加菜单项与路由。
- 占位模块统一指向 `Placeholder.vue`。

## 4. 主题与设计令牌规范

### 4.1 令牌集中
- 所有色值、字体族、字号、间距、圆角、阴影统一来自 `src/styles/tokens.ts` 的 `designTokens`。
- 禁止在组件内写魔法色值或硬编码字号；必须引用令牌或 CSS 变量。

### 4.2 主题覆盖
- Naive UI 主题只通过 `styles/theme.ts` 的 `generateThemeOverrides(state)` 生成，源头是 `theme` store。
- 运行时切换主色/字体/字号/亮暗由 `ThemeSwitch` 触发，写 `localStorage` 持久化，并同步 `:root` CSS 变量与 `data-theme`。

### 4.3 无边框原则
- 组件不主动加 `border`；分隔改用间距、留白、弱化背景或 `BORDER_NONE`（`1px solid transparent`）。
- 必要的视觉分隔用 `tokens` 中极浅半透明色，禁止实色边框。
- 表格行分隔用 `dividerColor` 弱化色，非实线。

### 4.4 可维护性
- 字体族、字号、圆角、间距梯度均暴露在 `tokens` 与 `theme` store，便于全局调整与个性化。
- 新增组件如需主题相关样式，优先用 Naive UI 主题覆盖，而非组件内 scoped 硬编码。

## 5. Git 规范

### 5.1 分支
- `main`：可发布稳定版。
- `dev`：集成开发。
- `feat/<module>-<short>`：功能分支，如 `feat/project-ai-extract`。
- `fix/<short>`：修复分支。

### 5.2 Commit（Conventional Commits）
格式：`<type>(<scope>): <subject>`，type ∈ `feat|fix|refactor|docs|style|test|chore|perf`。
示例：
- `feat(project): 新增 AI 扩展信息提取接口`
- `fix(contract): 修正补充协议关联主合同逻辑`
- `docs(arch): 补充架构图`

### 5.3 评审
- 提交前本地：后端 `black . && ruff check . && mypy app`；前端 `npm run type-check`。
- 不提交 `.env`、`*.db`、`node_modules/`、`backend/static/`、`.venv/`。

## 6. 文件与目录命名

- 目录：全小写 `kebab-case` 或单数名词（`project`、`commerce`、`placeholder`）。
- 文档：`UPPER_SNAKE.md`（`ARCHITECTURE.md`、`CONVENTIONS.md`）。
- 脚本：`snake_case.sh`。
- 配置：小写约定名（`pyproject.toml`、`package.json`、`vite.config.ts`、`.env.example`）。
