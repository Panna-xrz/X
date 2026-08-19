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

整体为「顶栏 + 中栏[左|主|右] + 底栏」结构：

- **顶栏 TopBar（40px）**：软件图标（建筑剪影）+ 名称 ArchSuite + 当前项目切换入口 + 布局开关（左/右/底三栏显隐）
- **左侧 64px 图标栏 IconBar**：项目入口 + 6 个模块 SVG 图标 + 底部设置
- **主内容区**：路由视图，带 12/16px 内边距，卡片化不贴边
- **右侧 Panna AI 助手（360px，可折叠）**：聊天 / RAG / Agent / Panna 四种模式，后端待接入
- **底栏 BottomBar（24px）**：连接状态 + 当前项目 + 日志条数，点击从底部滑出抽屉（日志 / 项目更新记录 / 连接状态三个 Tab）
- 布局显隐由 `stores/layout.ts` 管理，持久化到 localStorage
- 全局快捷键：`Ctrl+K` 项目管理、`Ctrl+B` 左栏、`Ctrl+J` 底栏、`Ctrl+/` 右栏、`Ctrl+,` 设置
- 主题系统：4 层背景（page/card/panel/inset）+ 4 种字号（xs/sm/base/lg）+ 单字体族，无分割线靠层次分层，全部在设置面板可调

## 设置面板

8 个类别（两列卡片布局）：基本 / 界面 / API-Key / 运行时 / 导入导出 / 快捷键 / 关于 / 清理

- **基本**：默认项目阶段、自动保存间隔、数据刷新间隔（调度器在 AppLayout 接管）
- **界面**：深色模式、主色调、字体族、4 层背景色、4 种字号、圆角、紧凑度、内容区宽度（实时生效）
- **API-Key**：高德地图 Key + 安全密钥（securityJsCode，2021-12-02 后申请的 Key 必填）+ LLM 提供商/Key/BaseURL/模型（含真实连接测试）
- **运行时**：请求超时（→axios）、AI 请求超时（→AI 接口）、日志级别（→前端 logger，影响底栏日志抽屉）
- **导入导出**：设置 JSON 导出/导入
- **快捷键**：全局快捷键速查
- **关于** / **清理**：应用信息 / 缓存与项目数据清理

## 场地周边功能

- 高德地图选点（点击/拖拽标记）+ 关键词搜索定位（PlaceSearch）
- 经纬度 + CGCS2000 3 度带 XY 联动显示（自动按经度选中央子午线）
- 用地红线放线：粘贴/上传 CSV/TSV/TXT 坐标表 → 解析 → 高斯反算为经纬度 → 地图绘制多边形并自适应视野
- 坐标换算工具：`utils/coord.ts`（高斯-克吕格 3 度带正反算 + 红线表解析）

## API 契约约定

- 所有响应为 camelCase JSON（snake_case 字段经 Pydantic 别名自动转换）
- 分页统一返回 `{ list, total, page, pageSize }`，列表项内字段亦为 camelCase
- 错误统一返回 `{ code, message, detail, path }` 与对应 HTTP 状态码
- ID 均为自增整数（number）

## 快速开始

```bash
./scripts/setup.sh           # 创建 venv + 安装前后端依赖
./scripts/build_frontend.sh  # 构建前端到 backend/static
./scripts/run.sh             # 启动 uvicorn (0.0.0.0:9099)
# 浏览器访问 http://localhost:9099
```

> 后端在 `/` 直接托管 SPA（`frontend/dist/index.html`），需先 `cd frontend && npm run build` 生成构建产物。`GET /` 返回 404 通常因 dist 缺失。

## 测试

```bash
cd backend && python -m pytest tests/ -v   # 后端 26 个测试（API/工具/项目子项/联系单）
cd frontend && npm run type-check          # 前端类型检查
cd frontend && npm run build               # 前端构建
```

## 文档

- 架构设计：[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- 编码规范：[docs/CONVENTIONS.md](docs/CONVENTIONS.md)
