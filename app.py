import streamlit as st
import requests

st.title("AI 工程 Demo")

question = st.text_input("输入问题")

if st.button("提问"):
    resp = requests.post(
        "http://localhost:8000/ask",
        json={"content": question}
    )
    st.session_state["last_answer"] = resp.json()["answer"]

if "last_answer" in st.session_state:
    st.write(st.session_state["last_answer"])
