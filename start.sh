#!/bin/bash

echo "🚀 启动A2A协议演示项目..."
echo "=================================="

# 检查Python版本
python_version=$(python3 --version 2>&1)
if [[ $? -eq 0 ]]; then
    echo "✅ Python版本: $python_version"
else
    echo "❌ 未找到Python3，请先安装Python 3.8+"
    exit 1
fi

# 检查依赖是否已安装
echo "📦 检查项目依赖..."
if ! python3 -c "import fastapi, uvicorn" 2>/dev/null; then
    echo "📥 安装项目依赖..."
    pip3 install -r requirements.txt
    if [[ $? -ne 0 ]]; then
        echo "❌ 依赖安装失败，请检查网络连接或手动安装"
        exit 1
    fi
else
    echo "✅ 项目依赖已安装"
fi

# 启动服务器
echo "🌐 启动A2A协议服务器..."
echo "📍 服务器地址: http://localhost:8000"
echo "📱 演示客户端: python3 demo_client.py"
echo "=================================="
echo "按 Ctrl+C 停止服务器"
echo ""

python3 main.py 