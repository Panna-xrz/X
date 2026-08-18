# ArchSuite 架构设计

> 建筑设计项目 AI 管理平台 — 整体架构、目录体系、分层职责与扩展机制。

## 1. 概述

ArchSuite 面向建筑设计单位，提供"项目信息 → 商务管理 → 设计辅助"的全流程数字化与 AI 辅助能力。本期实现 **项目信息** 与 **商务管理** 两大模块；环境解析、概念构思、平面构成、空间构成以占位页形式预留，按既定分层接入即可。

**设计原则**
- **分层清晰**：前后端均严格分层，禁止跨层调用。
- **模块独立**：每个业务模块拥有独立的 model / schema / crud / service / view，互不耦合，仅通过显式接口交互。
- **AI 抽象**：AI 能力统一抽象为 `AIProvider`，按配置切换 OpenAI 兼容 / Anthropic / 国内原生，业务层不感知具体厂商。
- **现代无边框 UI**：基于设计令牌与 Naive UI 主题覆盖，全局扁平、无边框、主题/字体/颜色运行时可配。
- **环境隔离**：venv + 前端构建静态托管，单机部署，与系统环境解耦。
- **不重复造轮子**：优先使用成熟库（FastAPI / SQLAlchemy / Naive UI / Pinia / openai / anthropic SDK）。

## 2. 技术栈

| 维度 | 选型 |
|---|---|
| 后端 | FastAPI · SQLAlchemy 2.0(async) · aiosqlite · Alembic · Pydantic v2 · pydantic-settings |
| 前端 | Vue 3 · Naive UI · Vite · Pinia · Vue Router · Axios · TypeScript · Sass |
| AI | 多提供商抽象（OpenAI 兼容 / Anthropic Claude / 国内原生 DashScope） |
| 数据库 | SQLite（单文件，便于单机） |
| 运行 | venv + uvicorn + 前端 dist 静态托管 |
| 质量 | ruff / black / mypy（后端）；ESLint / Prettier / vue-tsc（前端） |

## 3. 分层架构

### 3.1 后端分层（自上而下，单向依赖）

```
┌──────────────────────────────────────────────┐
│  API 路由层   app/api/v1/*.py                │  HTTP 入参校验、调用 service、返回 schema
├──────────────────────────────────────────────┤
│  业务逻辑层   app/services/*.py              │  编排 CRUD + AI，业务规则、事务边界
├──────────────────────────────────────────────┤
│  数据访问层   app/crud/*.py                  │  单模型原子读写，泛型 CRUDBase
├──────────────────────────────────────────────┤
│  ORM 模型层   app/models/*.py                │  表结构定义、关系映射
├──────────────────────────────────────────────┤
│  基础设施     app/core/                      │  config / database / logging / exceptions
└──────────────────────────────────────────────┘
        ▲ 业务层经 app/ai/ 调用 AI 能力（独立横切）
```

**依赖规则**
- `api` 只依赖 `services` 与 `schemas`；不直接调 `crud` / `models`。
- `services` 依赖 `crud`、`schemas`、`ai`；不直接操作 HTTP。
- `crud` 只依赖对应单个 `models`；不包含业务规则。
- `models` 不依赖任何上层。
- `ai` 层独立，被 `services` 调用，本身不依赖业务模型。

### 3.2 前端分层

```
┌──────────────────────────────────────────────┐
│  视图层   src/views/<module>/*.vue           │  页面与交互，组合式 API
├──────────────────────────────────────────────┤
│  布局层   src/components/layout/*.vue         │  主布局 / 侧栏 / 顶栏 / 主题切换
├──────────────────────────────────────────────┤
│  状态层   src/stores/*.ts                    │  Pinia store（theme / 业务状态）
├──────────────────────────────────────────────┤
│  接口层   src/api/*.ts                       │  axios 封装与按模块拆分接口
├──────────────────────────────────────────────┤
│  基础     src/styles  src/router  src/types  │  设计令牌 / 路由 / 类型
└──────────────────────────────────────────────┘
        ▲ views 通过 api 调后端 /api/v1
```

## 4. 目录体系

```
archsuite/
├── README.md
├── .gitignore
├── docs/
│   ├── ARCHITECTURE.md
│   └── CONVENTIONS.md
├── scripts/
│   ├── setup.sh               # 初始化 venv + 前端依赖
│   ├── build_frontend.sh      # 构建并托管前端
│   └── run.sh                 # 启动服务
├── backend/
│   ├── pyproject.toml
│   ├── .env.example
│   ├── app/
│   │   ├── main.py            # 入口：路由 + 静态托管
│   │   ├── core/
│   │   │   ├── config.py      # Settings(BaseSettings) 读 .env
│   │   │   ├── database.py    # async engine + AsyncSession + get_db
│   │   │   ├── logging.py
│   │   │   └── exceptions.py  # AppException + 全局 handler
│   │   ├── api/
│   │   │   ├── deps.py        # get_db / get_ai_provider
│   │   │   └── v1/
│   │   │       ├── router.py  # 聚合各模块 router
│   │   │       ├── projects.py
│   │   │       ├── contracts.py
│   │   │       ├── billing.py
│   │   │       └── ai.py
│   │   ├── models/
│   │   │   ├── base.py        # Base + TimestampMixin
│   │   │   ├── project.py     # Project + ProjectExtra（多表）
│   │   │   └── contract.py    # Contract + ContractNode + BillingRecord
│   │   ├── schemas/
│   │   │   ├── common.py      # PageResult[T] 泛型
│   │   │   ├── project.py
│   │   │   └── contract.py
│   │   ├── crud/
│   │   │   ├── base.py        # CRUDBase[T]
│   │   │   ├── project.py     # CRUDProject（含扩展信息）
│   │   │   └── contract.py    # CRUDContract（含补充协议）
│   │   ├── services/
│   │   │   ├── project_service.py   # 编排 CRUD + AI 提取
│   │   │   └── contract_service.py  # 合同生成/审核业务
│   │   ├── ai/
│   │   │   ├── base.py        # AIProvider ABC + AIMessage
│   │   │   ├── openai_provider.py   # OpenAI 兼容（DeepSeek/Qwen/Moonshot 同构）
│   │   │   ├── anthropic_provider.py
│   │   │   ├── domestic_provider.py # 国内原生（DashScope 示例）
│   │   │   ├── factory.py     # get_provider() 工厂 + 缓存
│   │   │   └── prompts/
│   │   │       ├── project_info.py
│   │   │       └── contract_review.py
│   │   └── utils/
│   ├── alembic/
│   │   ├── env.py
│   │   ├── script.py.mako
│   │   └── versions/
│   ├── static/                # 前端构建产物（gitignore）
│   └── tests/
└── frontend/
    ├── package.json
    ├── vite.config.ts         # base './' + /api 代理到 8000
    ├── tsconfig.json
    ├── index.html
    └── src/
        ├── main.ts
        ├── App.vue            # NConfigProvider 包裹（主题来源 theme store）
        ├── router/index.ts    # 6 模块路由，3-6 懒加载到 Placeholder
        ├── stores/
        │   └── theme.ts       # 主题/字体/颜色/圆角，localStorage 持久化
        ├── styles/
        │   ├── tokens.ts      # 设计令牌（色板/字体/间距/圆角/无边框常量）
        │   ├── theme.ts       # generateThemeOverrides() 主题覆盖
        │   └── global.scss    # reset + :root 变量
        ├── api/
        │   ├── request.ts     # axios 实例 + 拦截器
        │   ├── project.ts
        │   └── contract.ts
        ├── types/index.ts     # Project/Contract/Billing 等接口
        ├── components/
        │   └── layout/
        │       ├── AppLayout.vue
        │       ├── AppSidebar.vue   # 6 模块独立分组侧栏
        │       ├── AppHeader.vue
        │       └── ThemeSwitch.vue  # 亮/暗 + 主色 + 字体 + 字号
        └── views/
            ├── project/   ProjectList / ProjectDetail
            ├── commerce/  ContractList / ContractEditor / BillingList
            └── placeholder/ Placeholder.vue
```

## 5. 业务模块设计

### 模块 1：项目信息（已实现骨架）
- **多表存储**：`Project` 主表（名称/编号/位置/类型/规模/描述等基本字段）+ `ProjectExtra` 扩展表（`field_key` / `field_value` / `ai_source`），可无限扩展字段而不改表结构。
- **AI 自动获取**：`POST /api/v1/projects/{id}/ai-extract` → `project_service.ai_extract_info` 调用 `AIProvider`，使用 `prompts/project_info.build_extract_prompt` 让 AI 从基本字段推断用地性质、容积率、建筑限高、绿化率等扩展信息，写入 `ProjectExtra` 并标记来源。

### 模块 2：商务管理（已实现骨架）
- **一项目多合同**：`Contract.contract_type` ∈ {`main` 主合同, `supplement` 补充协议}；补充协议通过 `parent_contract_id` 指向主合同，形成合同树。
- **合同流程**：`POST /contracts/{id}/generate`（AI 起草）→ `POST /contracts/{id}/review`（AI 审核条款风险，用 `prompts/contract_review.build_review_prompt`）。
- **节点与记账**：`ContractNode`（项目节点 / 进度节点 / 收费节点）+ `BillingRecord`（收款/退款记账），均以 `contract_id` 归属。

### 模块 3–6：占位
- 环境解析、概念构思、平面构成、空间构成路由统一指向 `Placeholder.vue`，显示"暂不实现（规划中）"。
- **接入新模块的标准步骤**（保持架构一致）：
  1. 后端：`models/<m>.py` → `schemas/<m>.py` → `crud/<m>.py` → `services/<m>_service.py` → `api/v1/<m>.py` → 在 `router.py` 注册。
  2. 前端：`api/<m>.ts` → `types` 补类型 → `views/<m>/*.vue` → `router/index.ts` 加路由 → `AppSidebar` 加菜单项。
  3. AI 能力：`ai/prompts/<m>.py` 加 prompt 构造函数，service 调用。

## 6. 数据模型

```
Project 1 ─── n ProjectExtra            # 项目多表扩展
Project 1 ─── n Contract                # 一项目多合同
Contract (main) 1 ─── n Contract (supplement)  # 补充协议挂主合同
Contract 1 ─── n ContractNode           # 项目/进度/收费节点
Contract 1 ─── n BillingRecord          # 收款/退款记账
```

- 主键统一 `id`（自增整数），所有表含 `TimestampMixin`（created_at / updated_at）。
- 外键级联：删除项目级联其下合同与扩展信息（业务层显式处理，避免数据孤岛）。

## 7. AI 抽象层

```
app/ai/
├── base.py            AIProvider(ABC): chat(messages) / complete(prompt)
├── openai_provider.py    基于 openai.AsyncOpenAI（base_url 可指向 DeepSeek/Qwen 兼容端点）
├── anthropic_provider.py 基于 anthropic.AsyncAnthropic
├── domestic_provider.py  httpx 调 DashScope（国内原生，可改走 OpenAI 兼容）
├── factory.py         get_provider(name?) 按 settings.ai_default_provider 返回缓存实例
└── prompts/           纯函数构造 AIMessage 列表，与厂商解耦
```

- **调用路径**：`api` → `service` → `get_provider()` → `provider.chat(prompt)` → 结果回写业务表。
- **切换厂商**：仅改 `.env` 的 `AI_DEFAULT_PROVIDER` 与对应 KEY/BASE_URL/MODEL，业务代码零改动。
- **新增厂商**：实现 `AIProvider` 子类 + 在 `factory.py` 注册分支即可。

## 8. 主题与设计令牌系统

- **令牌集中**：`frontend/src/styles/tokens.ts` 导出 `designTokens`（亮/暗色板、字体族候选、字号/间距/圆角梯度、阴影、`BORDER_NONE` 常量）。
- **主题覆盖**：`styles/theme.ts` 的 `generateThemeOverrides(state)` 返回 Naive UI `GlobalThemeOverrides`，覆盖 `common` 主色/圆角/字号/字体，并去除 Card / FormItem / ListItem / Tag / Input / Button / DataTable / Menu 等组件边框。
- **运行时切换**：`stores/theme.ts` 持有 `themeName / primaryColor / fontFamily / fontSize / borderRadius / isDark`，`ThemeSwitch.vue` 提供亮/暗按钮 + 气泡内主色/字体/字号实时调整，写入 `localStorage` 持久化并同步 `:root` CSS 变量与 `data-theme`。
- **无边框原则**：组件不主动 `border`，分隔改用间距、留白与弱化背景；如需分隔使用 `BORDER_NONE` 或极浅半透明色。

## 9. 环境隔离与运行

- **后端隔离**：`scripts/setup.sh` 在项目内创建 `.venv`，依赖装在 venv；`run.sh` 始终 `source .venv`。
- **前端隔离**：依赖装在 `frontend/node_modules`；`build_frontend.sh` 产出 `dist` 并复制到 `backend/static/`。
- **静态托管**：`app/main.py` 用 `StaticFiles(html=True)` 把前端 SPA 挂到根路径，API 在 `/api/v1`，单端口访问 `http://localhost:8000`。
- **配置**：`backend/.env`（从 `.env.example` 复制）含数据库与各 AI 厂商密钥，不提交版本库。

## 10. 扩展性

- 新增业务模块遵循第 5 节"接入新模块的标准步骤"，分层与命名不变。
- AI 厂商扩展遵循第 7 节工厂模式。
- 主题与令牌扩展遵循第 8 节集中令牌原则。
- 数据库迁移：改 `models` 后 `alembic revision --autogenerate` + `alembic upgrade head`。
