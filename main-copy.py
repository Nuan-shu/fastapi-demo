"""
Day 1 — FastAPI 三个核心概念
路由 / 请求体(Pydantic) / 自动文档(/docs)

启动:uvicorn main:app --reload
文档:http://localhost:8000/docs
"""

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="AI工程 Demo", version="0.1.0")

# ============================================================
# 概念 1：路由 (Route)
# URL 路径 → Python 函数，FastAPI 自动处理 HTTP 协议
# ============================================================

@app.get("/")                          # GET / → 首页
def home():
    return {"message": "AI 工程 Day 1 — FastAPI 核心"}

@app.get("/health")                    # GET /health → 健康检查
def health_check():
    return {"status": "ok"}

# ============================================================
# 概念 2：请求体 + Pydantic 自动校验
# 定义一个 Pydantic 模型 → FastAPI 自动校验请求格式
# ============================================================

class Question(BaseModel):
    content: str                       # 必填，必须是字符串
    model: str = "deepseek"            # 可选，默认 deepseek
    temperature: Optional[float] = 0.7 # 可选，默认 0.7

# 内存存储（模拟数据库）
history: list[dict] = []

@app.post("/ask")                      # POST /ask → AI 问答
def ask(question: Question):
    """
    接收一个问题，返回一个模拟的 AI 回答。

    试试在 /docs 里发送：
    {"content": "什么是 FastAPI？", "model": "deepseek", "temperature": 0.5}
    """
    # 模拟 AI 回答（Day 3-4 会接入真正的 LLM）
    reply = f"[模拟回答] 你问了：「{question.content}」\n模型：{question.model}，温度：{question.temperature}"

    # 存入历史
    history.append({
        "question": question.content,
        "answer": reply
    })

    return {
        "answer": reply,
        "model_used": question.model,
        "history_count": len(history)
    }

@app.get("/history")                   # GET /history → 查看历史
def get_history():
    """查看所有历史问答"""
    return {"count": len(history), "items": history}

@app.get("/ping")
def ping():
    return {"pong": True}