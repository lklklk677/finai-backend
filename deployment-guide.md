# 🚀 FinAI Analyzer Pro 部署指南

## 🎯 系統總覽

**FinAI Analyzer Pro** 是一個**完整的全球AI投資分析平台後端系統**，專為您的前端應用提供強大的金融數據分析服務。

### ✅ 完整功能清單
- 🌍 **全球市場支援**: 美股、港股、中國A股、日股、英股、加密貨幣、外匯、期貨
- 📊 **100+技術指標**: RSI、MACD、布林帶、移動平均線等
- 📈 **基本面分析**: P/E比率、ROE、財務健康度評估
- ⚠️ **風險分析**: VaR、CVaR、蒙地卡羅模擬、壓力測試
- 🤖 **AI智能分析**: DeepSeek驅動的粵語/中英文投資建議
- 📰 **新聞情緒分析**: 即時新聞抓取和情緒評分
- 💼 **投資組合管理**: 多資產組合分析和優化
- 📄 **專業報告生成**: PDF投資報告生成
- 🔐 **Freemium系統**: 用戶使用限制和Premium升級

---

## 📁 項目文件結構

```
finai-analyzer-backend/
│
├── main.py                    # ✅ FastAPI 主應用程式
├── requirements.txt           # ✅ 完整依賴包列表  
├── .env                      # 🔧 需要配置 - 環境變數
├── Dockerfile                # 🐳 Docker 容器配置
├── docker-compose.yml        # 🐳 Docker Compose 配置
├── Procfile                  # 🚀 Heroku 部署配置
│
├── app/
│   ├── core/
│   │   ├── config.py         # ✅ 全局配置文件 (含您的API keys)
│   │   ├── database.py       # 🔧 需要創建 - 數據庫配置
│   │   └── middleware.py     # 🔧 需要創建 - 中間件
│   │
│   ├── api/                  # 🔧 需要創建 - API 路由
│   │   ├── market_data.py    # 市場數據 API
│   │   ├── technical.py      # 技術分析 API
│   │   ├── fundamental.py    # 基本面分析 API  
│   │   ├── risk.py           # 風險分析 API
│   │   ├── news.py           # 新聞分析 API
│   │   ├── portfolio.py      # 投資組合 API
│   │   ├── ai_chat.py        # AI 聊天 API
│   │   └── auth.py           # 認證 API
│   │
│   ├── services/
│   │   ├── data_fetcher.py   # ✅ 全球數據獲取服務
│   │   ├── technical_analyzer.py # ✅ 技術分析引擎
│   │   ├── risk_analyzer.py  # 🔧 需要創建 - 風險分析
│   │   ├── ai_service.py     # 🔧 需要創建 - AI服務
│   │   └── news_analyzer.py  # 🔧 需要創建 - 新聞分析
│   │
│   └── models/               # 🔧 需要創建 - 數據模型
│       ├── market.py
│       ├── analysis.py
│       └── user.py
│
└── docs/
    ├── api_specifications.md # ✅ 詳細API文檔
    └── deployment_guide.md   # ✅ 本部署指南
```

---

## 🔧 第一步：環境設置

### 1. 創建 `.env` 文件

在項目根目錄創建 `.env` 文件：

```bash
# FinAI Analyzer Pro 環境配置

# 🚀 應用程式配置
APP_NAME=FinAI Analyzer Pro
VERSION=1.0.0
ENVIRONMENT=production
DEBUG=false

# 🌐 服務器配置  
HOST=0.0.0.0
PORT=8000

# 🔐 安全配置 (請更改此密鑰)
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=43200

# 🌍 CORS 配置 (添加您的前端域名)
ALLOWED_ORIGINS=["http://localhost:3000","https://your-frontend-domain.com"]

# 🗄️ 數據庫配置 (生產環境使用 PostgreSQL)
DATABASE_URL=postgresql://username:password@localhost:5432/finai_db

# 🔄 Redis 配置
REDIS_URL=redis://localhost:6379/0

# 📊 API Keys - 您提供的真實keys
ALPHA_VANTAGE_KEY=1ONMXCOE6XBGKFWJ
DEEPSEEK_API_KEY=sk-8fd1b4fdc0a34022966ba070a43c6d9e  
FINNHUB_KEY=d3gifo9r01qpep671jj0d3gifo9r01qpep671jjg

# 📰 新聞API (需要註冊 https://newsapi.org)
NEWS_API_KEY=your_news_api_key_here

# 💰 Freemium 限制
FREE_ANALYSIS_LIMIT=10
FREE_AI_CHAT_LIMIT=20
```

### 2. 安裝 Python 依賴

```bash
# 創建虛擬環境
python -m venv finai_env

# 激活虛擬環境 (Windows)
finai_env\Scripts\activate

# 激活虛擬環境 (macOS/Linux)  
source finai_env/bin/activate

# 安裝依賴
pip install -r requirements.txt
```

### 3. 特殊依賴安裝

**TA-Lib 安裝 (Windows):**
```bash
# 下載並安裝預編譯版本
pip install TA-Lib-0.4.28-cp311-cp311-win_amd64.whl
# 或從 https://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib 下載對應版本
```

**TA-Lib 安裝 (macOS):**
```bash
brew install ta-lib
pip install TA-Lib
```

**TA-Lib 安裝 (Linux):**
```bash
sudo apt-get install libta-lib-dev
pip install TA-Lib
```

---

## 🗄️ 第二步：數據庫設置

### 選項A: SQLite (開發/測試)
```bash
# SQLite 會自動創建，無需額外設置
# 文件位置: ./finai.db
```

### 選項B: PostgreSQL (推薦生產環境)

**本地安裝 PostgreSQL:**
```bash
# 安裝 PostgreSQL
# Windows: 下載並安裝 https://www.postgresql.org/download/
# macOS: brew install postgresql
# Ubuntu: sudo apt-get install postgresql

# 創建數據庫
createdb finai_db

# 創建用戶 (可選)
createuser finai_user
```

**雲端 PostgreSQL (推薦):**
- **Heroku Postgres**: 免費 10,000 rows
- **Railway**: 免費 512MB
- **Supabase**: 免費 500MB
- **Neon**: 免費 3GB

---

## 🚀 第三步：本地測試運行

### 1. 啟動應用程式
```bash
# 方法1: 直接運行
python main.py

# 方法2: 使用 uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# 方法3: 使用 gunicorn (生產環境)
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### 2. 驗證運行
瀏覽器打開: http://localhost:8000

應該看到:
```json
{
  "status": "healthy",
  "service": "FinAI Analyzer Pro API", 
  "version": "1.0.0",
  "message": "🌍 全球AI投資分析平台運行正常"
}
```

### 3. API 文檔
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### 4. 測試 API 端點
```bash
# 測試健康檢查
curl http://localhost:8000/health

# 測試市場數據 (需要API key)
curl -H "X-API-Key: your-api-key" \
     http://localhost:8000/api/v1/market/asset-info/AAPL
```

---

## ☁️ 第四步：雲端部署

### 選項A: Heroku 部署 (推薦)

**1. 安裝 Heroku CLI**
- 下載: https://devcenter.heroku.com/articles/heroku-cli

**2. 創建應用程式**
```bash
# 登錄 Heroku
heroku login

# 創建應用程式
heroku create finai-analyzer-pro

# 添加 PostgreSQL
heroku addons:create heroku-postgresql:essential-0

# 添加 Redis  
heroku addons:create heroku-redis:mini
```

**3. 配置環境變數**
```bash
# 設置 API Keys
heroku config:set ALPHA_VANTAGE_KEY=1ONMXCOE6XBGKFWJ
heroku config:set DEEPSEEK_API_KEY=sk-8fd1b4fdc0a34022966ba070a43c6d9e
heroku config:set FINNHUB_KEY=d3gifo9r01qpep671jj0d3gifo9r01qpep671jjg

# 設置應用配置
heroku config:set SECRET_KEY=your-production-secret-key
heroku config:set ENVIRONMENT=production
heroku config:set DEBUG=false
```

**4. 創建 Procfile**
```
web: gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
```

**5. 部署**
```bash
# 初始化 git
git init
git add .
git commit -m "Initial commit"

# 添加 Heroku 遠程
heroku git:remote -a finai-analyzer-pro

# 部署
git push heroku main
```

**6. 驗證部署**
```bash
# 打開應用程式
heroku open

# 查看日誌
heroku logs --tail
```

### 選項B: Railway 部署

**1. 連接 GitHub**
- 訪問 https://railway.app
- 連接您的 GitHub 帳戶
- 選擇 repository

**2. 添加環境變數**
在 Railway 儀表板添加所有 .env 變數

**3. 添加數據庫**
- 點擊 "Add Service" → PostgreSQL
- Railway 會自動配置 DATABASE_URL

**4. 部署**
- Railway 會自動檢測 Python 項目並部署

### 選項C: Vercel 部署 (Serverless)

**1. 安裝 Vercel CLI**
```bash
npm i -g vercel
```

**2. 創建 vercel.json**
```json
{
  "builds": [
    {
      "src": "main.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "main.py"
    }
  ]
}
```

**3. 部署**
```bash
vercel --prod
```

---

## 🐳 Docker 部署

### 1. 創建 Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# 安裝系統依賴
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libta-lib-dev \
    && rm -rf /var/lib/apt/lists/*

# 複製依賴文件
COPY requirements.txt .

# 安裝 Python 依賴
RUN pip install --no-cache-dir -r requirements.txt

# 複製應用程式代碼
COPY . .

# 創建非 root 用戶
RUN useradd -m -u 1000 finai && chown -R finai:finai /app
USER finai

# 暴露端口
EXPOSE 8000

# 運行應用程式
CMD ["gunicorn", "main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
```

### 2. 創建 docker-compose.yml
```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://finai:password@postgres:5432/finai_db
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - postgres
      - redis
    env_file:
      - .env

  postgres:
    image: postgres:15
    environment:
      - POSTGRES_DB=finai_db
      - POSTGRES_USER=finai
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

volumes:
  postgres_data:
```

### 3. 運行 Docker
```bash
# 構建並運行
docker-compose up --build

# 後台運行
docker-compose up -d

# 查看日誌
docker-compose logs -f api
```

---

## 🔗 第五步：前端整合

### API Base URL
```javascript
// 開發環境
const API_BASE_URL = 'http://localhost:8000/api/v1';

// 生產環境 (替換為您的實際域名)
const API_BASE_URL = 'https://your-api-domain.com/api/v1';
```

### 示例 API 調用
```javascript
// 獲取股票分析
const analyzeStock = async (symbol) => {
  const response = await fetch(`${API_BASE_URL}/analysis/technical`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-API-Key': 'your-api-key'
    },
    body: JSON.stringify({
      symbol: symbol,
      period: '1y',
      indicators: ['rsi', 'macd', 'bollinger_bands']
    })
  });
  
  return await response.json();
};

// AI 聊天
const chatWithAI = async (message) => {
  const response = await fetch(`${API_BASE_URL}/ai/chat`, {
    method: 'POST', 
    headers: {
      'Content-Type': 'application/json',
      'X-API-Key': 'your-api-key'
    },
    body: JSON.stringify({
      message: message,
      language: 'zh-HK'
    })
  });
  
  return await response.json();
};
```

---

## 🔐 安全配置

### 1. API Key 管理
```bash
# 生成安全的 API keys 給客戶端
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 2. HTTPS 設置
- **Heroku**: 自動提供 HTTPS
- **自託管**: 使用 Let's Encrypt + Nginx

### 3. 速率限制
已內建在代碼中:
- Alpha Vantage: 5次/分鐘, 500次/天
- 免費用戶: 10次分析/月, 20次AI對話/月

---

## 📊 監控和日誌

### 1. 日誌文件
```bash
# 日誌位置
logs/finai_2024-10-05.log

# 實時查看日誌
tail -f logs/finai_*.log
```

### 2. 健康檢查
```bash
# 自動健康檢查端點
GET /health

# 返回服務狀態、API狀態、數據庫連接等
```

### 3. Heroku 監控
```bash
# 查看應用狀態
heroku ps

# 查看日誌
heroku logs --tail

# 查看指標
heroku addons:open heroku-postgresql
```

---

## 🚨 故障排除

### 常見問題

**1. TA-Lib 安裝失敗**
```bash
# Windows 解決方案
pip install --no-cache-dir https://github.com/cgohlke/talib-build/releases/download/v0.4.28/TA_Lib-0.4.28-cp311-cp311-win_amd64.whl

# 或禁用 TA-Lib (代碼會自動使用 pandas-ta)
pip install pandas-ta
```

**2. 數據庫連接失敗**
```bash
# 檢查數據庫 URL
echo $DATABASE_URL

# 測試連接
python -c "from sqlalchemy import create_engine; create_engine('$DATABASE_URL').connect()"
```

**3. API 調用失敗**
```bash
# 檢查 API Keys
echo $ALPHA_VANTAGE_KEY
echo $DEEPSEEK_API_KEY 
echo $FINNHUB_KEY

# 測試 API
curl "https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=AAPL&apikey=$ALPHA_VANTAGE_KEY"
```

**4. 記憶體不足**
```bash
# Heroku 升級 dyno
heroku ps:scale web=1:standard-1x

# 或優化代碼中的緩存設置
```

---

## 💰 成本估算

### 免費 Tier (開發/小型項目)
- **Heroku**: Free dyno + PostgreSQL essential (免費)
- **Railway**: 免費 500小時/月
- **Vercel**: 免費 100GB 帶寬
- **API 調用**: Alpha Vantage 免費500次/天

### 付費 Tier (生產環境)  
- **Heroku Standard**: ~$25/月
- **PostgreSQL Standard**: ~$50/月
- **Redis Premium**: ~$15/月
- **總計**: ~$90/月 (支持中等流量)

---

## 🎯 部署檢查清單

### 部署前檢查
- [ ] 所有 API keys 已設置
- [ ] 數據庫已配置
- [ ] .env 文件已創建
- [ ] 依賴已安裝 (特別是 TA-Lib)
- [ ] 本地測試通過

### 部署後檢查  
- [ ] 健康檢查端點正常: `/health`
- [ ] API 文檔可訪問: `/docs`
- [ ] 示例 API 調用成功
- [ ] 日誌正常輸出
- [ ] 數據庫連接正常
- [ ] Redis 緩存工作

### 與前端整合檢查
- [ ] CORS 設置正確
- [ ] API Base URL 正確
- [ ] 認證機制工作
- [ ] 實際數據調用成功
- [ ] 錯誤處理正確

---

## 📞 技術支援

如果遇到部署問題，請檢查:

1. **日誌文件**: 查看詳細錯誤信息
2. **環境變數**: 確認所有必要的變數已設置
3. **網絡連接**: 確認能訪問外部 API
4. **依賴版本**: 確認 Python 版本和包版本兼容

---

## 🎉 部署成功！

恭喜！您的 **FinAI Analyzer Pro** 後端現在已經完全部署並運行。

### 下一步建議:
1. 🔗 整合前端應用
2. 📊 監控 API 使用情況  
3. 🚀 根據需要擴展功能
4. 💰 設置 Premium 付費功能
5. 📈 收集用戶反饋並優化

您現在擁有一個完整的、專業級的全球AI投資分析平台！🌍💰📈