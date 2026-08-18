#!/usr/bin/env bash
# 初始化运行环境：创建 venv、安装后端依赖、安装前端依赖
# 与系统环境解耦，所有依赖装在项目内 .venv 与 frontend/node_modules
set -euo pipefail
PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$PROJECT_ROOT"

echo "[1/3] 创建 Python venv (.venv) ..."
python3 -m venv .venv
# shellcheck disable=SC1091
source .venv/bin/activate
pip install --upgrade pip
pip install -e backend

echo "[2/3] 安装前端依赖 (frontend/node_modules) ..."
cd frontend
npm install
cd "$PROJECT_ROOT"

echo "[3/3] 完成。"
echo "  - 构建前端:  ./scripts/build_frontend.sh"
echo "  - 启动服务:  ./scripts/run.sh"
echo "  - 访问:      http://localhost:8000"
