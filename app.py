from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI

# ファイルからAPIキーを読み込み
with open("apikey.txt", "r") as f:
    api_key = f.read().strip()

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
