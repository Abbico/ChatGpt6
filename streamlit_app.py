
import streamlit as st
import os
from PIL import Image
import pandas as pd
import requests
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Load OpenRouter API Key securely
openrouter_api_key = st.secrets["openrouter"]["api_key"]

# Set page config
st.set_page_config(page_title="DAJANIII Pro", layout="wide")

# Sidebar navigation
st.sidebar.title("📂 Navigation")
menu = st.sidebar.radio("Go to", ["📊 Portfolio", "📈 Charts", "💬 Chat", "🔍 Stock Lookup"])

# Load and display logo
logo_path = os.path.join("assets", "logo.png")
if os.path.exists(logo_path):
    st.image(logo_path, width=200)

st.title("🧠 DAJANIII - AI Portfolio Assistant")

if menu == "📊 Portfolio":
    st.subheader("Your Portfolio Overview")
    st.info("Upload your portfolio (PDF/CSV) to view performance metrics.")
    uploaded_file = st.file_uploader("Upload Portfolio File", type=["pdf", "csv"])
    if uploaded_file:
        st.success("Portfolio uploaded. Parsing will be displayed below.")
        df = None
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith(".pdf"):
            import fitz
            text = ""
            with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
                for page in doc:
                    text += page.get_text()
            st.text_area("Extracted Text (Preview)", text[:3000], height=300)
        if df is not None:
            st.dataframe(df)

elif menu == "📈 Charts":
    st.subheader("Stock Performance Comparison")
    tickers = st.text_input("Enter ticker symbols (comma separated)", "AAPL,MSFT,NVDA").upper().split(',')
    view = st.radio("View By", ["Price", "% Change"])
    timeframe = st.selectbox("Timeframe", ["1D", "5D", "1M", "6M", "YTD", "1Y", "MAX"])

    def get_start_date(tf):
        today = datetime.today()
        if tf == "1D": return today - timedelta(days=1)
        if tf == "5D": return today - timedelta(days=5)
        if tf == "1M": return today - timedelta(days=30)
        if tf == "6M": return today - timedelta(days=180)
        if tf == "YTD": return datetime(today.year, 1, 1)
        if tf == "1Y": return today - timedelta(days=365)
        return today - timedelta(days=1825)

    start = get_start_date(timeframe)
    end = datetime.today()

    plt.figure(figsize=(12, 6))
    for ticker in tickers:
        data = yf.download(ticker.strip(), start=start, end=end)
        if not data.empty:
            if view == "% Change":
                pct_change = (data["Close"] / data["Close"].iloc[0] - 1) * 100
                plt.plot(data.index, pct_change, label=ticker.strip())
            else:
                plt.plot(data.index, data["Close"], label=ticker.strip())
    plt.title(f"{view} over time")
    plt.xlabel("Date")
    plt.ylabel(view)
    plt.legend()
    st.pyplot(plt)

elif menu == "💬 Chat":
    st.subheader("Ask DAJANIII Anything")
    user_input = st.text_area("Your question:", height=100)
    if st.button("Ask") and user_input:
        with st.spinner("Thinking..."):
            headers = {
                "Authorization": f"Bearer {openrouter_api_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "openchat/openchat-3.5-0106",
                "messages": [
                    {"role": "system", "content": "You are DAJANIII, a smart financial assistant."},
                    {"role": "user", "content": user_input}
                ]
            }
            res = requests.post("https://openrouter.ai/api/v1/chat/completions", json=payload, headers=headers)
            if res.status_code == 200:
                st.write(res.json()["choices"][0]["message"]["content"])
            else:
                st.error("Error fetching response from OpenRouter")

elif menu == "🔍 Stock Lookup":
    st.subheader("Find Stock Info")
    symbol = st.text_input("Enter Stock Symbol", "AAPL").upper()
    if symbol:
        stock = yf.Ticker(symbol)
        info = stock.info
        st.markdown(f"### {info.get('shortName', symbol)} ({symbol})")
        st.metric("Current Price", f"${info.get('currentPrice', 'N/A')}")
        st.metric("Market Cap", f"${info.get('marketCap', 'N/A'):,}")
        st.metric("PE Ratio", info.get('trailingPE', 'N/A'))
        st.metric("EPS", info.get('trailingEps', 'N/A'))
        st.metric("52 Week High", f"${info.get('fiftyTwoWeekHigh', 'N/A')}")
        st.metric("52 Week Low", f"${info.get('fiftyTwoWeekLow', 'N/A')}")
        hist = stock.history(period="6mo")
        if not hist.empty:
            plt.figure(figsize=(10, 4))
            plt.plot(hist.index, hist["Close"])
            plt.title(f"{symbol} - Last 6 Months")
            plt.xlabel("Date")
            plt.ylabel("Close Price ($)")
            st.pyplot(plt)
