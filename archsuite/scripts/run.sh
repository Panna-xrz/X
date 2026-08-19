#!/usr/bin/env bash
# 启动后端服务（FastAPI + uvicorn），并托管前端静态资源
# 与系统环境解耦：始终使用项目内 .venv
set -euo pipefail
PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$PROJECT_ROOT"

# shellcheck disable=SC1091
source .venv/bin/activate

cd backend
exec uvicorn app.main:app --host 0.0.0.0 --port 9099 --reload
