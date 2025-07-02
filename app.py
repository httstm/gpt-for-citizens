from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv未インストールでもスルー

# APIキー取得
api_key = os.getenv("OPENAI_API_KEY") or None

if not api_key:
    # ローカル用ファイル読み込み（fallback）
    try:
        with open("apikey.txt", "r") as f:
            api_key = f.read().strip()
    except FileNotFoundError:
        raise Exception("OpenAI APIキーが設定されていません。")

app = FastAPI()
client = OpenAI(api_key=api_key)


class UserInput(BaseModel):
    message: str

@app.post("/gpt")
def call_gpt(user_input: UserInput):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "あなたは練馬区行政受付AIです。市民からの質問に丁寧に回答してください。"},
            {"role": "user", "content": user_input.message}
        ]
    )
    return {"response": response.choices[0].message.content}
