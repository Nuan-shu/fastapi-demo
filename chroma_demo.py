import os
import chromadb
from chromadb.utils import embedding_functions

# 中文 embedding（国内镜像）
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
embed_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="BAAI/bge-small-zh-v1.5"
)

# 建库
chroma_client = chromadb.Client()
collection = chroma_client.create_collection(
    name="my_docs",
    embedding_function=embed_fn
)

# 插入向量 — 存 4 段文本
collection.add(
    documents=[
        "贵州茅台2025年营收1800亿，同比增长15%",
        "比亚迪海鸥售价7万元，续航400公里",
        "茅台酒出厂价1169元，市场零售价2800元,提货价1000",
        "特斯拉Model 3降价到23万元"
    ],
    ids=["doc1", "doc2", "doc3", "doc4"]
)

# 相似度搜索 — 用户问「茅台多少钱」
results = collection.query(
    query_texts=["茅台多少钱"],
    n_results=2
)

print("用户问：茅台多少钱")
print("\n最相关的 2 段文本：")
for i, doc in enumerate(results["documents"][0]):
    print(f"  {i+1}. {doc}")
