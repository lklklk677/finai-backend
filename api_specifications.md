# 🌐 FinAI Analyzer Pro - API 詳細規格

## 🔗 Base URL
```
Development: http://localhost:8000
Production: https://your-api-domain.com
```

## 🔐 認證
所有 API 請求需要包含 API Key：
```
Headers: {
    "X-API-Key": "your-api-key"
}
```

## 📋 API 端點列表

### 1. 市場數據 API

#### 獲取資產資訊
```http
GET /api/v1/market/asset-info/{symbol}
```
**參數:**
- `symbol` (string): 資產代碼 (例: AAPL, 0700.HK, BTC-USD)

**回應:**
```json
{
    "status": "success",
    "data": {
        "symbol": "AAPL",
        "name": "Apple Inc.",
        "asset_type": "US_STOCK",
        "market": "NASDAQ",
        "currency": "USD",
        "timezone": "America/New_York",
        "sector": "Technology",
        "industry": "Consumer Electronics",
        "current_price": 175.84,
        "market_cap": 2750000000000,
        "shares_outstanding": 15637894000
    }
}
```

#### 獲取歷史價格數據
```http
POST /api/v1/market/historical-data
```
**請求體:**
```json
{
    "symbol": "AAPL",
    "period": "1y",
    "interval": "1d",
    "include_indicators": true
}
```

**回應:**
```json
{
    "status": "success",
    "data": {
        "symbol": "AAPL",
        "period": "1y",
        "data": [
            {
                "date": "2024-01-01",
                "open": 190.00,
                "high": 195.50,
                "low": 188.75,
                "close": 193.25,
                "volume": 45678900,
                "adjusted_close": 193.25
            }
        ],
        "technical_indicators": {
            "sma_20": [185.50, 186.75, 188.00],
            "sma_50": [182.25, 183.50, 184.75],
            "rsi": [45.2, 47.8, 52.3],
            "macd": {
                "macd_line": [1.25, 1.45, 1.68],
                "signal_line": [1.15, 1.32, 1.55],
                "histogram": [0.10, 0.13, 0.13]
            }
        }
    }
}
```

#### 即時價格
```http
GET /api/v1/market/real-time/{symbol}
```

**回應:**
```json
{
    "status": "success",
    "data": {
        "symbol": "AAPL",
        "price": 175.84,
        "change": 2.34,
        "change_percent": 1.35,
        "volume": 67890123,
        "timestamp": "2024-10-05T13:30:00Z",
        "market_status": "OPEN",
        "bid": 175.83,
        "ask": 175.85,
        "day_high": 176.50,
        "day_low": 173.25
    }
}
```

### 2. 技術分析 API

#### 技術指標計算
```http
POST /api/v1/analysis/technical
```

**請求體:**
```json
{
    "symbol": "AAPL",
    "period": "6m",
    "indicators": [
        "rsi",
        "macd", 
        "bollinger_bands",
        "stochastic",
        "sma",
        "ema",
        "atr"
    ],
    "parameters": {
        "rsi_period": 14,
        "macd_fast": 12,
        "macd_slow": 26,
        "macd_signal": 9,
        "bollinger_period": 20,
        "bollinger_std": 2,
        "sma_periods": [20, 50, 200],
        "ema_periods": [12, 26]
    }
}
```

**回應:**
```json
{
    "status": "success",
    "data": {
        "symbol": "AAPL",
        "analysis_date": "2024-10-05T13:30:00Z",
        "current_price": 175.84,
        "technical_score": 72,
        "recommendation": "BUY",
        "confidence": 0.85,
        "indicators": {
            "rsi": {
                "current": 55.2,
                "signal": "NEUTRAL",
                "description": "RSI在中性區間，無明確買賣信號"
            },
            "macd": {
                "current": {
                    "macd": 1.68,
                    "signal": 1.55,
                    "histogram": 0.13
                },
                "signal": "BUY",
                "description": "MACD金叉，買入信號"
            },
            "bollinger_bands": {
                "current": {
                    "upper": 185.50,
                    "middle": 178.25,
                    "lower": 171.00,
                    "position": 0.65
                },
                "signal": "NEUTRAL",
                "description": "價格位於布林帶中上部"
            }
        },
        "signals": [
            {
                "type": "BUY",
                "strength": "STRONG",
                "indicator": "MACD",
                "description": "MACD線向上突破訊號線，形成金叉"
            },
            {
                "type": "NEUTRAL",
                "strength": "WEAK",
                "indicator": "RSI",
                "description": "RSI處於50附近中性區域"
            }
        ],
        "support_resistance": {
            "resistance_levels": [180.00, 185.50, 190.25],
            "support_levels": [170.00, 165.25, 160.50]
        },
        "trend_analysis": {
            "short_term": "BULLISH",
            "medium_term": "BULLISH", 
            "long_term": "BULLISH",
            "trend_strength": 0.78
        }
    }
}
```

#### 模式識別
```http
POST /api/v1/analysis/patterns
```

**請求體:**
```json
{
    "symbol": "AAPL",
    "period": "3m",
    "patterns": [
        "head_and_shoulders",
        "double_top",
        "double_bottom",
        "triangle",
        "flag",
        "pennant"
    ]
}
```

**回應:**
```json
{
    "status": "success",
    "data": {
        "symbol": "AAPL",
        "patterns_found": [
            {
                "pattern_type": "ascending_triangle",
                "confidence": 0.82,
                "timeframe": "2024-09-15 to 2024-10-05",
                "breakout_target": 185.00,
                "stop_loss": 168.50,
                "description": "上升三角形形態，預期向上突破"
            }
        ],
        "chart_annotations": [
            {
                "type": "trendline",
                "points": [
                    {"date": "2024-09-15", "price": 170.00},
                    {"date": "2024-10-05", "price": 175.84}
                ]
            }
        ]
    }
}
```

### 3. 基本面分析 API

#### 財務指標分析
```http
POST /api/v1/analysis/fundamental
```

**請求體:**
```json
{
    "symbol": "AAPL",
    "metrics": [
        "valuation",
        "profitability", 
        "financial_health",
        "growth",
        "dividend"
    ],
    "period": "5y",
    "benchmark": "SPY"
}
```

**回應:**
```json
{
    "status": "success",
    "data": {
        "symbol": "AAPL",
        "company_info": {
            "name": "Apple Inc.",
            "sector": "Technology",
            "industry": "Consumer Electronics",
            "employees": 164000,
            "market_cap": 2750000000000,
            "enterprise_value": 2680000000000
        },
        "fundamental_score": 85,
        "recommendation": "BUY",
        "valuation": {
            "pe_ratio": {
                "current": 28.5,
                "sector_avg": 32.1,
                "5y_avg": 25.8,
                "rating": "FAIR"
            },
            "pb_ratio": {
                "current": 8.9,
                "sector_avg": 6.5,
                "5y_avg": 7.2,
                "rating": "EXPENSIVE"
            },
            "peg_ratio": {
                "current": 1.8,
                "rating": "FAIR"
            },
            "ev_ebitda": {
                "current": 22.3,
                "sector_avg": 25.8,
                "rating": "ATTRACTIVE"
            }
        },
        "profitability": {
            "roe": {
                "current": 0.365,
                "sector_avg": 0.185,
                "5y_avg": 0.315,
                "rating": "EXCELLENT"
            },
            "roa": {
                "current": 0.185,
                "sector_avg": 0.089,
                "rating": "EXCELLENT"
            },
            "gross_margin": {
                "current": 0.456,
                "5y_avg": 0.421,
                "trend": "IMPROVING"
            },
            "net_margin": {
                "current": 0.231,
                "5y_avg": 0.208,
                "trend": "IMPROVING"
            }
        },
        "financial_health": {
            "debt_to_equity": {
                "current": 1.85,
                "sector_avg": 0.95,
                "rating": "MODERATE_RISK"
            },
            "current_ratio": {
                "current": 1.05,
                "rating": "ADEQUATE"
            },
            "interest_coverage": {
                "current": 28.5,
                "rating": "STRONG"
            }
        },
        "growth": {
            "revenue_growth_5y": 0.089,
            "eps_growth_5y": 0.125,
            "dividend_growth_5y": 0.065,
            "growth_consistency": 0.82,
            "rating": "STRONG"
        },
        "dividend": {
            "dividend_yield": 0.0045,
            "payout_ratio": 0.15,
            "dividend_growth_10y": 0.078,
            "rating": "CONSERVATIVE"
        },
        "benchmark_comparison": {
            "benchmark": "SPY",
            "relative_pe": 0.85,
            "relative_roe": 1.97,
            "relative_growth": 1.23,
            "outperformance_score": 78
        }
    }
}
```

### 4. 風險分析 API

#### 風險指標計算
```http
POST /api/v1/analysis/risk
```

**請求體:**
```json
{
    "symbol": "AAPL",
    "period": "2y",
    "confidence_levels": [0.95, 0.99],
    "benchmark": "SPY",
    "stress_test": true,
    "monte_carlo": {
        "enabled": true,
        "iterations": 10000,
        "forecast_days": [30, 90, 180]
    }
}
```

**回應:**
```json
{
    "status": "success",
    "data": {
        "symbol": "AAPL",
        "analysis_date": "2024-10-05T13:30:00Z",
        "current_price": 175.84,
        "risk_score": 65,
        "risk_level": "MEDIUM",
        "market_risk": {
            "beta": {
                "value": 1.25,
                "vs_spy": 1.25,
                "vs_sector": 1.08,
                "interpretation": "比大盤波動性高25%"
            },
            "correlation": {
                "vs_spy": 0.82,
                "vs_qqq": 0.89,
                "vs_sector": 0.76
            }
        },
        "volatility": {
            "realized_volatility": {
                "30d": 0.285,
                "90d": 0.312,
                "1y": 0.278,
                "annualized": 0.285
            },
            "implied_volatility": 0.295,
            "volatility_rank": 45
        },
        "var": {
            "confidence_95": {
                "1d": -0.032,
                "1w": -0.071,
                "1m": -0.145,
                "amount_usd": -5632.80
            },
            "confidence_99": {
                "1d": -0.048,
                "1w": -0.106, 
                "1m": -0.218,
                "amount_usd": -8458.32
            }
        },
        "cvar": {
            "confidence_95": -0.052,
            "confidence_99": -0.078,
            "amount_usd": -13698.24
        },
        "risk_adjusted_returns": {
            "sharpe_ratio": {
                "1y": 1.85,
                "3y": 1.92,
                "5y": 1.68,
                "rating": "EXCELLENT"
            },
            "sortino_ratio": {
                "1y": 2.63,
                "3y": 2.78,
                "rating": "EXCELLENT"
            },
            "calmar_ratio": {
                "3y": 1.24,
                "rating": "GOOD"
            }
        },
        "drawdown_analysis": {
            "max_drawdown": {
                "value": -0.278,
                "start_date": "2022-01-03",
                "end_date": "2022-10-03",
                "recovery_date": "2023-07-31",
                "recovery_days": 301
            },
            "current_drawdown": -0.045,
            "avg_drawdown": -0.089,
            "drawdown_frequency": 0.15
        },
        "stress_testing": {
            "scenarios": {
                "market_crash_2008": {
                    "expected_return": -0.42,
                    "probability": 0.02,
                    "description": "類似2008金融危機情景"
                },
                "covid_pandemic": {
                    "expected_return": -0.35,
                    "probability": 0.05,
                    "description": "類似2020疫情衝擊"
                },
                "fed_rate_hike": {
                    "expected_return": -0.18,
                    "probability": 0.25,
                    "description": "聯準會激進升息"
                },
                "tech_bubble_burst": {
                    "expected_return": -0.55,
                    "probability": 0.08,
                    "description": "科技股泡沫破裂"
                }
            }
        },
        "monte_carlo_simulation": {
            "iterations": 10000,
            "forecast": {
                "30d": {
                    "expected_return": 0.025,
                    "confidence_intervals": {
                        "95": {"lower": -0.18, "upper": 0.23},
                        "90": {"lower": -0.14, "upper": 0.19},
                        "80": {"lower": -0.09, "upper": 0.14}
                    },
                    "probability_positive": 0.68,
                    "expected_price": 180.23
                },
                "90d": {
                    "expected_return": 0.075,
                    "confidence_intervals": {
                        "95": {"lower": -0.31, "upper": 0.46},
                        "90": {"lower": -0.25, "upper": 0.40},
                        "80": {"lower": -0.18, "upper": 0.33}
                    },
                    "probability_positive": 0.72,
                    "expected_price": 189.03
                }
            }
        },
        "risk_recommendations": [
            {
                "type": "POSITION_SIZING",
                "recommendation": "建議持股不超過投資組合的8-10%",
                "reason": "考慮到Beta 1.25的高波動性"
            },
            {
                "type": "STOP_LOSS",
                "recommendation": "建議設定止損點為165.00 (-6.2%)",
                "reason": "基於2倍ATR和支撐位分析"
            },
            {
                "type": "HEDGING",
                "recommendation": "可考慮購買保護性認沽期權",
                "reason": "科技股面臨估值壓力風險"
            }
        ]
    }
}
```

### 5. 新聞分析 API

#### 新聞情緒分析
```http
POST /api/v1/analysis/news
```

**請求體:**
```json
{
    "symbol": "AAPL",
    "limit": 20,
    "days": 7,
    "languages": ["en", "zh"],
    "sources": ["all"],
    "sentiment_analysis": true,
    "impact_analysis": true
}
```

**回應:**
```json
{
    "status": "success",
    "data": {
        "symbol": "AAPL",
        "analysis_period": "2024-09-28 to 2024-10-05",
        "total_articles": 156,
        "sentiment_summary": {
            "overall_score": 0.35,
            "overall_sentiment": "POSITIVE",
            "positive_count": 89,
            "neutral_count": 45,
            "negative_count": 22,
            "sentiment_trend": "IMPROVING"
        },
        "impact_analysis": {
            "high_impact_news": 12,
            "medium_impact_news": 34,
            "low_impact_news": 110,
            "market_moving_events": [
                {
                    "date": "2024-10-03",
                    "headline": "Apple發布iPhone 16 Pro系列",
                    "impact_score": 0.85,
                    "price_correlation": 0.15
                }
            ]
        },
        "news_articles": [
            {
                "id": "news_001",
                "published_at": "2024-10-05T10:30:00Z",
                "headline": "Apple's Q4 Earnings Beat Expectations",
                "summary": "Apple公佈第四季度財報超出預期，iPhone銷售強勁...",
                "source": "Reuters",
                "url": "https://reuters.com/...",
                "sentiment": {
                    "score": 0.78,
                    "label": "POSITIVE",
                    "confidence": 0.92
                },
                "impact": {
                    "score": 0.88,
                    "level": "HIGH",
                    "categories": ["EARNINGS", "REVENUE"]
                },
                "key_topics": ["earnings", "iphone", "revenue", "guidance"],
                "language": "en"
            }
        ],
        "topic_analysis": {
            "most_discussed_topics": [
                {"topic": "earnings", "frequency": 45, "sentiment": 0.65},
                {"topic": "iphone", "frequency": 38, "sentiment": 0.42},
                {"topic": "ai", "frequency": 29, "sentiment": 0.58},
                {"topic": "china", "frequency": 22, "sentiment": -0.12}
            ]
        },
        "sentiment_timeline": [
            {
                "date": "2024-09-28",
                "sentiment_score": 0.12,
                "article_count": 18
            },
            {
                "date": "2024-10-05", 
                "sentiment_score": 0.68,
                "article_count": 28
            }
        ]
    }
}
```

### 6. 投資組合 API

#### 組合分析
```http
POST /api/v1/portfolio/analyze
```

**請求體:**
```json
{
    "portfolio": [
        {"symbol": "AAPL", "quantity": 100, "cost_basis": 150.00},
        {"symbol": "0700.HK", "quantity": 200, "cost_basis": 400.00},
        {"symbol": "BTC-USD", "quantity": 0.5, "cost_basis": 35000.00},
        {"symbol": "SPY", "quantity": 50, "cost_basis": 380.00}
    ],
    "benchmark": "SPY",
    "analysis_period": "1y",
    "rebalancing": true,
    "risk_assessment": true
}
```

**回應:**
```json
{
    "status": "success",
    "data": {
        "portfolio_summary": {
            "total_value": 127850.00,
            "total_cost": 110000.00,
            "total_return": 17850.00,
            "total_return_pct": 0.1623,
            "annualized_return": 0.1545,
            "last_updated": "2024-10-05T13:30:00Z"
        },
        "asset_allocation": [
            {
                "symbol": "AAPL",
                "current_value": 17584.00,
                "weight": 0.1375,
                "return": 0.1723,
                "contribution_to_return": 0.0237
            },
            {
                "symbol": "0700.HK", 
                "current_value": 73040.00,
                "weight": 0.5711,
                "return": -0.0875,
                "contribution_to_return": -0.0500
            }
        ],
        "diversification_analysis": {
            "diversification_score": 72,
            "sector_allocation": {
                "Technology": 0.71,
                "Financial": 0.15,
                "Cryptocurrency": 0.14
            },
            "geographic_allocation": {
                "US": 0.52,
                "Hong Kong": 0.34,
                "Global": 0.14
            },
            "correlation_matrix": {
                "AAPL_0700.HK": 0.45,
                "AAPL_BTC": 0.32,
                "0700.HK_BTC": 0.28
            }
        },
        "risk_metrics": {
            "portfolio_beta": 1.15,
            "portfolio_volatility": 0.235,
            "sharpe_ratio": 1.67,
            "max_drawdown": -0.18,
            "var_95": -0.045,
            "expected_shortfall": -0.068
        },
        "performance_vs_benchmark": {
            "benchmark": "SPY",
            "portfolio_return": 0.1623,
            "benchmark_return": 0.1285,
            "alpha": 0.0338,
            "beta": 1.15,
            "tracking_error": 0.078,
            "information_ratio": 0.43,
            "outperformance_periods": 0.68
        },
        "rebalancing_suggestions": [
            {
                "action": "REDUCE",
                "symbol": "0700.HK",
                "current_weight": 0.5711,
                "target_weight": 0.4500,
                "reason": "過度集中單一資產"
            },
            {
                "action": "INCREASE",
                "symbol": "SPY",
                "current_weight": 0.1489,
                "target_weight": 0.2500,
                "reason": "增加美股大盤配置"
            }
        ],
        "optimization_analysis": {
            "efficient_frontier": [
                {"risk": 0.15, "expected_return": 0.08},
                {"risk": 0.20, "expected_return": 0.12},
                {"risk": 0.25, "expected_return": 0.15}
            ],
            "optimal_portfolio": {
                "risk_tolerance": "MODERATE",
                "suggested_allocation": {
                    "AAPL": 0.20,
                    "0700.HK": 0.35,
                    "SPY": 0.30,
                    "BTC-USD": 0.15
                },
                "expected_return": 0.145,
                "expected_risk": 0.21,
                "sharpe_ratio": 1.89
            }
        }
    }
}
```

### 7. AI 聊天 API

#### AI 投資顧問
```http
POST /api/v1/ai/chat
```

**請求體:**
```json
{
    "message": "幫我分析0700.HK嘅投資風險",
    "language": "zh-HK",
    "context": {
        "user_portfolio": ["AAPL", "0700.HK", "BTC-USD"],
        "risk_tolerance": "MODERATE",
        "investment_horizon": "LONG_TERM"
    },
    "include_data": true,
    "session_id": "user_123_session_456"
}
```

**回應:**
```json
{
    "status": "success",
    "data": {
        "session_id": "user_123_session_456",
        "message_id": "msg_789",
        "response": {
            "text": "根據最新嘅分析，0700.HK（騰訊）而家面臨幾個主要風險：\n\n📊 **技術面風險**\n- RSI 28，處於超賣區域\n- 跌穿50日均線支撐\n- 成交量萎縮，缺乏買盤\n\n💼 **基本面挑戰**\n- 遊戲業務面臨監管壓力\n- 廣告收入受宏觀環境影響\n- 雲業務競爭激烈\n\n🌍 **宏觀風險**\n- 中美關係緊張影響科技股\n- 港股整體估值偏低\n- 資金流向美股\n\n💡 **投資建議**\n考慮到你嘅中等風險承受能力：\n1. 如果持有，建議減倉至組合10-15%\n2. 設定止損位：340港元\n3. 等待跌破300港元再考慮加倉\n4. 分散投資美股科技股作對沖\n\n你而家嘅組合已經有AAPL作科技股配置，騰訊權重唔宜過高。",
            "confidence": 0.88,
            "sources": [
                "technical_analysis_0700_hk",
                "fundamental_analysis_0700_hk", 
                "market_sentiment_hk_tech"
            ]
        },
        "analysis_data": {
            "symbol": "0700.HK",
            "current_price": 365.20,
            "technical_score": 25,
            "fundamental_score": 65,
            "risk_level": "HIGH",
            "recommendation": "REDUCE"
        },
        "follow_up_questions": [
            "想了解更多騰訊嘅財務狀況？",
            "需要其他港股科技股建議？",
            "想調整投資組合配置？"
        ],
        "usage": {
            "tokens_used": 245,
            "remaining_quota": 18,
            "quota_reset": "2024-11-01T00:00:00Z"
        }
    }
}
```

### 8. 預測分析 API

#### ML 價格預測
```http
POST /api/v1/prediction/price
```

**請求體:**
```json
{
    "symbol": "AAPL",
    "model": "prophet",
    "forecast_days": 30,
    "confidence_interval": 0.95,
    "include_events": true,
    "external_factors": [
        "earnings_date",
        "fed_meetings",
        "product_launches"
    ]
}
```

**回應:**
```json
{
    "status": "success",
    "data": {
        "symbol": "AAPL",
        "model_info": {
            "model_type": "Prophet",
            "training_period": "2022-01-01 to 2024-10-05",
            "model_accuracy": {
                "mae": 4.25,
                "mape": 0.025,
                "r2_score": 0.78
            },
            "last_trained": "2024-10-05T10:00:00Z"
        },
        "current_price": 175.84,
        "forecast": [
            {
                "date": "2024-10-06",
                "predicted_price": 177.25,
                "lower_bound": 172.50,
                "upper_bound": 182.00,
                "confidence": 0.95,
                "change_pct": 0.008
            },
            {
                "date": "2024-11-05",
                "predicted_price": 185.50,
                "lower_bound": 175.25,
                "upper_bound": 195.75,
                "confidence": 0.95,
                "change_pct": 0.055
            }
        ],
        "trend_components": {
            "overall_trend": "BULLISH",
            "trend_strength": 0.68,
            "seasonal_factors": {
                "yearly": 0.03,
                "quarterly": -0.01,
                "monthly": 0.02
            },
            "volatility_forecast": [
                {"date": "2024-10-06", "volatility": 0.025},
                {"date": "2024-11-05", "volatility": 0.032}
            ]
        },
        "key_events": [
            {
                "date": "2024-10-31",
                "event": "Q4 Earnings Release",
                "expected_impact": 0.05,
                "impact_direction": "POSITIVE"
            }
        ],
        "probability_analysis": {
            "probability_up_1w": 0.68,
            "probability_up_1m": 0.72,
            "probability_above_180": 0.65,
            "probability_below_170": 0.15
        },
        "model_disclaimer": "預測結果僅供參考，實際價格可能因市場因素大幅偏離預測值"
    }
}
```

### 9. 報告生成 API

#### 生成投資報告
```http
POST /api/v1/reports/generate
```

**請求體:**
```json
{
    "report_type": "COMPREHENSIVE_ANALYSIS",
    "symbol": "AAPL",
    "language": "zh-HK",
    "format": "PDF",
    "include_sections": [
        "executive_summary",
        "technical_analysis", 
        "fundamental_analysis",
        "risk_analysis",
        "news_sentiment",
        "price_prediction",
        "investment_recommendation"
    ],
    "custom_notes": "客戶風險承受能力：中等，投資期限：3-5年",
    "branding": {
        "company_name": "FinAI Analyzer Pro",
        "logo_url": "https://...",
        "primary_color": "#001F3F",
        "secondary_color": "#FFD700"
    }
}
```

**回應:**
```json
{
    "status": "success", 
    "data": {
        "report_id": "report_20241005_AAPL_001",
        "generated_at": "2024-10-05T13:45:00Z",
        "report_url": "https://api.domain.com/reports/download/report_20241005_AAPL_001.pdf",
        "report_metadata": {
            "symbol": "AAPL",
            "report_type": "COMPREHENSIVE_ANALYSIS",
            "language": "zh-HK",
            "pages": 15,
            "file_size": "2.3MB",
            "validity": "2024-11-05T13:45:00Z"
        },
        "executive_summary": {
            "overall_rating": "BUY",
            "confidence": 0.85,
            "target_price": 195.00,
            "risk_level": "MEDIUM",
            "key_highlights": [
                "技術面評分72/100，處於強勢區間",
                "基本面穩健，ROE達36.5%",
                "預期Q4財報將超出預期",
                "建議設定止損位165元"
            ]
        },
        "download_options": {
            "pdf_url": "https://api.domain.com/reports/download/report_20241005_AAPL_001.pdf",
            "excel_url": "https://api.domain.com/reports/download/report_20241005_AAPL_001.xlsx",
            "json_url": "https://api.domain.com/reports/download/report_20241005_AAPL_001.json"
        },
        "sharing": {
            "public_link": "https://reports.finai.com/public/report_20241005_AAPL_001",
            "expires_at": "2024-10-12T13:45:00Z",
            "password_protected": true
        }
    }
}
```

## 🔒 認證和限制

### API Key 管理
```http
POST /api/v1/auth/api-key
Content-Type: application/json

{
    "email": "user@example.com",
    "tier": "FREE"  // FREE, PREMIUM, ENTERPRISE
}
```

### 速率限制
- **免費版**: 100 requests/hour, 10 concurrent
- **Premium**: 1000 requests/hour, 50 concurrent  
- **Enterprise**: 無限制

### 錯誤回應格式
```json
{
    "status": "error",
    "error": {
        "code": "INVALID_SYMBOL",
        "message": "不支援的資產代碼",
        "details": "Symbol 'INVALID' not found in supported markets",
        "suggestion": "請檢查資產代碼格式，如：AAPL, 0700.HK, BTC-USD"
    },
    "timestamp": "2024-10-05T13:30:00Z",
    "request_id": "req_12345"
}
```

## 📊 數據更新頻率
- **即時價格**: 5-15秒延遲
- **技術指標**: 每分鐘更新
- **基本面數據**: 每日更新
- **新聞數據**: 每15分鐘
- **AI 分析**: 按需生成，緩存30分鐘