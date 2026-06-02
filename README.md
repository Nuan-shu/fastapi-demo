# FastAPI + Streamlit 前后端骨架

AI 工程学习项目 — 从零手写的一个完整前后端 Demo。

## 做了什么

浏览器输入问题 → Streamlit 发请求 → FastAPI 处理 → 返回答案 → 页面显示。

```
浏览器                 Streamlit               FastAPI
  │  打字 + 点按钮        │                       │
  │─────────────────────>│  POST /ask             │
  │                      │  {"content":"..."}     │
  │                      │──────────────────────>│
  │                      │              Pydantic 校验
  │                      │  {"answer":"..."}      │
  │                      │<──────────────────────│
  │  显示答案             │                       │
  │<─────────────────────│                       │
```

## 技术栈

| 层 | 技术 | 作用 |
|----|------|------|
| 前端 | Streamlit | 输入框 + 按钮 + 显示答案 |
| 后端 | FastAPI | 路由 + 数据校验 + 业务逻辑 |
| 校验 | Pydantic | 自动校验请求体格式 |

## 项目结构

```
fastapi-demo/
├── main.py              # FastAPI 后端（GET /、POST /ask）
├── app.py               # Streamlit 前端
├── main_annotated.py    # 逐行注释版
├── pydantic_demo.py     # Pydantic 复习脚本
└── .gitignore
```

## 快速开始

```bash
# 1. 启动后端
cd fastapi-demo
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000

# 2. 新终端，启动前端
cd fastapi-demo
python3 -m streamlit run app.py --server.port 8501

# 3. 浏览器打开 http://localhost:8501
```

## API

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | / | 首页 |
| GET | /health | 健康检查 |
| POST | /ask | 提问（body: {"content":"...", "model":"deepseek"}） |

## 学习日志

- Day 1 (6/1)：FastAPI 核心 — 路由、Pydantic 校验、/docs 文档
- Day 2 (6/2)：Streamlit 核心 — 前后端打通、session_state 持久化
