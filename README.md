# FastAPI + Streamlit + RAG — AI 工程学习项目

从零手写的 AI 应用工程学习项目。三天内从后端骨架到 RAG 全链路闭环——前端展示、后端服务、向量检索、LLM 生成，一条命令全部跑通。

## 项目概览

```
用户 → Streamlit 界面 → POST /ask → FastAPI → RAG 引擎 → 答案

RAG 引擎内部：
  文档 → chroma_demo（分块入库）→ 向量检索 → 拼 Prompt → DeepSeek → 答案
```

## 技术栈

| 层 | 技术 | 作用 |
|----|------|------|
| 前端 | Streamlit | 输入框 + 按钮 + 文件上传 + 答案展示 |
| 后端 | FastAPI | 路由 + Pydantic 数据校验 |
| 向量库 | ChromaDB | 文档存储 + 语义检索 |
| Embedding | bge-small-zh-v1.5 | 中文文本转向量（通过 hf-mirror 镜像） |
| LLM | DeepSeek API | 根据检索结果生成答案 |

## 项目结构：7 个学习节点

```
fastapi-demo/
├── main.py              # 节点1：FastAPI 后端（GET /、POST /ask）
├── pydantic_demo.py     # 节点2：Pydantic 自动校验演示
├── app.py               # 节点3：Streamlit 前端（输入框+按钮+答案）
├── chroma_demo.py       # 节点4：ChromaDB（建库/插入/语义搜索）
├── chunking_demo.py     # 节点5：文本分块（chunk_size + overlap）
├── rag_demo.py          # 节点6：RAG 原型（检索 + Prompt 拼装）
├── rag_demo_2.py        # 节点7：RAG 闭环（bge 中文嵌入 + DeepSeek 生成）
├── main_annotated.py    # FastAPI 逐行注释版
└── .gitignore
```

详尽的节点说明见 `Wiki/06.AI工程 AI-Engineering/05.FastAPI-Demo学习节点全览.md`

## 快速开始

```bash
# 1. 安装依赖
pip3 install fastapi uvicorn streamlit chromadb sentence-transformers openai

# 2. 设 API Key
export DEEPSEEK_API_KEY="sk-xxx"

# 3. 启动后端
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000

# 4. 新终端，启动前端
python3 -m streamlit run app.py --server.port 8501

# 5. 浏览器打开 http://localhost:8501

# 6. 直接跑 RAG 全链路（不依赖服务）
python3 rag_demo_2.py
```

## 各节点快速体验

```bash
# 数据校验
python3 pydantic_demo.py

# 向量搜索
python3 chroma_demo.py

# 文本分块
python3 chunking_demo.py

# RAG 原型
python3 rag_demo.py

# RAG 闭环
export DEEPSEEK_API_KEY="sk-xxx"
python3 rag_demo_2.py
```

## API

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /health | 健康检查 |
| POST | /ask | 提问（body: `{"content":"..."}`） |

交互式文档：`http://localhost:8000/docs`

## 学习日志

| 日期 | Tag | 内容 |
|------|-----|------|
| Day 1 (6/1) | v0.0.1 | FastAPI 后端 — 路由、Pydantic 校验、/docs 文档 |
| Day 2 (6/2) | — | Streamlit 前端 — 前后端打通、session_state、GitHub 上线 |
| Day 3 (6/3) | v0.0.2 | ChromaDB + chunking + RAG 全链路闭环（bge + DeepSeek） |
