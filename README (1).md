# Indian Stock Analysis Assistant

# Indian Stock Analysis Assistant

## Overview

Indian Stock Analysis Assistant is a Streamlit-based web application designed to help investors and students analyze Indian stocks listed on the National Stock Exchange (NSE).

The application provides technical indicators, fundamental analysis, news sentiment analysis, watchlist management, stock comparison, and downloadable reports through an interactive dashboard.

---

## Features

### Market Data

* Live NSE stock prices
* Historical stock data using Yahoo Finance
* Interactive stock price charts

### Technical Analysis

* 20-Day Moving Average (MA20)
* Relative Strength Index (RSI-14)
* Market status indicator (Open/Closed)

### Fundamental Analysis

* Market Capitalization
* P/E Ratio
* Dividend Yield
* 52-Week High
* 52-Week Low

### News & Sentiment Analysis

* Latest company-related news headlines
* Sentiment analysis of news articles
* Positive, Neutral, and Negative sentiment classification

### Watchlist Management

* Add stocks to watchlist
* Remove stocks from watchlist
* Persistent storage using SQLite

### Stock Comparison

* Compare two NSE-listed stocks
* Price comparison
* RSI comparison
* P/E comparison
* Dividend Yield comparison
* Market Cap comparison
* Comparative stock price chart

### Report Generation

* Download stock analysis results as CSV reports

---

## Technology Stack

### Frontend

* Streamlit

### Backend

* Python

### Data Sources

* Yahoo Finance (yfinance)
* Google News RSS Feed

### Libraries Used

* pandas
* yfinance
* plotly
* feedparser
* textblob
* sqlite3
* streamlit

---

## System Architecture

User Input (Ticker Symbol)

↓

Streamlit Dashboard

↓

Data Collection Layer

(yfinance + Google News RSS)

↓

Analysis Layer

(RSI, Moving Average, Fundamentals, Sentiment)

↓

Visualization Layer

(Plotly Charts + Streamlit Components)

↓

Report Generation & Watchlist Management

---

## Installation

### Clone Repository

```bash
git clone https://github.com/shivampatel1905-cyber/Indian-stock-analysis-assistant.git
```

### Move Into Project Folder

```bash
cd indian-stock-analysis-assistant
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Application

```bash
streamlit run app.py
```

---

## Usage

1. Enter an NSE ticker symbol (e.g., RELIANCE.NS).
2. View stock price, RSI, and moving average.
3. Analyze company fundamentals.
4. Read latest news and sentiment analysis.
5. Add or remove stocks from watchlist.
6. Compare stocks side-by-side.
7. Download stock analysis reports as CSV files.

---

## Future Improvements

* Portfolio Analysis Module
* AI-Based Investment Recommendations
* Multiple Technical Indicators (MACD, Bollinger Bands)
* Mutual Fund Analysis
* Candlestick Pattern Recognition
* Email Report Generation
* Cloud Database Integration

---

## Disclaimer

This project is developed for educational and academic purposes only.

The information provided by the application should not be considered financial or investment advice. Users should conduct their own research before making investment decisions.

---

## Author

Shivam Patel

M.Tech, Mechanical Engineering

Indian Institute of Technology Guwahati
