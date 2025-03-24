
# DAJANIII Pro - Stock Trading & Portfolio Intelligence App 📈🤖

DAJANIII Pro is a powerful, AI-enhanced stock trading and portfolio assistant. Built with Streamlit, this app enables intelligent analysis, tax-aware hedging strategies, live news, and technical signals — all from uploaded portfolio PDFs.

## 🌟 Features

- 🔐 Secure OpenRouter AI integration (default, can switch to OpenAI in settings)
- 📄 Upload **PDF portfolios** (auto-parse and extract positions)
- 📊 Combine multiple portfolios into one unified dashboard
- 📈 Interactive charts and sector analysis
- 💬 AI Chat assistant for personalized strategy
- 📰 Latest stock news and political market headlines
- 📌 Click any stock for:
  - Fundamentals
  - Latest news
  - Buy/Sell/Hold recommendations
  - Technical indicators (RSI, MACD, MA)
  - Hedging and tax-sensitive strategy suggestions
- 🌎 Real-time index and crypto market data
- ⚙️ User settings: risk tolerance, tax profile, AI provider

## 🚀 How to Use

1. **Install dependencies**  
```bash
pip install -r requirements.txt
```

2. **Run the app locally**  
```bash
streamlit run streamlit_app.py
```

3. **Deploy to Streamlit Cloud**  
Push this to your GitHub repo and deploy using [https://streamlit.io/cloud](https://streamlit.io/cloud)

## 🧠 OpenRouter API Key

The app uses OpenRouter by default. Your key is stored securely in the code (ghosted) and can be changed in Settings.  
To use OpenAI, toggle the setting and input your OpenAI key.

## 📂 Folder Structure

```
dajaniii_pro_final/
├── streamlit_app.py
├── README.md
├── sample_data/
└── assets/
    └── logo.png
```

## 👨‍💻 Created by Zapher Dajani

All rights reserved © 2025 — DAJANIII™
