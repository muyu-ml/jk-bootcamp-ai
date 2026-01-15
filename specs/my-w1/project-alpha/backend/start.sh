#!/bin/bash

# 获取脚本所在目录的绝对路径
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
# 项目根目录（backend 的父目录的父目录的父目录）
PROJECT_ROOT="$( cd "$SCRIPT_DIR/../../.." && pwd )"

# 激活虚拟环境
source "$PROJECT_ROOT/venv/bin/activate"

# 切换到 backend 目录
cd "$SCRIPT_DIR"

# 运行 uvicorn
uvicorn app.main:app --reload
