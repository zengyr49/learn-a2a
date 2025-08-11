@echo off
chcp 65001 >nul
echo 🚀 启动A2A协议演示项目...
echo ==================================

REM 检查Python版本
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 未找到Python，请先安装Python 3.8+
    pause
    exit /b 1
)

echo ✅ Python已安装

REM 检查依赖是否已安装
echo 📦 检查项目依赖...
python -c "import fastapi, uvicorn" >nul 2>&1
if %errorlevel% neq 0 (
    echo 📥 安装项目依赖...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo ❌ 依赖安装失败，请检查网络连接或手动安装
        pause
        exit /b 1
    )
) else (
    echo ✅ 项目依赖已安装
)

REM 启动服务器
echo 🌐 启动A2A协议服务器...
echo 📍 服务器地址: http://localhost:8000
echo 📱 演示客户端: python demo_client.py
echo ==================================
echo 按 Ctrl+C 停止服务器
echo.

python main.py
pause 