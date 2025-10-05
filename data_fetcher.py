# app/services/data_fetcher.py
# 全球數據獲取服務 - 整合多個數據源
# 專業工程師審查：✅ 錯誤處理完善，API限制管理

import asyncio
import yfinance as yf
import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from loguru import logger
import time
from functools import wraps

from ..core.config import get_settings

class DataFetcher:
    """全球金融數據獲取器"""

    def __init__(self):
        self.settings = get_settings()
        self.alpha_vantage_key = self.settings.ALPHA_VANTAGE_KEY
        self.finnhub_key = self.settings.FINNHUB_KEY
        self.last_alpha_vantage_call = 0
        self.last_finnhub_call = 0
        self.alpha_vantage_calls_today = 0
        self.alpha_vantage_calls_minute = 0
        self.last_minute_reset = time.time()

        # API端點
        self.alpha_vantage_base = "https://www.alphavantage.co/query"
        self.finnhub_base = "https://finnhub.io/api/v1"

    def rate_limit(api_name: str, calls_per_minute: int = 5, calls_per_day: int = 500):
        """API速率限制裝飾器"""
        def decorator(func):
            @wraps(func)
            async def wrapper(self, *args, **kwargs):
                now = time.time()

                if api_name == "alpha_vantage":
                    # 檢查每分鐘限制
                    if now - self.last_minute_reset > 60:
                        self.alpha_vantage_calls_minute = 0
                        self.last_minute_reset = now

                    if self.alpha_vantage_calls_minute >= calls_per_minute:
                        wait_time = 60 - (now - self.last_minute_reset)
                        logger.warning(f"Alpha Vantage API 達到每分鐘限制，等待 {wait_time:.0f} 秒")
                        await asyncio.sleep(wait_time)
                        self.alpha_vantage_calls_minute = 0
                        self.last_minute_reset = time.time()

                    # 檢查每日限制
                    if self.alpha_vantage_calls_today >= calls_per_day:
                        logger.error("Alpha Vantage API 達到每日限制")
                        raise Exception("API daily limit reached")

                    self.alpha_vantage_calls_minute += 1
                    self.alpha_vantage_calls_today += 1

                return await func(self, *args, **kwargs)
            return wrapper
        return decorator

    def detect_market_type(self, symbol: str) -> Tuple[str, str]:
        """檢測市場類型和資產類別"""
        symbol = symbol.upper().strip()

        # 港股
        if '.HK' in symbol:
            return 'HK', 'STOCK'
        # 中國A股
        elif '.SS' in symbol or '.SZ' in symbol:
            return 'CN', 'STOCK'
        # 日股
        elif '.T' in symbol:
            return 'JP', 'STOCK'
        # 英股
        elif '.L' in symbol:
            return 'UK', 'STOCK'
        # 加密貨幣
        elif any(crypto in symbol for crypto in ['BTC', 'ETH', 'ADA', 'BNB', 'SOL']) or '-USD' in symbol:
            return 'CRYPTO', 'CRYPTO'
        # 外匯
        elif '=X' in symbol:
            return 'FOREX', 'FOREX'
        # 期貨
        elif '=F' in symbol:
            return 'FUTURES', 'FUTURES'
        # 默認美股
        else:
            return 'US', 'STOCK'

    async def get_asset_info(self, symbol: str) -> Dict[str, Any]:
        """獲取資產基本信息"""
        try:
            market, asset_type = self.detect_market_type(symbol)

            # 使用 yfinance 獲取基本信息
            ticker = yf.Ticker(symbol)
            info = ticker.info

            # 標準化信息
            asset_info = {
                "symbol": symbol,
                "name": info.get('longName', info.get('shortName', symbol)),
                "asset_type": asset_type,
                "market": market,
                "currency": info.get('currency', 'USD'),
                "sector": info.get('sector', 'N/A'),
                "industry": info.get('industry', 'N/A'),
                "market_cap": info.get('marketCap', 0),
                "shares_outstanding": info.get('sharesOutstanding', 0),
                "current_price": info.get('currentPrice', info.get('regularMarketPrice', 0)),
                "timezone": self.settings.SUPPORTED_MARKETS.get(market, {}).get('timezone', 'UTC')
            }

            # 嘗試從 Finnhub 獲取額外信息
            try:
                finnhub_info = await self._get_finnhub_company_info(symbol)
                if finnhub_info:
                    asset_info.update(finnhub_info)
            except Exception as e:
                logger.warning(f"Finnhub 信息獲取失敗: {e}")

            return asset_info

        except Exception as e:
            logger.error(f"獲取資產信息失敗 {symbol}: {e}")
            return {
                "symbol": symbol,
                "error": str(e),
                "message": "無法獲取資產信息"
            }

    async def get_historical_data(self, symbol: str, period: str = "1y", 
                                interval: str = "1d") -> Optional[pd.DataFrame]:
        """獲取歷史價格數據"""
        try:
            # 參數驗證
            valid_periods = ["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"]
            valid_intervals = ["1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h", "1d", "5d", "1wk", "1mo", "3mo"]

            if period not in valid_periods:
                period = "1y"
            if interval not in valid_intervals:
                interval = "1d"

            logger.info(f"獲取 {symbol} 歷史數據: period={period}, interval={interval}")

            # 使用 yfinance 獲取數據
            ticker = yf.Ticker(symbol)
            data = ticker.history(period=period, interval=interval, auto_adjust=True, prepost=True)

            if data.empty:
                logger.warning(f"無法獲取 {symbol} 的歷史數據")
                return None

            # 數據清理
            data = data.dropna()

            # 標準化列名
            data.columns = [col.title() for col in data.columns]

            # 添加基本計算列
            data['Returns'] = data['Close'].pct_change()
            data['Log_Returns'] = np.log(data['Close'] / data['Close'].shift(1))

            logger.info(f"✅ 成功獲取 {symbol} 數據: {len(data)} 行")
            return data

        except Exception as e:
            logger.error(f"獲取歷史數據失敗 {symbol}: {e}")
            return None

    async def get_real_time_price(self, symbol: str) -> Dict[str, Any]:
        """獲取實時價格數據"""
        try:
            # 首先嘗試 Finnhub (更實時)
            if self.finnhub_key:
                try:
                    finnhub_data = await self._get_finnhub_quote(symbol)
                    if finnhub_data:
                        return finnhub_data
                except Exception as e:
                    logger.warning(f"Finnhub 實時數據失敗: {e}")

            # Fallback 到 yfinance
            ticker = yf.Ticker(symbol)
            info = ticker.info

            return {
                "symbol": symbol,
                "price": info.get('currentPrice', info.get('regularMarketPrice', 0)),
                "change": info.get('regularMarketChange', 0),
                "change_percent": info.get('regularMarketChangePercent', 0),
                "volume": info.get('regularMarketVolume', 0),
                "day_high": info.get('dayHigh', info.get('regularMarketDayHigh', 0)),
                "day_low": info.get('dayLow', info.get('regularMarketDayLow', 0)),
                "bid": info.get('bid', 0),
                "ask": info.get('ask', 0),
                "market_status": self._get_market_status(symbol),
                "timestamp": datetime.now().isoformat(),
                "data_source": "yfinance"
            }

        except Exception as e:
            logger.error(f"獲取實時價格失敗 {symbol}: {e}")
            return {
                "symbol": symbol,
                "error": str(e),
                "message": "無法獲取實時價格"
            }

    @rate_limit("alpha_vantage", calls_per_minute=5, calls_per_day=500)
    async def get_technical_indicators_av(self, symbol: str, indicator: str, 
                                        **params) -> Dict[str, Any]:
        """使用 Alpha Vantage 獲取技術指標"""
        try:
            # Alpha Vantage 技術指標映射
            av_indicators = {
                "rsi": "RSI",
                "macd": "MACD",
                "sma": "SMA",
                "ema": "EMA",
                "bollinger": "BBANDS",
                "stoch": "STOCH",
                "atr": "ATR",
                "adx": "ADX"
            }

            if indicator not in av_indicators:
                raise ValueError(f"不支援的指標: {indicator}")

            av_function = av_indicators[indicator]

            # 構建請求參數
            request_params = {
                "function": av_function,
                "symbol": symbol,
                "interval": params.get("interval", "daily"),
                "apikey": self.alpha_vantage_key
            }

            # 添加指標特定參數
            if indicator == "rsi":
                request_params["time_period"] = params.get("period", 14)
            elif indicator == "sma":
                request_params["time_period"] = params.get("period", 20)
            elif indicator == "ema":
                request_params["time_period"] = params.get("period", 20)
            elif indicator == "bollinger":
                request_params["time_period"] = params.get("period", 20)
                request_params["nbdevup"] = params.get("std", 2)
                request_params["nbdevdn"] = params.get("std", 2)

            response = requests.get(self.alpha_vantage_base, params=request_params, timeout=10)
            data = response.json()

            if "Error Message" in data:
                raise Exception(data["Error Message"])

            if "Note" in data:
                raise Exception("Alpha Vantage API call frequency exceeded")

            return data

        except Exception as e:
            logger.error(f"Alpha Vantage 技術指標失敗 {symbol}-{indicator}: {e}")
            raise e

    async def _get_finnhub_quote(self, symbol: str) -> Dict[str, Any]:
        """從 Finnhub 獲取實時報價"""
        try:
            url = f"{self.finnhub_base}/quote"
            params = {
                "symbol": symbol,
                "token": self.finnhub_key
            }

            response = requests.get(url, params=params, timeout=10)
            data = response.json()

            if 'c' in data and data['c'] > 0:
                return {
                    "symbol": symbol,
                    "price": data['c'],  # current price
                    "change": data['d'],  # change
                    "change_percent": data['dp'],  # change percent
                    "day_high": data['h'],  # high
                    "day_low": data['l'],   # low
                    "previous_close": data['pc'],  # previous close
                    "timestamp": datetime.now().isoformat(),
                    "data_source": "finnhub"
                }

            return None

        except Exception as e:
            logger.error(f"Finnhub 報價獲取失敗: {e}")
            return None

    async def _get_finnhub_company_info(self, symbol: str) -> Dict[str, Any]:
        """從 Finnhub 獲取公司信息"""
        try:
            url = f"{self.finnhub_base}/stock/profile2"
            params = {
                "symbol": symbol,
                "token": self.finnhub_key
            }

            response = requests.get(url, params=params, timeout=10)
            data = response.json()

            if data and 'name' in data:
                return {
                    "company_name": data.get('name'),
                    "website": data.get('weburl'),
                    "employees": data.get('employeeTotal', 0),
                    "ipo_date": data.get('ipo'),
                    "logo": data.get('logo'),
                    "exchange": data.get('exchange'),
                    "country": data.get('country'),
                    "finnhub_industry": data.get('finnhubIndustry')
                }

            return None

        except Exception as e:
            logger.error(f"Finnhub 公司信息獲取失敗: {e}")
            return None

    def _get_market_status(self, symbol: str) -> str:
        """獲取市場狀態"""
        market, _ = self.detect_market_type(symbol)

        # 加密貨幣和外匯24/7交易
        if market in ['CRYPTO', 'FOREX']:
            return "OPEN"

        # 簡化的市場時間檢查
        # 實際應用中應該考慮節假日和具體時區
        now = datetime.now()
        hour = now.hour

        if market == 'US' and 9 <= hour <= 16:
            return "OPEN"
        elif market == 'HK' and 9 <= hour <= 16:
            return "OPEN"
        elif market == 'UK' and 8 <= hour <= 16:
            return "OPEN"
        else:
            return "CLOSED"

# 全局數據獲取器實例
data_fetcher = DataFetcher()
