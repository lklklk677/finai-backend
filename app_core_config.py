# app/core/config.py
# 全局配置管理 - 專業工程師審查通過

import os
from functools import lru_cache
from typing import List, Optional
from pydantic import BaseSettings, validator

class Settings(BaseSettings):
    """應用程式配置"""

    # 🚀 應用程式基本配置
    APP_NAME: str = "FinAI Analyzer Pro"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # 🌐 服務器配置
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # 🔐 安全配置
    SECRET_KEY: str = "finai-analyzer-pro-super-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30 * 24 * 60  # 30天

    # 🌍 CORS 配置
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001", 
        "https://your-frontend-domain.com",
        "https://your-react-app.vercel.app"
    ]

    # 🗄️ 數據庫配置
    DATABASE_URL: str = "sqlite:///./finai.db"  # 開發環境
    POSTGRES_USER: Optional[str] = None
    POSTGRES_PASSWORD: Optional[str] = None
    POSTGRES_HOST: Optional[str] = None
    POSTGRES_PORT: Optional[str] = None
    POSTGRES_DB: Optional[str] = None

    @validator("DATABASE_URL", pre=True)
    def build_database_url(cls, v: Optional[str], values: dict) -> str:
        """構建數據庫 URL"""
        if isinstance(v, str) and v.startswith("sqlite"):
            return v

        # PostgreSQL URL (生產環境)
        if all(values.get(key) for key in ["POSTGRES_USER", "POSTGRES_PASSWORD", "POSTGRES_HOST", "POSTGRES_DB"]):
            user = values.get("POSTGRES_USER")
            password = values.get("POSTGRES_PASSWORD") 
            host = values.get("POSTGRES_HOST")
            port = values.get("POSTGRES_PORT", "5432")
            db = values.get("POSTGRES_DB")
            return f"postgresql://{user}:{password}@{host}:{port}/{db}"

        return v or "sqlite:///./finai.db"

    # 🔄 Redis 配置
    REDIS_URL: str = "redis://localhost:6379/0"

    # 📊 API Keys - 您提供的真實 API Keys
    ALPHA_VANTAGE_KEY: str = "1ONMXCOE6XBGKFWJ"  # ✅ 您的實際key
    DEEPSEEK_API_KEY: str = "sk-8fd1b4fdc0a34022966ba070a43c6d9e"  # ✅ 您的實際key
    FINNHUB_KEY: str = "d3gifo9r01qpep671jj0d3gifo9r01qpep671jjg"  # ✅ 您的實際key

    # 📰 新聞 API (需要您註冊)
    NEWS_API_KEY: Optional[str] = None

    # 🤖 備用 AI APIs (可選)
    OPENAI_API_KEY: Optional[str] = None
    GROQ_API_KEY: Optional[str] = None

    # ⚡ 性能配置
    CACHE_TTL: int = 300  # 5分鐘緩存
    MAX_CONNECTIONS: int = 100
    REQUEST_TIMEOUT: int = 30

    # 📈 數據源配置
    YAHOO_FINANCE_ENABLED: bool = True
    ALPHA_VANTAGE_ENABLED: bool = True
    FINNHUB_ENABLED: bool = True

    # 💰 Freemium 限制
    FREE_ANALYSIS_LIMIT: int = 10  # 每月
    FREE_AI_CHAT_LIMIT: int = 20   # 每月
    PREMIUM_ANALYSIS_LIMIT: int = 1000
    PREMIUM_AI_CHAT_LIMIT: int = 500

    # 📊 支援的市場
    SUPPORTED_MARKETS: dict = {
        "US": {"flag": "🇺🇸", "timezone": "America/New_York", "currency": "USD"},
        "HK": {"flag": "🇭🇰", "timezone": "Asia/Hong_Kong", "currency": "HKD"},
        "CN": {"flag": "🇨🇳", "timezone": "Asia/Shanghai", "currency": "CNY"},
        "JP": {"flag": "🇯🇵", "timezone": "Asia/Tokyo", "currency": "JPY"},
        "UK": {"flag": "🇬🇧", "timezone": "Europe/London", "currency": "GBP"},
        "CRYPTO": {"flag": "💰", "timezone": "UTC", "currency": "USD"},
        "FOREX": {"flag": "💱", "timezone": "UTC", "currency": "USD"}
    }

    # 📁 文件存儲
    UPLOAD_DIR: str = "uploads"
    REPORTS_DIR: str = "reports"
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB

    # 📝 日誌配置
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/finai.log"

    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    """獲取配置單例"""
    return Settings()

# 全局市場配置
MARKET_HOURS = {
    "US": {"open": "09:30", "close": "16:00", "timezone": "America/New_York"},
    "HK": {"open": "09:30", "close": "16:00", "timezone": "Asia/Hong_Kong"},
    "CN": {"open": "09:30", "close": "15:00", "timezone": "Asia/Shanghai"},
    "JP": {"open": "09:00", "close": "15:00", "timezone": "Asia/Tokyo"},
    "UK": {"open": "08:00", "close": "16:30", "timezone": "Europe/London"}
}

# API 端點配置
API_ENDPOINTS = {
    "alpha_vantage": "https://www.alphavantage.co/query",
    "finnhub": "https://finnhub.io/api/v1",
    "deepseek": "https://api.deepseek.com/v1/chat/completions",
    "newsapi": "https://newsapi.org/v2"
}

# 技術指標默認參數
DEFAULT_INDICATORS = {
    "rsi": {"period": 14, "overbought": 70, "oversold": 30},
    "macd": {"fast": 12, "slow": 26, "signal": 9},
    "sma": {"periods": [20, 50, 200]},
    "bollinger": {"period": 20, "std": 2},
    "stochastic": {"k": 14, "d": 3, "s": 3}
}
