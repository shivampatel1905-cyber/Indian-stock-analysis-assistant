
import pandas as pd
from datetime import datetime
import sqlite3
from textblob import TextBlob
import feedparser
from urllib.parse import quote_plus
import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

def add_ticker_to_watchlist(ticker):

    conn = sqlite3.connect("watchlist.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS watchlist (
            ticker TEXT UNIQUE
        )
        """
    )

    cursor.execute(
        "INSERT OR IGNORE INTO watchlist VALUES (?)",
        (ticker,)
    )

    conn.commit()
    conn.close()


def remove_ticker_from_watchlist(ticker):

    conn = sqlite3.connect("watchlist.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM watchlist WHERE ticker = ?",
        (ticker,)
    )

    conn.commit()
    conn.close()

st.set_page_config(
    page_title="Indian Stock Analysis Assistant",
    layout="wide"
)

st.title("📈 Indian Stock Analysis Assistant")
st.caption(
    f"Last Updated: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}"
)

ticker = st.sidebar.text_input(
    "Enter NSE Ticker",
    value="RELIANCE.NS",
    help="Examples: RELIANCE.NS, TCS.NS, INFY.NS, YESBANK.NS"
)

# =====================
# WATCHLIST
# =====================

st.sidebar.subheader("📋 Watchlist")

new_ticker = st.sidebar.text_input(
    "Add Ticker",
    value=""
)

if st.sidebar.button("➕ Add"):

    if new_ticker:

        add_ticker_to_watchlist(
            new_ticker.upper()
        )

        st.rerun()

try:

    conn = sqlite3.connect("watchlist.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT ticker FROM watchlist"
    )

    rows = cursor.fetchall()

    conn.close()

    watchlist = [row[0] for row in rows]

    for stock in watchlist:

        col_a, col_b = st.sidebar.columns([3, 1])

        with col_a:
            st.write(stock)

        with col_b:

            if st.button(
                "❌",
                key=f"remove_{stock}"
            ):

                remove_ticker_from_watchlist(stock)

                st.rerun()

except Exception:
    st.sidebar.write("No watchlist found")

st.sidebar.subheader("⚖️ Compare Stocks")

compare_ticker = st.sidebar.text_input(
    "Compare With",
    value=""
)

st.success(f"Selected Ticker: {ticker}")

now = datetime.now()

current_hour = now.hour
current_minute = now.minute

market_open = (
    (current_hour > 9 or (current_hour == 9 and current_minute >= 15))
    and
    (current_hour < 15 or (current_hour == 15 and current_minute <= 30))
)

if market_open:
    st.success("🟢 NSE Market Open")

else:
    st.warning("🔴 NSE Market Closed")

try:

    # =====================
    # PRICE DATA
    # =====================

    df = yf.download(
        ticker,
        period="6mo",
        progress=False,
        auto_adjust=True
    )
    if df.empty:

        st.error(
            "❌ Invalid ticker symbol or no data available."
        )

        st.stop()

    close = df["Close"].squeeze()
    close = close.dropna()

    if len(close) == 0:

        st.error(
            "❌ Invalid ticker symbol or no price data available."
        )

        st.stop()

    

    current_price = float(close.iloc[-1])

    ma20 = float(
        close.rolling(20).mean().iloc[-1]
    )

    delta = close.diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(14).mean()
    avg_loss = loss.rolling(14).mean()

    rs = avg_gain / avg_loss

    rsi = float(
        (100 - (100 / (1 + rs))).iloc[-1]
    )

    # =====================
    # METRICS
    # =====================

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Current Price",
            f"₹{current_price:.2f}"
        )

    with col2:
        st.metric(
            "20-Day Moving Average",
            f"{ma20:.2f}"
        )

    with col3:
        st.metric(
            "RSI (14)",
            f"{rsi:.2f}"
        )

    # =====================
    # FUNDAMENTALS
    # =====================

    info = yf.Ticker(ticker).info

    market_cap = info.get("marketCap", "N/A")
    pe_ratio = info.get("trailingPE", "N/A")
    dividend_yield = info.get("dividendYield", "N/A")
    high_52 = info.get("fiftyTwoWeekHigh", "N/A")
    low_52 = info.get("fiftyTwoWeekLow", "N/A")

    st.subheader("📊 Fundamentals")

    col4, col5, col6 = st.columns(3)

    with col4:
        st.metric("P/E Ratio", pe_ratio)

    with col5:
        st.metric("52W High", high_52)

    with col6:
        st.metric("52W Low", low_52)

    # Market Cap Formatting

    if isinstance(market_cap, (int, float)):

        if market_cap >= 1e12:
            market_cap_display = f"₹{market_cap/1e12:.2f} Trillion"

        elif market_cap >= 1e9:
            market_cap_display = f"₹{market_cap/1e9:.2f} Billion"

        else:
            market_cap_display = str(market_cap)

    else:
        market_cap_display = market_cap

    st.write(f"**Market Cap:** {market_cap_display}")
    st.write(f"**Dividend Yield:** {dividend_yield}")

    # =====================
    # STOCK CHART
    # =====================

    st.subheader("📈 Stock Price Chart")

    chart_close = close

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=chart_close.index,
            y=chart_close.values,
            mode="lines",
            name=ticker
        )
    )

    if compare_ticker:
        
      

        compare_chart_df = yf.download(
            compare_ticker,
            period="6mo",
            progress=False,
            auto_adjust=True
        )

        compare_chart_close = (
            compare_chart_df["Close"]
            .squeeze()
            .dropna()
        )
        if len(compare_chart_close) == 0:

            st.warning(
                "⚠️ Invalid comparison ticker."
            )

        else:  

            fig.add_trace(
                go.Scatter(
                    x=compare_chart_close.index,
                    y=compare_chart_close.values,
                    mode="lines",
                    name=compare_ticker
                )
            )

    fig.update_layout(
        title="Stock Price Comparison",
        height=500,
        xaxis_title="Date",
        yaxis_title="Price (₹)",
        hovermode="x unified"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )
    # =====================
# STOCK COMPARISON
# =====================

    if compare_ticker:

        st.subheader("⚖️ Stock Comparison")

        compare_info = yf.Ticker(
             compare_ticker
        ).info

        compare_df = yf.download(
            compare_ticker,
            period="6mo",
            progress=False,
            auto_adjust=True
        )

        compare_close = (
            compare_df["Close"]
            .squeeze()
            .dropna()
        )

        compare_delta = compare_close.diff()

        compare_gain = compare_delta.clip(lower=0)
        compare_loss = -compare_delta.clip(upper=0)

        compare_avg_gain = compare_gain.rolling(14).mean()
        compare_avg_loss = compare_loss.rolling(14).mean()

        compare_rs = compare_avg_gain / compare_avg_loss

        compare_rsi = float(
            (100 - (100 / (1 + compare_rs))).iloc[-1]
        )

        compare_price = float(
           compare_close.iloc[-1]
        )

        compare_pe = compare_info.get(
            "trailingPE",
            "N/A"
        )

        compare_market_cap = compare_info.get(
            "marketCap",
            "N/A"
        )

        compare_high_52 = compare_info.get(
            "fiftyTwoWeekHigh",
            "N/A"
        )

        compare_low_52 = compare_info.get(
            "fiftyTwoWeekLow",
            "N/A"
        )

        compare_dividend = compare_info.get(
            "dividendYield",
            "N/A"
        )

        compare_market_cap = compare_info.get(
            "marketCap",
            "N/A"
        )
        if isinstance(compare_market_cap, (int, float)):

            if compare_market_cap >= 1e12:
                compare_market_cap_display = (
                    f"₹{compare_market_cap/1e12:.2f} Trillion"
                )

            elif compare_market_cap >= 1e9:
                compare_market_cap_display = (
                    f"₹{compare_market_cap/1e9:.2f} Billion"
                )

            else:
                compare_market_cap_display = (
                    str(compare_market_cap)
                )

        else:
            compare_market_cap_display = (
                compare_market_cap
            )

        compare_high_52 = compare_info.get(
            "fiftyTwoWeekHigh",
            "N/A"
        )

        compare_low_52 = compare_info.get(
            "fiftyTwoWeekLow",
            "N/A"
        )

        compare_dividend = compare_info.get(
            "dividendYield",
            "N/A"
        )

        col_a, col_b = st.columns(2)



        col_a, col_b = st.columns(2)

        with col_a:

            st.subheader(ticker)

            st.metric(
                "Current Price",
               f"₹{current_price:.2f}"
            )

            st.metric(
                "RSI",
                f"{rsi:.2f}"
            )

            st.metric(
               "PE Ratio",
               str(pe_ratio)
            )

            st.metric(
               "52W High",
               str(high_52)
            )

            st.metric(
               "52W Low",
               str(low_52)
            )

            st.metric(
               "Dividend Yield",
               str(dividend_yield)
            )

            st.metric(
               "Market Cap",
               market_cap_display
            )

        with col_b:

            st.subheader(compare_ticker)

            st.metric(
                "Current Price",
                f"₹{compare_price:.2f}"
            )

            st.metric(
                "RSI",
                f"{compare_rsi:.2f}"
            )

            st.metric(
                "PE Ratio",
                str(compare_pe)
            )

            st.metric(
                "52W High",
                str(compare_high_52)
            )

            st.metric(
                "52W Low",
                str(compare_low_52)
            )

            st.metric(
                "Dividend Yield",
                str(compare_dividend)
            )

            st.metric(
                "Market Cap",
                compare_market_cap_display
            )

        report_data = {
            "Metric": [
                "Current Price",
                "20-Day MA",
                "RSI",
                "PE Ratio",
                "52W High",
                "52W Low",
                "Dividend Yield"
           ],
            ticker: [
                current_price,
                ma20,
                rsi,
                pe_ratio,
                high_52,
                low_52,
                dividend_yield
           ]
         }

        if compare_ticker:

            report_data[compare_ticker] = [
                compare_price,
                "N/A",
                compare_rsi,
                compare_pe,
                compare_high_52,
                compare_low_52,
                compare_dividend
            ]

        report_df = pd.DataFrame(report_data)

        csv = report_df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            label="📄 Download Analysis Report",
            data=csv,
            file_name="stock_analysis_report.csv",
            mime="text/csv"
        )

        # =====================
    # NEWS HEADLINES
    # =====================

    st.subheader("📰 Latest News")

    company_name = ticker.replace(".NS", "")

    company_encoded = quote_plus(company_name)

    news_url = (
        f"https://news.google.com/rss/search?"
        f"q={company_encoded}&hl=en-IN&gl=IN&ceid=IN:en"
    )

    feed = feedparser.parse(news_url)

    if feed.entries:

        for entry in feed.entries[:5]:
            st.write("•", entry.title)

        headlines_text = " ".join(
            [entry.title for entry in feed.entries[:5]]
        )

        polarity = TextBlob(
            headlines_text
        ).sentiment.polarity

        st.subheader("🧠 News Sentiment")

        if polarity > 0.1:
            st.success("🟢 Positive")

        elif polarity < -0.1:
            st.error("🔴 Negative")

        else:
            st.warning("🟡 Neutral")

        st.write(f"Sentiment Score: {polarity:.3f}")

    else:
        st.write("No recent news found.")
    st.divider()

    st.caption(
        "For educational purposes only. "
        "Not investment advice."
    )

except Exception as e:
    st.error(f"Error: {e}")
