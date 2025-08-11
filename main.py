from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
import json
import asyncio
from typing import Dict, List, Optional
from pydantic import BaseModel
import uuid
from datetime import datetime

app = FastAPI(title="A2A协议演示项目", description="AI代理间通信协议演示")

# 挂载静态文件
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# 数据模型
class Agent(BaseModel):
    id: str
    name: str
    type: str
    capabilities: List[str]
    status: str = "online"
    created_at: datetime

class Message(BaseModel):
    id: str
    sender_id: str
    receiver_id: str
    content: str
    message_type: str = "text"
    timestamp: datetime
    metadata: Optional[Dict] = None

class A2AProtocol:
    """A2A协议实现类"""
    
    def __init__(self):
        self.agents: Dict[str, Agent] = {}
        self.messages: List[Message] = []
        self.connections: Dict[str, WebSocket] = {}
        
    async def register_agent(self, agent: Agent) -> bool:
        """注册AI代理"""
        if agent.id in self.agents:
            return False
        self.agents[agent.id] = agent
        return True
    
    async def unregister_agent(self, agent_id: str) -> bool:
        """注销AI代理"""
        if agent_id in self.agents:
            del self.agents[agent_id]
            if agent_id in self.connections:
                del self.connections[agent_id]
            return True
        return False
    
    async def send_message(self, message: Message) -> bool:
        """发送消息"""
        # 验证发送者和接收者
        if message.sender_id not in self.agents or message.receiver_id not in self.agents:
            return False
        
        # 存储消息
        self.messages.append(message)
        
        # 如果接收者在线，实时推送消息
        if message.receiver_id in self.connections:
            try:
                await self.connections[message.receiver_id].send_text(
                    json.dumps({
                        "type": "message",
                        "data": message.dict()
                    })
                )
            except:
                pass
        
        return True
    
    async def broadcast_message(self, message: Message) -> bool:
        """广播消息给所有代理"""
        message.receiver_id = "broadcast"
        self.messages.append(message)
        
        # 推送给所有连接的代理
        for connection in self.connections.values():
            try:
                await connection.send_text(
                    json.dumps({
                        "type": "broadcast",
                        "data": message.dict()
                    })
                )
            except:
                pass
        
        return True
    
    def get_agent_info(self, agent_id: str) -> Optional[Agent]:
        """获取代理信息"""
        return self.agents.get(agent_id)
    
    def get_all_agents(self) -> List[Agent]:
        """获取所有代理"""
        return list(self.agents.values())
    
    def get_agent_messages(self, agent_id: str) -> List[Message]:
        """获取代理的消息历史"""
        return [msg for msg in self.messages if msg.sender_id == agent_id or msg.receiver_id == agent_id]

# 全局A2A协议实例
a2a_protocol = A2AProtocol()

# 路由
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """主页"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/agents")
async def get_agents():
    """获取所有代理"""
    return {"agents": a2a_protocol.get_all_agents()}

@app.post("/agents/register")
async def register_agent(agent: Agent):
    """注册新代理"""
    success = await a2a_protocol.register_agent(agent)
    if success:
        return {"message": "代理注册成功", "agent": agent}
    else:
        raise HTTPException(status_code=400, detail="代理ID已存在")

@app.post("/agents/{agent_id}/unregister")
async def unregister_agent(agent_id: str):
    """注销代理"""
    success = await a2a_protocol.unregister_agent(agent_id)
    if success:
        return {"message": "代理注销成功"}
    else:
        raise HTTPException(status_code=404, detail="代理不存在")

@app.post("/messages/send")
async def send_message(message: Message):
    """发送消息"""
    success = await a2a_protocol.send_message(message)
    if success:
        return {"message": "消息发送成功", "message_id": message.id}
    else:
        raise HTTPException(status_code=400, detail="消息发送失败")

@app.post("/messages/broadcast")
async def broadcast_message(message: Message):
    """广播消息"""
    success = await a2a_protocol.broadcast_message(message)
    if success:
        return {"message": "消息广播成功", "message_id": message.id}
    else:
        raise HTTPException(status_code=400, detail="消息广播失败")

@app.get("/agents/{agent_id}/messages")
async def get_agent_messages(agent_id: str):
    """获取代理的消息历史"""
    messages = a2a_protocol.get_agent_messages(agent_id)
    return {"messages": messages}

@app.websocket("/ws/{agent_id}")
async def websocket_endpoint(websocket: WebSocket, agent_id: str):
    """WebSocket连接端点"""
    await websocket.accept()
    
    # 验证代理是否存在
    if agent_id not in a2a_protocol.agents:
        await websocket.close(code=4004, reason="代理不存在")
        return
    
    # 建立连接
    a2a_protocol.connections[agent_id] = websocket
    
    try:
        # 发送连接成功消息
        await websocket.send_text(json.dumps({
            "type": "connection",
            "message": "连接成功",
            "agent_id": agent_id
        }))
        
        # 保持连接并处理消息
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            # 处理接收到的消息
            if message_data.get("type") == "message":
                message = Message(**message_data["data"])
                await a2a_protocol.send_message(message)
                
    except WebSocketDisconnect:
        # 连接断开，清理资源
        if agent_id in a2a_protocol.connections:
            del a2a_protocol.connections[agent_id]
    except Exception as e:
        print(f"WebSocket错误: {e}")
        if agent_id in a2a_protocol.connections:
            del a2a_protocol.connections[agent_id]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 