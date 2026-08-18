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
│   │   ├── main.py            # 入口，挂载路由 + SPA 静态托管
│   │   ├── core/              # 配置 / 数据库 / 日志 / 异常
│   │   ├── api/v1/            # 路由层（projects/contracts/nodes/contacts/ai）
│   │   ├── models/            # ORM 模型层（project/contract/contact/project_detail）
│   │   ├── schemas/           # Pydantic 数据契约层（camelCase）
│   │   ├── crud/              # 数据访问层
│   │   ├── services/          # 业务逻辑层
│   │   ├── ai/                # AI 抽象层（base/factory/providers/prompts）
│   │   └── utils/             # JSON 解析等工具
│   ├── alembic/               # 数据库迁移
│   └── tests/
└── frontend/                  # Vue 3 前端
    ├── package.json
    ├── vite.config.ts
    └── src/
        ├── main.ts
        ├── App.vue
        ├── router/            # 路由
        ├── stores/            # Pinia（project 当前项目状态 / theme）
        ├── styles/            # 设计令牌 / 主题覆盖 / 全局样式
        ├── api/               # 接口请求层（project/contract/contact/request）
        ├── types/             # TS 类型（与后端 camelCase 契约一一对齐）
        ├── components/        # 布局（IconBar/ProjectSwitcher）/ 图标组件 / 高德地图
        └── views/             # 页面（project/commerce/settings/placeholder）
```

## 功能模块

1. **项目信息** — 全生命周期项目数据管理，6 个子项：
   - 基本信息（名称/编号/地址/类型/阶段/委托甲方）
   - 指标信息（用地性质/场地面积/容积率/绿地率/建筑密度/停车位）
   - 场地周边（高德地图选点/经纬度/200m·500m·2000m范围/道路/自然景观/交通）
   - 物理环境（气候区/主导风向/日照/降水量/地下水位/海拔/温度）
   - 人文环境（文化符号/地域建筑符号/城市色彩/风俗/历史文化）
   - 建筑立项（每个建筑单体：性质/功能/层数/高度/面积）
2. **商务管理** — 5 个子项：
   - 联系单（委方甲方联系人 + 项目小组联系人）
   - 合同预览（正文展示 + 下载）
   - 合同草拟（内置模板 AI 起草 + 上传参考合同 AI 生成）
   - 合同审查（AI 审核条款风险，结构化风险清单标注）
   - 合同管理（合同列表 + 收费节点 CRUD）
3. 环境解析（暂不实现，占位）
4. 概念构思（暂不实现，占位）
5. 平面构成（暂不实现，占位）
6. 空间构成（暂不实现，占位）

## 前端布局

- 左侧 64px 图标栏：顶部项目切换器（选择/新建/删除），6 个模块 SVG 图标 + 底部设置
- 点击图标切换主内容区，当前模块图标高亮
- 所有页面基于当前选中项目操作，状态持久化到 localStorage
- 高德地图 Key 在设置页配置（存 localStorage）

## API 契约约定

- 所有响应为 camelCase JSON（snake_case 字段经 Pydantic 别名自动转换）
- 分页统一返回 `{ list, total, page, pageSize }`，列表项内字段亦为 camelCase
- 错误统一返回 `{ code, message, detail, path }` 与对应 HTTP 状态码
- ID 均为自增整数（number）

## 快速开始

```bash
./scripts/setup.sh           # 创建 venv + 安装前后端依赖
./scripts/build_frontend.sh  # 构建前端到 backend/static
./scripts/run.sh             # 启动 uvicorn (0.0.0.0:8000)
# 浏览器访问 http://localhost:8000
```

## 测试

```bash
cd backend && python -m pytest tests/ -v   # 后端 26 个测试（API/工具/项目子项/联系单）
cd frontend && npm run type-check          # 前端类型检查
cd frontend && npm run build               # 前端构建
```

## 文档

- 架构设计：[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- 编码规范：[docs/CONVENTIONS.md](docs/CONVENTIONS.md)
