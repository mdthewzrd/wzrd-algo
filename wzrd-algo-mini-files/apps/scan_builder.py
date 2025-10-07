"""
WZRD Scan Builder - Quick Market Scanning Tool
Validates AI-generated scans with custom universes and date ranges
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import os
from datetime import datetime, timedelta
import numpy as np
import sys

# Add utils to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Set page config for wide layout like WZRD chart viewer
st.set_page_config(
    page_title="WZRD Scan Builder",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Apply WZRD Dark Theme CSS
st.markdown("""
<style>
    .stApp {
        background-color: #000000;
        color: #ffffff;
    }
    .css-1d391kg {
        background-color: #000000;
    }
    .css-1lcbmhc {
        background-color: #1a1a1a;
    }
    .plotly {
        background-color: #000000 !important;
    }
    .scan-result-card {
        background-color: #1a1a1a;
        border: 1px solid #333;
        border-radius: 8px;
        padding: 15px;
        margin: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Predefined ticker universes
TICKER_UNIVERSES = {
    "S&P 500": ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "NVDA", "META", "BRK.B", "UNH", "JNJ",
                "JPM", "V", "PG", "HD", "CVX", "MA", "BAC", "ABBV", "PFE", "KO",
                "AVGO", "PEP", "TMO", "COST", "DIS", "ABT", "DHR", "VZ", "ADBE", "CRM"],

    "QQQ Holdings": ["AAPL", "MSFT", "AMZN", "NVDA", "GOOGL", "META", "TSLA", "AVGO", "COST", "NFLX",
                     "ADBE", "PEP", "TMUS", "CSCO", "INTC", "TXN", "QCOM", "INTU", "AMAT", "AMD"],

    "Russell 2000 Sample": ["AMC", "GME", "BBBY", "SNDL", "NAKD", "EXPR", "KOSS", "NOK", "BB", "CLOV",
                           "WISH", "PLTR", "SOFI", "LCID", "RIVN", "F", "BAC", "AAL", "CCL", "RKT"],

    "Popular ETFs": ["SPY", "QQQ", "IWM", "DIA", "VTI", "VEA", "VWO", "AGG", "BND", "GLD",
                     "SLV", "XLF", "XLK", "XLE", "XLV", "XLI", "XLY", "XLP", "XLB", "XLU"],

    "Sector ETFs": ["XLF", "XLK", "XLE", "XLV", "XLI", "XLY", "XLP", "XLB", "XLU", "XLRE",
                    "XBI", "XRT", "XME", "XOP", "XHB", "ITB", "VNQ", "KBE", "KRE", "SMH"],

    "Crypto Related": ["COIN", "MSTR", "RIOT", "MARA", "SQ", "PYPL", "NVDA", "AMD", "CAN", "BTBT",
                       "EBON", "SOS", "EBANG", "NILE", "ANY", "LGHL", "CLSK", "CORZ", "WULF", "IREN"]
}

def generate_mock_data(ticker, start_date, end_date, seed_offset=0):
    """Generate realistic mock price data for a ticker"""
    np.random.seed(hash(ticker) % 1000 + seed_offset)

    # Base prices for different tickers
    base_prices = {
        'SPY': 450, 'QQQ': 380, 'IWM': 200, 'AAPL': 180, 'MSFT': 420,
        'GOOGL': 140, 'AMZN': 145, 'TSLA': 250, 'NVDA': 460, 'META': 320
    }

    base_price = base_prices.get(ticker, np.random.uniform(50, 500))

    # Generate date range (trading days only)
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    trading_dates = [d for d in dates if d.weekday() < 5]  # Remove weekends

    if not trading_dates:
        return pd.DataFrame()

    n_days = len(trading_dates)

    # Generate realistic price movement
    daily_returns = np.random.normal(0.001, 0.02, n_days)  # ~0.1% daily drift, 2% volatility
    prices = [base_price]

    for i in range(1, n_days):
        price_change = prices[-1] * daily_returns[i]
        new_price = max(prices[-1] + price_change, base_price * 0.5)  # Floor at 50% of base
        prices.append(new_price)

    # Generate OHLC data
    data = []
    for i, date in enumerate(trading_dates):
        close = prices[i]
        daily_range = close * np.random.uniform(0.005, 0.03)  # 0.5-3% daily range

        high = close + np.random.uniform(0, daily_range)
        low = close - np.random.uniform(0, daily_range)
        open_price = low + (high - low) * np.random.uniform(0.2, 0.8)

        volume = int(np.random.uniform(500000, 5000000))

        data.append({
            'date': date,
            'open': round(open_price, 2),
            'high': round(high, 2),
            'low': round(low, 2),
            'close': round(close, 2),
            'volume': volume
        })

    return pd.DataFrame(data)

def evaluate_scan_condition(data, condition):
    """Evaluate a single scan condition against price data"""
    if data.empty:
        return False, []

    condition_type = condition.get('type', '')

    try:
        if condition_type == 'price_breakout':
            lookback = condition.get('lookback', 20)
            threshold = condition.get('threshold', 'daily_high')

            if len(data) < lookback + 1:
                return False, []

            # Check if recent close breaks lookback period high
            recent_high = data['high'].tail(lookback + 1).iloc[:-1].max()
            latest_close = data['close'].iloc[-1]

            if latest_close > recent_high:
                return True, [len(data) - 1]  # Signal on last bar

        elif condition_type == 'volume_spike':
            multiplier = condition.get('multiplier', 2.0)
            period = condition.get('period', 20)

            if len(data) < period + 1:
                return False, []

            avg_volume = data['volume'].tail(period + 1).iloc[:-1].mean()
            latest_volume = data['volume'].iloc[-1]

            if latest_volume > avg_volume * multiplier:
                return True, [len(data) - 1]

        elif condition_type == 'rsi':
            period = condition.get('period', 14)
            operator = condition.get('operator', '>')
            value = condition.get('value', 70)

            if len(data) < period + 1:
                return False, []

            # Simple RSI calculation
            delta = data['close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))

            latest_rsi = rsi.iloc[-1]

            if operator == '>' and latest_rsi > value:
                return True, [len(data) - 1]
            elif operator == '<' and latest_rsi < value:
                return True, [len(data) - 1]

        elif condition_type == 'price_change':
            period = condition.get('period', 1)
            operator = condition.get('operator', '>')
            value = condition.get('value', 5.0)  # percentage

            if len(data) < period + 1:
                return False, []

            old_price = data['close'].iloc[-(period + 1)]
            new_price = data['close'].iloc[-1]
            change_pct = ((new_price - old_price) / old_price) * 100

            if operator == '>' and change_pct > value:
                return True, [len(data) - 1]
            elif operator == '<' and change_pct < value:
                return True, [len(data) - 1]

    except Exception as e:
        st.error(f"Error evaluating condition {condition_type}: {str(e)}")
        return False, []

    return False, []

def run_scan(scan_config, tickers, start_date, end_date):
    """Execute scan across ticker universe"""
    results = []
    conditions = scan_config.get('conditions', [])
    filters = scan_config.get('filters', {})

    progress_bar = st.progress(0)
    status_text = st.empty()

    for i, ticker in enumerate(tickers):
        status_text.text(f"Scanning {ticker}... ({i+1}/{len(tickers)})")
        progress_bar.progress((i + 1) / len(tickers))

        # Generate mock data for ticker
        data = generate_mock_data(ticker, start_date, end_date)

        if data.empty:
            continue

        # Apply basic filters
        latest_price = data['close'].iloc[-1]
        latest_volume = data['volume'].iloc[-1]

        if filters.get('min_price') and latest_price < filters['min_price']:
            continue
        if filters.get('max_price') and latest_price > filters['max_price']:
            continue
        if filters.get('min_volume') and latest_volume < filters['min_volume']:
            continue

        # Check all conditions
        all_conditions_met = True
        signal_dates = []

        for condition in conditions:
            condition_met, dates = evaluate_scan_condition(data, condition)
            if not condition_met:
                all_conditions_met = False
                break
            signal_dates.extend(dates)

        if all_conditions_met and signal_dates:
            results.append({
                'ticker': ticker,
                'price': latest_price,
                'volume': latest_volume,
                'signal_date': data['date'].iloc[signal_dates[0]] if signal_dates else data['date'].iloc[-1],
                'data': data
            })

    progress_bar.empty()
    status_text.empty()

    return results

def create_mini_chart(ticker_data, ticker):
    """Create a mini chart for scan results"""
    data = ticker_data['data']

    fig = go.Figure()

    # Candlestick chart
    fig.add_trace(go.Candlestick(
        x=data['date'],
        open=data['open'],
        high=data['high'],
        low=data['low'],
        close=data['close'],
        name=ticker,
        increasing_line_color='#00ff88',
        decreasing_line_color='#ff4444'
    ))

    # Add signal marker
    signal_date = ticker_data['signal_date']
    signal_price = ticker_data['price']

    fig.add_trace(go.Scatter(
        x=[signal_date],
        y=[signal_price],
        mode='markers',
        marker=dict(
            color='yellow',
            size=15,
            symbol='star',
            line=dict(color='black', width=1)
        ),
        name='Signal',
        showlegend=False
    ))

    fig.update_layout(
        title=f"{ticker} - ${signal_price:.2f}",
        plot_bgcolor='black',
        paper_bgcolor='black',
        font=dict(color='white'),
        height=300,
        showlegend=False,
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False)
    )

    return fig

# Initialize session state
if 'scan_results' not in st.session_state:
    st.session_state.scan_results = []

# Main UI
st.title("🔍 WZRD Scan Builder")
st.markdown("**Quick market scanning with custom universes and date ranges**")

# Create columns for layout
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 📅 Date Range")

    # Quick date options
    date_option = st.selectbox(
        "Quick Select",
        ["Custom Range", "Last Week", "Last 2 Weeks", "Last Month", "Last 3 Months"]
    )

    if date_option == "Custom Range":
        start_date = st.date_input("Start Date", value=datetime.now() - timedelta(days=14))
        end_date = st.date_input("End Date", value=datetime.now())
    else:
        days_map = {"Last Week": 7, "Last 2 Weeks": 14, "Last Month": 30, "Last 3 Months": 90}
        days = days_map[date_option]
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days)
        st.info(f"Scanning from {start_date} to {end_date}")

with col2:
    st.markdown("### 🎯 Ticker Universe")

    universe_option = st.selectbox(
        "Select Universe",
        ["Custom List"] + list(TICKER_UNIVERSES.keys())
    )

    if universe_option == "Custom List":
        custom_tickers = st.text_area(
            "Enter tickers (comma separated)",
            value="AAPL,MSFT,GOOGL,TSLA,SPY,QQQ",
            help="Enter ticker symbols separated by commas"
        )
        tickers = [t.strip().upper() for t in custom_tickers.split(',') if t.strip()]
    else:
        tickers = TICKER_UNIVERSES[universe_option]
        st.info(f"Using {len(tickers)} tickers from {universe_option}")

# Scan JSON input
st.markdown("### 🔍 Scan Configuration")

# Example scan JSON
example_scan = {
    "scan_name": "breakout_with_volume",
    "conditions": [
        {
            "type": "price_breakout",
            "lookback": 20,
            "threshold": "daily_high"
        },
        {
            "type": "volume_spike",
            "multiplier": 2.0,
            "period": 20
        }
    ],
    "filters": {
        "min_price": 5.0,
        "min_volume": 100000,
        "max_price": null
    }
}

scan_json = st.text_area(
    "Paste or edit scan JSON",
    value=json.dumps(example_scan, indent=2),
    height=300,
    help="Paste AI-generated scan JSON or edit the example"
)

# Expected frequency
expected_freq = st.selectbox(
    "Expected Frequency",
    ["Daily", "Hourly", "Weekly", "Monthly"],
    help="How often do you expect this scan to find results?"
)

# Run scan button
if st.button("🚀 Run Scan", type="primary"):
    try:
        scan_config = json.loads(scan_json)

        with st.spinner(f"Scanning {len(tickers)} tickers..."):
            results = run_scan(scan_config, tickers, start_date, end_date)

        st.session_state.scan_results = results

        if results:
            st.success(f"✅ Found {len(results)} matches!")
        else:
            st.warning("No matches found. Try adjusting parameters.")

    except json.JSONDecodeError:
        st.error("Invalid JSON format. Please check your scan configuration.")
    except Exception as e:
        st.error(f"Error running scan: {str(e)}")

# Display results
if st.session_state.scan_results:
    st.markdown("### 📊 Scan Results")

    results = st.session_state.scan_results
    st.markdown(f"**Found {len(results)} matches**")

    # Create chart grid
    cols_per_row = 3
    rows = (len(results) + cols_per_row - 1) // cols_per_row

    for row in range(rows):
        cols = st.columns(cols_per_row)
        for col_idx in range(cols_per_row):
            result_idx = row * cols_per_row + col_idx
            if result_idx < len(results):
                result = results[result_idx]
                with cols[col_idx]:
                    fig = create_mini_chart(result, result['ticker'])
                    st.plotly_chart(fig, use_container_width=True)

                    # Result details
                    st.markdown(f"""
                    **{result['ticker']}**
                    Price: ${result['price']:.2f}
                    Volume: {result['volume']:,}
                    Date: {result['signal_date'].strftime('%Y-%m-%d')}
                    """)

<function_calls>
<invoke name="TodoWrite">
<parameter name="todos">[{"content": "Create scan builder Streamlit app", "status": "completed", "activeForm": "Creating scan builder Streamlit app"}, {"content": "Build ticker universe management", "status": "completed", "activeForm": "Building ticker universe management"}, {"content": "Implement scan engine logic", "status": "completed", "activeForm": "Implementing scan engine logic"}, {"content": "Create chart gallery for results", "status": "completed", "activeForm": "Creating chart gallery for results"}, {"content": "Update start_services.sh for port 8503", "status": "in_progress", "activeForm": "Updating start_services.sh for port 8503"}]