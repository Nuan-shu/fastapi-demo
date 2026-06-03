import chromadb





text = """ 州茅台酒股份有限公司2025年年度报告。
     公司实现营业总收入1800亿元，同比增长15%。
     其中茅台酒销售收入1600亿元，系列酒销售收入200亿元。
     归属于上市公司股东的净利润为880亿元，同比增长13%。
     公司拟向全体股东每10股派发现金红利300元。
     2026年公司经营目标：营业总收入较上年度增长12%左右。
     公司将继续推进数字化转型，深化i茅台平台建设。
     报告期内，公司完成茅台酒基酒产量5.8万吨，系列酒基酒产量4.2万吨。"""

# 分块参数
chunk_size = 100 # 每块 100 个字符
overlap = 20 # 重叠 20 个字符

# 开始分块
chunks = [] 
start = 0 
while start < len(text):
    end = start + chunk_size 
    chunk = text[start:end]
    chunks.append(chunk)
    start = end - overlap # 下一块往回退overlap个字符

print(f"原文长度: {len(text)} 字符")
print(f"分块大小: {chunk_size}, 重叠: {overlap}")
print(f"共切出 {len(chunks)} 块: \n")
for i, chunk in enumerate(chunks):
    print(f"--- 块 {i+1} ({len(chunk)} 字符) ---")
    print(chunk)
    print()
    



client = chromadb.Client()
collection = client.create_collection(name= "maotai_report")

# 入库# 模拟一片财报文本
for i, chunk in enumerate(chunks):
    collection.add(
        documents = [chunk],
        ids = [f"chunk_{i}"]
    )

# 搜索
results = collection.query(
    query_texts = ["茅台酒产量"],
    n_results = 2
)


print("\n======== 在 ChromaDB 中搜索 [茅台酒产量] ========")
for i,doc in enumerate(results["documents"][0]):
    print(f" 相关块 {i+1}: {doc[:80]}...")
