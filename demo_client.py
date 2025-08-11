#!/usr/bin/env python3
"""
A2A协议演示客户端
这个脚本展示了如何使用Python客户端与A2A协议服务器进行交互
"""

import requests
import json
import time
import uuid
from datetime import datetime
from typing import Dict, List

class A2AClient:
    """A2A协议客户端类"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.agent_id = None
        
    def register_agent(self, name: str, agent_type: str, capabilities: List[str]) -> bool:
        """注册AI代理"""
        agent_data = {
            "id": str(uuid.uuid4()),
            "name": name,
            "type": agent_type,
            "capabilities": capabilities,
            "status": "online",
            "created_at": datetime.now().isoformat()
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/agents/register",
                json=agent_data
            )
            
            if response.status_code == 200:
                self.agent_id = agent_data["id"]
                print(f"✅ 代理注册成功: {name} (ID: {self.agent_id})")
                return True
            else:
                print(f"❌ 代理注册失败: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ 注册请求失败: {e}")
            return False
    
    def get_all_agents(self) -> List[Dict]:
        """获取所有已注册的代理"""
        try:
            response = self.session.get(f"{self.base_url}/agents")
            if response.status_code == 200:
                return response.json()["agents"]
            else:
                print(f"❌ 获取代理列表失败: {response.text}")
                return []
        except Exception as e:
            print(f"❌ 请求失败: {e}")
            return []
    
    def send_message(self, receiver_id: str, content: str) -> bool:
        """发送消息给指定代理"""
        if not self.agent_id:
            print("❌ 请先注册代理")
            return False
            
        message_data = {
            "id": str(uuid.uuid4()),
            "sender_id": self.agent_id,
            "receiver_id": receiver_id,
            "content": content,
            "message_type": "text",
            "timestamp": datetime.now().isoformat(),
            "metadata": {}
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/messages/send",
                json=message_data
            )
            
            if response.status_code == 200:
                print(f"✅ 消息发送成功: {content[:50]}...")
                return True
            else:
                print(f"❌ 消息发送失败: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ 发送请求失败: {e}")
            return False
    
    def broadcast_message(self, content: str) -> bool:
        """广播消息给所有代理"""
        if not self.agent_id:
            print("❌ 请先注册代理")
            return False
            
        message_data = {
            "id": str(uuid.uuid4()),
            "sender_id": self.agent_id,
            "receiver_id": "broadcast",
            "content": content,
            "message_type": "text",
            "timestamp": datetime.now().isoformat(),
            "metadata": {}
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/messages/broadcast",
                json=message_data
            )
            
            if response.status_code == 200:
                print(f"✅ 广播消息发送成功: {content[:50]}...")
                return True
            else:
                print(f"❌ 广播消息发送失败: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ 广播请求失败: {e}")
            return False
    
    def get_messages(self, agent_id: str = None) -> List[Dict]:
        """获取代理的消息历史"""
        target_id = agent_id or self.agent_id
        if not target_id:
            print("❌ 请先注册代理或指定代理ID")
            return []
            
        try:
            response = self.session.get(f"{self.base_url}/agents/{target_id}/messages")
            if response.status_code == 200:
                return response.json()["messages"]
            else:
                print(f"❌ 获取消息失败: {response.text}")
                return []
        except Exception as e:
            print(f"❌ 请求失败: {e}")
            return []

def demo_basic_operations():
    """演示基本操作"""
    print("🚀 开始A2A协议基本操作演示...\n")
    
    # 创建客户端
    client = A2AClient()
    
    # 1. 注册多个代理
    print("📋 步骤1: 注册AI代理")
    print("-" * 50)
    
    agents_data = [
        {
            "name": "智能助手Alice",
            "type": "assistant",
            "capabilities": ["自然语言处理", "问答", "翻译"]
        },
        {
            "name": "数据分析师Bob",
            "type": "specialist",
            "capabilities": ["数据分析", "统计建模", "可视化"]
        },
        {
            "name": "项目协调员Charlie",
            "type": "coordinator",
            "type": "coordinator",
            "capabilities": ["项目管理", "任务分配", "进度跟踪"]
        }
    ]
    
    registered_agents = []
    for agent_info in agents_data:
        if client.register_agent(**agent_info):
            registered_agents.append(client.agent_id)
            time.sleep(0.5)  # 避免请求过快
    
    print(f"\n✅ 成功注册 {len(registered_agents)} 个代理\n")
    
    # 2. 查看所有代理
    print("📋 步骤2: 查看所有已注册的代理")
    print("-" * 50)
    
    all_agents = client.get_all_agents()
    for agent in all_agents:
        print(f"🤖 {agent['name']} ({agent['type']})")
        print(f"   ID: {agent['id']}")
        print(f"   能力: {', '.join(agent['capabilities'])}")
        print(f"   状态: {agent['status']}")
        print()
    
    # 3. 发送点对点消息
    print("📋 步骤3: 发送点对点消息")
    print("-" * 50)
    
    if len(registered_agents) >= 2:
        # Alice给Bob发送消息
        client.agent_id = registered_agents[0]  # Alice
        client.send_message(
            registered_agents[1],  # Bob
            "你好Bob！我需要分析一些数据，你能帮助我吗？"
        )
        
        time.sleep(1)
        
        # Bob给Alice回复
        client.agent_id = registered_agents[1]  # Bob
        client.send_message(
            registered_agents[0],  # Alice
            "当然可以！请告诉我你需要分析什么类型的数据？"
        )
    
    # 4. 广播消息
    print("\n📋 步骤4: 广播消息")
    print("-" * 50)
    
    client.agent_id = registered_agents[2]  # Charlie
    client.broadcast_message(
        "大家好！我是项目协调员Charlie。我们有一个新项目需要大家协作完成。"
    )
    
    # 5. 查看消息历史
    print("\n📋 步骤5: 查看消息历史")
    print("-" * 50)
    
    for i, agent_id in enumerate(registered_agents):
        agent_name = agents_data[i]["name"]
        print(f"\n📬 {agent_name} 的消息历史:")
        
        messages = client.get_messages(agent_id)
        if messages:
            for msg in messages:
                sender_name = next((a["name"] for a in all_agents if a["id"] == msg["sender_id"]), msg["sender_id"])
                receiver_name = next((a["name"] for a in all_agents if a["id"] == msg["receiver_id"]), msg["receiver_id"])
                
                print(f"  📤 {sender_name} → {receiver_name}: {msg['content']}")
                print(f"     时间: {msg['timestamp']}")
        else:
            print("  暂无消息")
    
    print("\n🎉 基本操作演示完成！")

def demo_advanced_features():
    """演示高级功能"""
    print("\n🚀 开始A2A协议高级功能演示...\n")
    
    client = A2AClient()
    
    # 注册一个研究型代理
    print("📋 注册研究型代理")
    print("-" * 50)
    
    if client.register_agent(
        name="研究员David",
        agent_type="researcher",
        capabilities=["文献检索", "实验设计", "结果分析", "论文写作"]
    ):
        print("✅ 研究型代理注册成功")
        
        # 模拟复杂的协作场景
        print("\n📋 模拟复杂协作场景")
        print("-" * 50)
        
        # 1. 发送结构化消息
        structured_message = {
            "task": "研究项目协作",
            "requirements": ["文献综述", "实验设计", "数据分析"],
            "deadline": "2024-12-31",
            "collaborators": ["智能助手Alice", "数据分析师Bob"]
        }
        
        client.send_message(
            "broadcast",
            f"新研究项目启动！详情：{json.dumps(structured_message, ensure_ascii=False)}"
        )
        
        # 2. 模拟任务分配
        time.sleep(1)
        client.send_message(
            "broadcast",
            "任务分配：Alice负责文献综述，Bob负责数据分析，David负责实验设计"
        )
        
        # 3. 模拟进度更新
        time.sleep(1)
        client.send_message(
            "broadcast",
            "进度更新：文献综述完成30%，数据分析完成50%，实验设计完成80%"
        )
    
    print("\n🎉 高级功能演示完成！")

if __name__ == "__main__":
    print("=" * 60)
    print("🤖 A2A协议演示客户端")
    print("=" * 60)
    print("这个演示将展示A2A协议的核心功能：")
    print("• 代理注册和管理")
    print("• 点对点消息通信")
    print("• 广播消息")
    print("• 消息历史查询")
    print("• 复杂协作场景")
    print("=" * 60)
    
    try:
        # 检查服务器是否运行
        response = requests.get("http://localhost:8000/agents", timeout=5)
        if response.status_code == 200:
            print("✅ 服务器连接正常，开始演示...\n")
            
            # 运行演示
            demo_basic_operations()
            demo_advanced_features()
            
            print("\n" + "=" * 60)
            print("🎯 演示总结")
            print("=" * 60)
            print("通过这个演示，您了解了：")
            print("1. A2A协议如何实现AI代理间的标准化通信")
            print("2. 代理注册、发现和管理的机制")
            print("3. 点对点和广播两种通信模式")
            print("4. 实时消息传递和历史记录查询")
            print("5. 多代理协作的典型应用场景")
            print("\n💡 提示：您可以打开浏览器访问 http://localhost:8000 查看Web界面")
            
        else:
            print("❌ 服务器响应异常，请检查服务器状态")
            
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到服务器，请确保服务器正在运行")
        print("💡 启动服务器命令：python main.py")
        
    except Exception as e:
        print(f"❌ 演示过程中出现错误：{e}") 