# DAJANIII - AI Portfolio Assistant

## Features
- Upload and parse PDF/CSV portfolios (IB + Schwab)
- Compare stocks using live charts (price or % change)
- Real-time stock lookup with fundamentals, chart, and news
- AI-powered chat via OpenRouter

## Deployment (Streamlit Cloud)
1. Upload to GitHub
2. Go to https://streamlit.io/cloud → New App → point to `streamlit_app.py`
3. Add secrets:
```
[openrouter]
api_key = "your-api-key"
```
