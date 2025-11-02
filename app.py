# 実行前に以下を実行する
# pip install "langchain==0.1.16" "langchain-openai==0.0.5"
# pip install python-dotenv streamlit openai>=1.0.0

from dotenv import load_dotenv
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

load_dotenv()

st.title("サンプルアプリ: LLMを使ったWebアプリ")

st.write("##### 専門家による回答生成")
st.write("専門家を選んでテキストを入力し、「実行」ボタンを押すと、その専門家の視点で回答が表示されます。")

selected_item = st.radio(
    "専門家の種類を選択してください。",
    ["A：インフラエンジニア（AWS/ネットワーク/SRE）", "B：英語コーチ（簡潔な英文作成・校正）"]
)

st.divider()

input_message = st.text_input(label="テキストを入力してください。")

SYSTEM_MESSAGES = {
    "A：インフラエンジニア（AWS/ネットワーク/SRE）":
        ("You are a senior infrastructure engineer (AWS/Network/SRE). "
         "Provide concise, practical guidance considering reliability, security, cost, and operations."),
    "B：英語コーチ（簡潔な英文作成・校正）":
        ("You are an English writing coach. Provide concise, natural business English with brief tips and alternatives."),
}

def generate_answer(text: str, mode: str) -> str:
    if not text:
        return ""
    system_content = SYSTEM_MESSAGES.get(mode, "You are a helpful assistant.")
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.2)
    messages = [SystemMessage(content=system_content), HumanMessage(content=text)]
    result = llm(messages)
    return result.content

if st.button("実行"):
    st.divider()
    if input_message:
        answer = generate_answer(input_message, selected_item)
        st.write("##### 回答")
        st.write(answer)
    else:
        st.error("テキストを入力してから「実行」ボタンを押してください。")