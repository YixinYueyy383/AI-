#!/bin/bash

# AI Editorial Layout Agent 启动脚本

echo "🎨 AI Editorial Layout Agent"
echo "=============================="
echo ""

# 检查Python版本
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python版本: $python_version"

# 检查依赖
if ! python3 -c "import streamlit" 2>/dev/null; then
    echo "正在安装依赖..."
    pip3 install -r requirements.txt
fi

echo ""
echo "启动应用程序..."
echo ""

# 启动Streamlit
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
