"""
Pydantic 复习 — 三个实验
"""
from pydantic import BaseModel

# ============================================================
# 你的 Question 模型（第17-19行）
# ============================================================
class Question(BaseModel):
    content: str              # 必填，必须是字符串
    model: str = "deepseek"   # 可选，不传就用 deepseek


print("=" * 50)
print("实验 1：普通 dict vs Pydantic，有什么不同")
print("=" * 50)

# 普通字典 — 没有任何校验
d = {"content": 123, "model": 456}  # 数字也能塞进去
print(f"普通 dict: {d}")
print(f"d['content'] 的类型: {type(d['content'])}")  # int，不是 str

# Pydantic — 自动校验 + 类型转换
q = Question(content="Python怎么学")
print(f"\nPydantic 模型: {q}")
print(f"q.content = {q.content}  (类型: {type(q.content).__name__})")
print(f"q.model   = {q.model}    (类型: {type(q.model).__name__})")
print(f"q.model_dump() = {q.model_dump()}")  # 转回字典

print()
print("=" * 50)
print("实验 2：不传必填字段会怎样")
print("=" * 50)

try:
    q2 = Question(model="gpt4")  # 没传 content
except Exception as e:
    print(f"报错了！")
    print(f"错误类型: {type(e).__name__}")
    # 只打印第一行错误
    errors = e.errors()
    for err in errors:
        print(f"  字段: {err['loc']}")
        print(f"  原因: {err['msg']}")
        print(f"  类型: {err['type']}")

print()
print("=" * 50)
print("实验 3：可选字段不传 — 默认值生效")
print("=" * 50)

q3 = Question(content="什么是RAG")  # 没传 model
print(f"q3.content = {q3.content}")
print(f"q3.model   = {q3.model}  ← 自动用了默认值 'deepseek'")
