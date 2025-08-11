# 🤖 A2A协议演示项目

## 📖 项目简介

这是一个完整的A2A（Agent-to-Agent）协议演示项目，旨在帮助新手了解AI代理间通信协议的核心概念和实现方式。A2A协议是AI领域的新兴技术，允许多个AI代理之间进行标准化通信和协作。

## 🎯 什么是A2A协议？

A2A（Agent-to-Agent）协议是一种专门为AI代理间通信设计的标准化协议，它解决了以下关键问题：

- **标准化通信**：统一的消息格式和协议规范
- **能力发现**：代理可以声明和发现彼此的能力
- **实时协作**：支持WebSocket实时通信
- **灵活路由**：支持点对点和广播通信模式
- **可扩展性**：易于集成新的代理类型和功能

## 🚀 核心特性

### 1. 代理管理系统
- 代理注册和注销
- 能力声明和发现
- 状态监控和管理

### 2. 通信协议
- 点对点消息传递
- 广播消息系统
- 消息历史记录
- 实时WebSocket连接

### 3. 协作机制
- 多代理任务分配
- 进度跟踪和更新
- 结构化消息支持

## 🛠️ 技术架构

```
┌─────────────────┐    HTTP/WebSocket    ┌─────────────────┐
│   前端界面      │ ←──────────────────→ │   A2A协议服务器  │
│  (HTML/CSS/JS) │                      │   (FastAPI)      │
└─────────────────┘                      └─────────────────┘
                                                    │
                                                    ▼
                                         ┌─────────────────┘
                                         │   数据存储      │
                                         │  (内存存储)     │
                                         └─────────────────┘
```

### 技术栈
- **后端**: FastAPI + Python 3.8+
- **前端**: HTML5 + CSS3 + JavaScript (ES6+)
- **通信**: HTTP REST API + WebSocket
- **数据模型**: Pydantic
- **样式**: 现代化CSS Grid + Flexbox

## 📦 安装和运行

### 环境要求
- Python 3.8 或更高版本
- 现代浏览器（支持ES6和WebSocket）

### 1. 克隆项目
```bash
git clone <项目地址>
cd learnA2A
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 启动服务器
```bash
python main.py
```

### 4. 访问应用
打开浏览器访问：http://localhost:8000

## 🎮 使用方法

### 1. 代理管理
- **注册代理**: 填写代理名称、类型和能力描述
- **查看代理**: 浏览所有已注册的AI代理
- **代理类型**: 助手型、专业型、协调型、研究型

### 2. 消息通信
- **点对点通信**: 选择发送者和接收者，发送私密消息
- **广播消息**: 向所有代理发送公共消息
- **消息历史**: 查看代理的通信记录

### 3. 实时连接
- **WebSocket连接**: 建立实时通信连接
- **连接状态**: 监控代理的在线状态
- **实时消息**: 接收即时推送的消息

## 🔧 API接口

### 代理管理
```
POST /agents/register          # 注册新代理
GET  /agents                  # 获取所有代理
POST /agents/{id}/unregister  # 注销代理
```

### 消息通信
```
POST /messages/send           # 发送点对点消息
POST /messages/broadcast      # 广播消息
GET  /agents/{id}/messages    # 获取代理消息历史
```

### WebSocket
```
WS /ws/{agent_id}            # 建立WebSocket连接
```

## 📱 演示脚本

项目包含一个完整的Python演示客户端，展示A2A协议的各种功能：

```bash
python demo_client.py
```

演示内容包括：
- 多代理注册和管理
- 点对点消息通信
- 广播消息系统
- 复杂协作场景模拟

## 🌟 学习要点

### 1. 协议设计原则
- **标准化**: 统一的消息格式和接口规范
- **可扩展性**: 支持新的代理类型和功能
- **互操作性**: 不同系统间的无缝协作

### 2. 通信模式
- **同步通信**: HTTP REST API
- **异步通信**: WebSocket实时连接
- **消息路由**: 智能的消息分发机制

### 3. 协作机制
- **能力发现**: 代理间的能力匹配
- **任务分配**: 基于能力的智能分配
- **进度同步**: 实时状态更新和监控

## 🔍 实际应用场景

### 1. 多AI系统协作
- 不同AI服务间的任务协调
- 分布式AI任务处理
- 智能工作流自动化

### 2. 企业级应用
- 智能客服系统
- 数据分析平台
- 项目管理工具

### 3. 研究领域
- 多智能体系统研究
- 分布式AI算法测试
- 协作学习实验

## 🚧 扩展开发

### 1. 添加新的代理类型
```python
class CustomAgent(Agent):
    custom_field: str
    custom_method: Callable
```

### 2. 实现新的通信协议
```python
class CustomProtocol(A2AProtocol):
    async def custom_operation(self):
        # 自定义操作逻辑
        pass
```

### 3. 集成外部AI服务
- OpenAI GPT API
- Google PaLM API
- 本地大语言模型

## 📚 学习资源

### 相关概念
- **多智能体系统** (Multi-Agent Systems)
- **分布式AI** (Distributed AI)
- **智能体通信协议** (Agent Communication Protocols)
- **WebSocket实时通信**
- **RESTful API设计**

### 进阶学习
- 研究现有的A2A协议标准
- 学习分布式系统设计
- 了解微服务架构
- 探索AI编排技术

## 🤝 贡献指南

欢迎贡献代码和改进建议！

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 发起 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 🆘 常见问题

### Q: 服务器启动失败怎么办？
A: 检查端口8000是否被占用，或修改main.py中的端口号

### Q: WebSocket连接失败？
A: 确保代理已注册，且服务器正在运行

### Q: 如何添加新的代理类型？
A: 修改HTML模板中的select选项，并在后端添加相应的处理逻辑

### Q: 可以持久化存储数据吗？
A: 当前使用内存存储，可以集成数据库（如SQLite、PostgreSQL）

## 📞 联系方式

如有问题或建议，请通过以下方式联系：
- 项目Issues: [GitHub Issues](https://github.com/zengyr49/learn-a2a/issues)
- 邮箱: [595438103@qq.com]

---

**🎉 祝您学习愉快！通过这个项目，您将深入了解AI代理协作的未来技术。** 