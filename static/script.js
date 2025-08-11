// 全局变量
let websocket = null;
let currentAgentId = null;

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    loadAgents();
    loadMessages();
    updateAgentSelects();
});

// 生成唯一ID
function generateId() {
    return 'id_' + Math.random().toString(36).substr(2, 9);
}

// 格式化时间
function formatTime(timestamp) {
    const date = new Date(timestamp);
    return date.toLocaleString('zh-CN');
}

// 注册代理
async function registerAgent() {
    const name = document.getElementById('agentName').value.trim();
    const type = document.getElementById('agentType').value;
    const capabilities = document.getElementById('agentCapabilities').value.trim();
    
    if (!name) {
        alert('请输入代理名称');
        return;
    }
    
    const agent = {
        id: generateId(),
        name: name,
        type: type,
        capabilities: capabilities ? capabilities.split(',').map(c => c.trim()) : [],
        status: 'online',
        created_at: new Date().toISOString()
    };
    
    try {
        const response = await fetch('/agents/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(agent)
        });
        
        if (response.ok) {
            alert('代理注册成功！');
            document.getElementById('agentName').value = '';
            document.getElementById('agentCapabilities').value = '';
            loadAgents();
            updateAgentSelects();
        } else {
            const error = await response.json();
            alert('注册失败：' + error.detail);
        }
    } catch (error) {
        alert('注册失败：' + error.message);
    }
}

// 加载代理列表
async function loadAgents() {
    try {
        const response = await fetch('/agents');
        const data = await response.json();
        displayAgents(data.agents);
    } catch (error) {
        console.error('加载代理失败：', error);
    }
}

// 显示代理列表
function displayAgents(agents) {
    const agentsList = document.getElementById('agentsList');
    
    if (agents.length === 0) {
        agentsList.innerHTML = '<p>暂无注册的代理</p>';
        return;
    }
    
    agentsList.innerHTML = agents.map(agent => `
        <div class="agent-item">
            <h4>${agent.name}</h4>
            <p><strong>ID:</strong> ${agent.id}</p>
            <p><strong>类型:</strong> ${agent.type}</p>
            <p><strong>状态:</strong> ${agent.status}</p>
            <p><strong>创建时间:</strong> ${formatTime(agent.created_at)}</p>
            <div class="capabilities">
                ${agent.capabilities.map(cap => `<span class="capability-tag">${cap}</span>`).join('')}
            </div>
        </div>
    `).join('');
}

// 更新代理选择下拉框
function updateAgentSelects() {
    loadAgents().then(() => {
        fetch('/agents')
            .then(response => response.json())
            .then(data => {
                const agents = data.agents;
                const senderSelect = document.getElementById('senderAgent');
                const receiverSelect = document.getElementById('receiverAgent');
                const connectSelect = document.getElementById('connectAgent');
                
                // 清空现有选项
                senderSelect.innerHTML = '<option value="">选择发送者</option>';
                receiverSelect.innerHTML = '<option value="">选择接收者</option>';
                connectSelect.innerHTML = '<option value="">选择要连接的代理</option>';
                
                // 添加代理选项
                agents.forEach(agent => {
                    const option = `<option value="${agent.id}">${agent.name} (${agent.type})</option>`;
                    senderSelect.innerHTML += option;
                    receiverSelect.innerHTML += option;
                    connectSelect.innerHTML += option;
                });
            });
    });
}

// 发送消息
async function sendMessage() {
    const senderId = document.getElementById('senderAgent').value;
    const receiverId = document.getElementById('receiverAgent').value;
    const content = document.getElementById('messageContent').value.trim();
    
    if (!senderId || !receiverId || !content) {
        alert('请填写完整的消息信息');
        return;
    }
    
    const message = {
        id: generateId(),
        sender_id: senderId,
        receiver_id: receiverId,
        content: content,
        message_type: 'text',
        timestamp: new Date().toISOString(),
        metadata: {}
    };
    
    try {
        let response;
        if (receiverId === 'broadcast') {
            response = await fetch('/messages/broadcast', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(message)
            });
        } else {
            response = await fetch('/messages/send', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(message)
            });
        }
        
        if (response.ok) {
            alert('消息发送成功！');
            document.getElementById('messageContent').value = '';
            loadMessages();
        } else {
            const error = await response.json();
            alert('发送失败：' + error.detail);
        }
    } catch (error) {
        alert('发送失败：' + error.message);
    }
}

// 加载消息历史
async function loadMessages() {
    try {
        // 这里简化处理，实际项目中可能需要分页或其他策略
        const response = await fetch('/agents');
        const agentsData = await response.json();
        
        if (agentsData.agents.length > 0) {
            const firstAgent = agentsData.agents[0];
            const messagesResponse = await fetch(`/agents/${firstAgent.id}/messages`);
            const messagesData = await messagesResponse.json();
            displayMessages(messagesData.messages);
        }
    } catch (error) {
        console.error('加载消息失败：', error);
    }
}

// 显示消息列表
function displayMessages(messages) {
    const messagesList = document.getElementById('messagesList');
    
    if (messages.length === 0) {
        messagesList.innerHTML = '<p>暂无消息记录</p>';
        return;
    }
    
    messagesList.innerHTML = messages.map(message => `
        <div class="message-item">
            <div class="message-header">
                <span><strong>从:</strong> ${message.sender_id}</span>
                <span><strong>到:</strong> ${message.receiver_id}</span>
                <span><strong>时间:</strong> ${formatTime(message.timestamp)}</span>
            </div>
            <div class="message-content">${message.content}</div>
        </div>
    `).join('');
}

// 建立WebSocket连接
function connectWebSocket() {
    const agentId = document.getElementById('connectAgent').value;
    
    if (!agentId) {
        alert('请选择要连接的代理');
        return;
    }
    
    if (websocket && websocket.readyState === WebSocket.OPEN) {
        alert('已经存在连接，请先断开');
        return;
    }
    
    try {
        const wsUrl = `ws://${window.location.host}/ws/${agentId}`;
        websocket = new WebSocket(wsUrl);
        currentAgentId = agentId;
        
        websocket.onopen = function(event) {
            console.log('WebSocket连接已建立');
            updateConnectionStatus('connected', '已连接');
        };
        
        websocket.onmessage = function(event) {
            const data = JSON.parse(event.data);
            handleWebSocketMessage(data);
        };
        
        websocket.onclose = function(event) {
            console.log('WebSocket连接已关闭');
            updateConnectionStatus('disconnected', '连接已断开');
            websocket = null;
            currentAgentId = null;
        };
        
        websocket.onerror = function(error) {
            console.error('WebSocket错误：', error);
            updateConnectionStatus('disconnected', '连接错误');
        };
        
    } catch (error) {
        alert('连接失败：' + error.message);
    }
}

// 断开WebSocket连接
function disconnectWebSocket() {
    if (websocket) {
        websocket.close();
        websocket = null;
        currentAgentId = null;
        updateConnectionStatus('disconnected', '未连接');
    }
}

// 处理WebSocket消息
function handleWebSocketMessage(data) {
    console.log('收到WebSocket消息：', data);
    
    switch (data.type) {
        case 'connection':
            console.log('连接状态：', data.message);
            break;
        case 'message':
            console.log('收到消息：', data.data);
            // 可以在这里更新UI显示新消息
            break;
        case 'broadcast':
            console.log('收到广播：', data.data);
            // 可以在这里更新UI显示广播消息
            break;
        default:
            console.log('未知消息类型：', data);
    }
}

// 更新连接状态显示
function updateConnectionStatus(status, message) {
    const statusElement = document.getElementById('connectionStatus');
    statusElement.textContent = message;
    statusElement.className = status;
}

// 发送WebSocket消息
function sendWebSocketMessage(message) {
    if (websocket && websocket.readyState === WebSocket.OPEN) {
        websocket.send(JSON.stringify({
            type: 'message',
            data: message
        }));
    } else {
        alert('WebSocket未连接');
    }
}

// 页面卸载时清理连接
window.addEventListener('beforeunload', function() {
    if (websocket) {
        websocket.close();
    }
}); 