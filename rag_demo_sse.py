"""RAG 全链路 — 流式输出（打字机效果）"""
import os
import chromadb
from chromadb.utils import embedding_functions
from openai import OpenAI

api_key = os.getenv("DEEPSEEK_API_KEY")
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
embed_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="BAAI/bge-small-zh-v1.5"
)
chat_client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

documents = [
    "贵州茅台2025年营收1800亿元，同比增长15%，净利润880亿元。",
    "茅台酒出厂价1169元，市场零售价约2800元，系列酒出厂价200-500元。",
    "比亚迪2025年销量427万辆，海鸥售价7万元，汉售价22万元。",
    "特斯拉Model 3降价至23万元，Model Y售价26万元。",
    "茅台2026年目标营收增长12%，推进i茅台平台数字化转型。",
    "宁德时代2025年动力电池装机量全球第一，市场份额37%。",
]
client = chromadb.Client()
collection = client.create_collection(name="rag_kb", embedding_function=embed_fn)
for i, doc in enumerate(documents):
    collection.add(documents=[doc], ids=[f"doc_{i}"])

question = "茅台酒卖多少钱"
results = collection.query(query_texts=[question], n_results=3)
retrieved = results["documents"][0]

prompt = f"""根据以下资料回答问题。如果资料中没有相关信息，请说"资料中未提及"。

资料：
{chr(10).join(f'- {doc}' for doc in retrieved)}

问题：{question}
回答："""

print("DeepSeek 回答（流式）：", end="", flush=True)

stream = chat_client.chat.completions.create(
    model="deepseek-chat",
    messages=[{"role": "user", "content": prompt}],
    stream=True
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)

print()
