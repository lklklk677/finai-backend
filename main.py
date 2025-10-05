from fastapi import FastAPI
import os

app = FastAPI()

@app.get("/")
def root():
    return {
        "status": "healthy",
        "service": "FinAI Analyzer Pro",
        "message": "API is running!",
        "api_keys": {
            "alpha_vantage": "✅" if os.getenv("ALPHA_VANTAGE_KEY") else "❌",
            "deepseek": "✅" if os.getenv("DEEPSEEK_API_KEY") else "❌",
            "finnhub": "✅" if os.getenv("FINNHUB_KEY") else "❌"
        }
    }

@app.get("/health")
def health():
    return {"status": "ok", "timestamp": "2025-10-05"}
