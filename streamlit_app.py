import streamlit as st
import os
from PIL import Image
import pandas as pd
import openai
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Load OpenRouter API Key securely
openrouter_api_key = st.secrets["openrouter"]["api_key"]
openai.api_key = openrouter_api_key
openai.api_base = "https://openrouter.ai/api/v1"

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
        ib_data = pd.read_csv("/mnt/data/ib_holdings.csv") if os.path.exists("/mnt/data/ib_holdings.csv") else None
        schwab_data = pd.read_csv("/mnt/data/schwab_holdings.csv") if os.path.exists("/mnt/data/schwab_holdings.csv") else None

        if ib_data is not None:
            st.write("### Interactive Brokers Holdings")
            st.dataframe(ib_data)

        if schwab_data is not None:
            st.write("### Charles Schwab Holdings")
            st.dataframe(schwab_data)

elif menu == "📈 Charts":
    st.subheader("Stock Performance Comparison")
    tickers = st.text_input("Enter ticker symbols separated by commas (e.g., AAPL,GOOG,NVDA)").upper().split(',')
    timeframe = st.selectbox("Select Timeframe", ["1M", "6M", "YTD", "1Y", "MAX"])

    def get_start_date(timeframe):
        today = datetime.today()
        if timeframe == "1M": return today - timedelta(days=30)
        elif timeframe == "6M": return today - timedelta(days=180)
        elif timeframe == "YTD": return datetime(today.year, 1, 1)
        elif timeframe == "1Y": return today - timedelta(days=365)
        else: return datetime(today.year - 5, 1, 1)

    start_date = get_start_date(timeframe)
    end_date = datetime.today()

    if tickers and tickers[0]:
        plt.figure(figsize=(12, 6))
        for ticker in tickers:
            data = yf.download(ticker.strip(), start=start_date, end=end_date)
            if not data.empty:
                plt.plot(data.index, data['Close'], label=ticker.strip())
        plt.title("Price History")
        plt.xlabel("Date")
        plt.ylabel("Price ($)")
        plt.legend()
        st.pyplot(plt)

elif menu == "💬 Chat":
    st.subheader("Ask DAJANIII Anything")
    user_input = st.text_area("Type your question about the market, a stock, or your portfolio:", height=100)
    if st.button("Ask") and user_input:
        with st.spinner("Thinking..."):
            response = openai.ChatCompletion.create(
                model="openchat/openchat-3.5-0106",
                messages=[
                    {"role": "system", "content": "You are DAJANIII, a smart financial assistant."},
                    {"role": "user", "content": user_input}
                ]
            )
            st.success(response.choices[0].message.content)

elif menu == "🔍 Stock Lookup":
    st.subheader("Find Stock Info")
    symbol = st.text_input("Enter Stock Symbol (e.g., AAPL, TSLA, GOOG)").upper()
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

        st.write("### Recent Price Chart")
        hist = stock.history(period="6mo")
        if not hist.empty:
            plt.figure(figsize=(10, 4))
            plt.plot(hist.index, hist['Close'])
            plt.title(f"{symbol} - Last 6 Months")
            plt.xlabel("Date")
            plt.ylabel("Close Price ($)")
            st.pyplot(plt)

        st.write("### News")
        for i, article in enumerate(info.get('news', [])[:5]):
            st.markdown(f"[{article['title']}]({article['link']})")
