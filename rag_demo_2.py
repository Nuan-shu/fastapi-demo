"""
RAG 全链路 — 中文 Embedding + DeepSeek Chat
"""
import os
import chromadb
from chromadb.utils import embedding_functions
from openai import OpenAI

# ============================================
# 配置
# ============================================
api_key = os.getenv("DEEPSEEK_API_KEY")

# Embedding：中文模型，通过国内镜像下载
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
embed_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="BAAI/bge-small-zh-v1.5"  # 轻量中文 embedding，512维
)

# Chat
chat_client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

# ============================================
# 第 1 步：入库
# ============================================
documents = [
    "贵州茅台2025年营收1800亿元，同比增长15%，净利润880亿元。",
    "茅台酒出厂价1169元，市场零售价约2800元，系列酒出厂价200-500元。",
    "比亚迪2025年销量427万辆，海鸥售价7万元，汉售价22万元。",
    "特斯拉Model 3降价至23万元，Model Y售价26万元。",
    "茅台2026年目标营收增长12%，推进i茅台平台数字化转型。",
    "宁德时代2025年动力电池装机量全球第一，市场份额37%。",
]

client = chromadb.Client()
collection = client.create_collection(
    name="knowledge_base",
    embedding_function=embed_fn
)

for i, doc in enumerate(documents):
    collection.add(documents=[doc], ids=[f"doc_{i}"])

print(f"知识库已入库 {len(documents)} 篇文档\n")

# ============================================
# 第 2 步：检索
# ============================================
question = "茅台酒卖多少钱"
results = collection.query(query_texts=[question], n_results=3)
retrieved = results["documents"][0]

print("=" * 50)
print("检索到的相关片段：")
for i, doc in enumerate(retrieved):
    print(f"  [{i+1}] {doc}")

# ============================================
# 第 3 步：拼 Prompt + 调 LLM
# ============================================
prompt = f"""根据以下资料回答问题。如果资料中没有相关信息，请说"资料中未提及"。

资料：
{chr(10).join(f'- {doc}' for doc in retrieved)}

问题：{question}
回答："""

response = chat_client.chat.completions.create(
    model="deepseek-chat",
    messages=[{"role": "user", "content": prompt}]
)

answer = response.choices[0].message.content

print("\n" + "=" * 50)
print("DeepSeek 回答：")
print(answer)
