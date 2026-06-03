import streamlit as st
import requests

st.title("AI 工程 Demo")
uploaded_file = st.file_uploader("上传PDF", type = ["pdf"])
if uploaded_file is not None:
    st.write(f"已上传: {uploaded_file.name}")

question = st.text_input("输入问题")

if st.button("提问"):
    resp = requests.post(
        "http://localhost:8000/ask",
        json={"content": question}
    )
    st.session_state["last_answer"] = resp.json()["answer"]

if "last_answer" in st.session_state:
    st.write(st.session_state["last_answer"])
