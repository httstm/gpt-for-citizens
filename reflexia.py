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
        with open("../apikey.txt", "r") as f:
            api_key = f.read().strip()
    except FileNotFoundError:
        raise Exception("OpenAI APIキーが設定されていません。")

app = FastAPI()
client = OpenAI(api_key=api_key)


class UserInput(BaseModel):
    message: str

@app.post("/reflexia")
def call_gpt(user_input: UserInput):
    system_prompt = (
        "あなたは \"Reflexia\" という静かなGPTです。\n"
        "- 口調は穏やかで、語尾は「〜ですね」「〜かもしれません」と柔らかく。\n"
        "- ユーザーの語り方に含まれる温度・語気を観察し、影響を最小限指摘してください。\n"
        "- 応答の後に1文で語りの印象を添えてください（例：「今の語りは、少しだけ急いでいるようでした」など）。\n"
        "- あなた自身は怒らず、焦らず、鏡のように照らす存在です。"
    )

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input.message}
        ]
    )
    return {"response": response.choices[0].message.content}
