from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Hello, FastAPI!"}


@app.get("/health")
def health_check():
    return {"status": "running"}


class Question(BaseModel):
    content: str
    model: str = "deepseek"


@app.post("/ask")
def ask(question: Question):
    reply = f"你问了：{question.content}（模型：{question.model}）"
    return {"answer": reply, "model": question.model}
