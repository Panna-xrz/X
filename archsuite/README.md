# ArchSuite — 建筑设计项目 AI 管理平台

基于 AI API 的建筑设计项目全生命周期管理与辅助设计系统。本仓库为系统架构与目录体系设计成果。

## 技术栈

| 层 | 选型 |
|---|---|
| 后端 | FastAPI · SQLAlchemy 2.0 (async) · SQLite · Alembic · Pydantic v2 |
| 前端 | Vue 3 · Naive UI · Vite · Pinia · Vue Router · TypeScript · Sass |
| AI | 多提供商抽象层（OpenAI 兼容 / Anthropic Claude / 国内原生） |
| 隔离 | venv + 前端构建静态托管，与系统环境解耦 |
| 部署 | Debian 单机，无认证单机使用 |

## 目录结构

```
archsuite/
├── README.md
├── .gitignore
├── docs/                      # 架构与规范文档
│   ├── ARCHITECTURE.md        # 分层架构 / 目录体系 / AI 抽象层
│   └── CONVENTIONS.md         # 编码规范 / 主题令牌 / 命名
├── scripts/                   # 运行脚本
│   ├── setup.sh
│   ├── build_frontend.sh
│   └── run.sh
├── backend/                   # FastAPI 后端
│   ├── pyproject.toml
│   ├── .env.example
│   ├── app/
│   │   ├── main.py            # 入口，挂载路由 + 静态托管
│   │   ├── core/              # 配置 / 数据库 / 日志 / 异常
│   │   ├── api/v1/            # 路由层（projects/contracts/billing/ai）
│   │   ├── models/            # ORM 模型层
│   │   ├── schemas/           # Pydantic 数据契约层
│   │   ├── crud/              # 数据访问层
│   │   ├── services/          # 业务逻辑层
│   │   ├── ai/                # AI 抽象层（base/factory/providers/prompts）
│   │   └── utils/
│   ├── alembic/               # 数据库迁移
│   └── tests/
└── frontend/                  # Vue 3 前端
    ├── package.json
    ├── vite.config.ts
    └── src/
        ├── main.ts
        ├── App.vue
        ├── router/            # 路由
        ├── stores/            # Pinia（theme 等）
        ├── styles/            # 设计令牌 / 主题覆盖 / 全局样式
        ├── api/               # 接口请求层
        ├── types/            # TS 类型
        ├── components/layout/ # 主布局 / 侧栏 / 顶栏 / 主题切换
        └── views/             # 页面（project/commerce/placeholder）
```

## 功能模块

1. **项目信息** — 多表存储项目基本信息与扩展信息，部分信息经 AI 自动获取
2. **商务管理** — 合同起草/审核/管理，支持一项目多合同（主合同 + 补充协议）、项目节点、收费节点、记账
3. 环境解析（暂不实现，占位）
4. 概念构思（暂不实现，占位）
5. 平面构成（暂不实现，占位）
6. 空间构成（暂不实现，占位）

## 快速开始

```bash
./scripts/setup.sh           # 创建 venv + 安装前后端依赖
./scripts/build_frontend.sh  # 构建前端到 backend/static
./scripts/run.sh             # 启动 uvicorn (0.0.0.0:8000)
# 浏览器访问 http://localhost:8000
```

## 文档

- 架构设计：[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- 编码规范：[docs/CONVENTIONS.md](docs/CONVENTIONS.md)
