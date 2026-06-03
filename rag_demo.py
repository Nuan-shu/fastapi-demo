"""
rag最小原型: 文本 → 分块 → 入库 → 搜索 → 拼 Prompt
"""\

import chromadb

# 第一步: 准备知识库文本 (模拟pdf内容)

documents = ["贵州茅台2025年营收1800亿元，同比增长15%，净利润880亿元。",
            "茅台酒出厂价1169元，市场零售价约2800元，系列酒出厂价200-500元。",
            "比亚迪2025年销量427万辆，海鸥售价7万元，汉售价22万元。",
            "特斯拉Model 3降价至23万元，Model Y售价26万元。",
            "茅台2026年目标营收增长12%，推进i茅台平台数字化转型。",
            "宁德时代2025年动力电池装机量全球第一，市场份额37%。"
        ]

# 第二步: 入库CHromaDB

client = chromadb.Client()
collection = client.create_collection(name = "knowledge_base")

for i,doc in enumerate(documents):
    collection.add(documents = [doc], ids = [f"doc_{i}"])

print(f"知识库已入库 {len(documents)} 篇文档\n")

# 第三步: 用户提问 → 检索 → 拼Prompt

question = "茅台酒卖多少钱"

results = collection.query(query_texts = [question], n_results = 3)
# 取出检索到的文本
retrieved = results["documents"][0]
# 拼成Prompt(用来喂给LLM)
prompt = f""" 根据以下资料回答问题,如果资料中没有相关信息,请说"资料中未提及"
资料:
{chr(10).join(f'- {doc}' for doc in retrieved)}
问题: {question}
回答: """

print("="*50)
print("检索到的相关片段")
for i, doc in enumerate(retrieved):
    print(f" [{i+1}] {doc}")
    
print("\n" + "="*50)
print("拼好的Prompt (可以直接喂给Deepseek) : ")
print(prompt)


import os
from openai import OpenAI

client = OpenAI(
    api_key = os.getenv("DEEPSEEK_API_KEY"),
    base_url = "https://api.deepseek.com/v1"
)

response = client.chat.completions.create(
    model = "deepseek-chat",
    messages =  [{"role" : "user", "content": prompt}]
)

answer = response.choices[0].message.content

print("\n" + "=" * 50)
print("DeepSeek 回答: ")
print(answer)

