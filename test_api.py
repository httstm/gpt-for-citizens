import streamlit as st
import requests

st.title("行政受付AIデモ")

# ユーザー入力
user_input = st.text_input("質問を入力してください:")

if st.button("送信"):
    if user_input:
        # FastAPIサーバーへのPOSTリクエスト
        url = "https://gpt-for-citizens.onrender.com/gpt"
        # url = "https://34a3-240f-37-3ba0-1-6983-2b32-7aca-ff3f.ngrok-free.app/gpt"
        # url = "http://127.0.0.1:8000/gpt"  # エンドポイント

        payload = {"message": user_input}  # ←ここが重要

        response = requests.post(url, json=payload)

        if response.status_code == 200:
            result = response.json()
            st.write("回答:")
            st.write(result["response"])  # FastAPIのreturn構造に合わせて表示
        else:
            st.write("エラーが発生しました。")
    else:
        st.write("質問を入力してください。")
