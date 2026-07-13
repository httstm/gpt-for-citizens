from fastapi import FastAPI
import os
import requests
import notion_mapper

from config import get_config

NOTION_TOKEN = get_config("NOTION_TOKEN")
DATABASE_ID = get_config("NOTION_DATABASE_ID")

app = FastAPI(
    title="Cookpan API",
    version="0.1.0",
    servers=[
        {
            "url": "https://clutch-eggnog-overarch.ngrok-free.dev"
        }
    ],
)

@app.get("/")
def root():
    return {"message": "Cookpan API"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/env-check")
def env_check():
    return {
        "has_token": NOTION_TOKEN is not None,
        "has_database_id": DATABASE_ID is not None
    }

@app.get("/recipes-raw")
def recipes_raw():
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"

    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json",
    }

    response = requests.post(url, headers=headers, json={})
    response.raise_for_status()

    return response.json()

@app.get("/recipes")
def recipes():
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"

    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json",
    }

    response = requests.post(url, headers=headers, json={})
    response.raise_for_status()

    data = response.json()

    return [
    notion_mapper.page_to_recipe(page)
    for page in data["results"]
    ]

@app.get("/recipe/{page_id}")
def recipe(page_id: str):
    url = f"https://api.notion.com/v1/pages/{page_id}"

    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": "2022-06-28",
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    page = response.json()

    return notion_mapper.page_to_recipe(page)