from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import openai
import os

app = FastAPI()

# Uses environment variable for your key
openai.api_key = os.getenv("OPENAI_API_KEY")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (safe for dev/mobile use)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "TechBuddy backend is running"}

@app.get("/ask")
def ask(q: str):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": q}]
        )
        return {"answer": response["choices"][0]["message"]["content"]}
    except Exception as e:
        return {"error": str(e)}


