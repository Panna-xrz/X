#!/usr/bin/env bash
# 构建前端静态资源并复制到后端静态托管目录
set -euo pipefail
PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$PROJECT_ROOT"

echo "[1/2] 构建前端 (frontend/dist) ..."
cd frontend
npm run build
cd "$PROJECT_ROOT"

echo "[2/2] 复制到 backend/static ..."
mkdir -p backend/static
rm -rf backend/static/*
cp -r frontend/dist/* backend/static/

echo "完成。启动 ./scripts/run.sh 后访问 http://localhost:8000"
