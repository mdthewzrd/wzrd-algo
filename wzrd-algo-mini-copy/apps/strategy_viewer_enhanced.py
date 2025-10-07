"""
Enhanced Strategy Viewer - Using Proper WZRD Chart Templates
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
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.chart_templates import CHART_TEMPLATES, CHART_STYLE
from utils.wzrd_mini_chart import create_chart

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Set page config for wide layout like WZRD chart viewer
st.set_page_config(
    page_title="Enhanced Strategy Viewer",
    page_icon="📈",
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
</style>
""", unsafe_allow_html=True)

def generate_mock_data_for_strategy(selected_ticker, signal_dates, start_date, end_date, chart_frequency, signals=None):
    """Generate mock data that matches WZRD chart format"""
    # Convert date objects to datetime objects if needed
    if hasattr(start_date, 'date'):
        start_date = datetime.combine(start_date, datetime.min.time())
    elif not isinstance(start_date, datetime):
        start_date = datetime.combine(start_date, datetime.min.time())

    if hasattr(end_date, 'date'):
        end_date = datetime.combine(end_date, datetime.min.time())
    elif not isinstance(end_date, datetime):
        end_date = datetime.combine(end_date, datetime.min.time())

    # Extend end_date to end of day
    end_date = end_date.replace(hour=23, minute=59, second=59)

    # Generate realistic trading data
    np.random.seed(hash(selected_ticker) % 1000)

    # Base price for ticker - if signals exist, use their price range as reference
    if signals and len(signals) > 0:
        # Extract actual signal prices to center our data around
        signal_prices = [float(s.get('price', 0)) for s in signals if s.get('price', 0) > 0]

        if signal_prices:
            # Use the average of signal prices as our base, this ensures perfect alignment
            base_price = sum(signal_prices) / len(signal_prices)
            print(f"🎯 Using signal-based price: ${base_price:.2f} (from {len(signal_prices)} signals)")
        else:
            # Fallback to default if no valid signal prices
            base_price = 660 if selected_ticker == 'SPY' else 400
    else:
        # Default prices when no signals
        base_prices = {
            'SPY': 575, 'QQQ': 480, 'IWM': 220, 'AAPL': 180, 'MSFT': 420,
            'GOOGL': 140, 'AMZN': 145, 'TSLA': 250, 'NVDA': 460, 'META': 320
        }
        base_price = base_prices.get(selected_ticker, np.random.uniform(100, 600))

    # Create date range
    if chart_frequency == "5min":
        freq_minutes = 5
    elif chart_frequency == "15min":
        freq_minutes = 15
    else:
        freq_minutes = 60

    current_time = start_date.replace(hour=4, minute=0, second=0, microsecond=0)
    data = []

    price = base_price
    total_days = (end_date - start_date).days + 1

    for day in range(total_days):
        day_date = current_time + timedelta(days=day)

        # Skip weekends
        if day_date.weekday() >= 5:
            continue

        # Generate bars for extended trading day (4:00 AM to 8:00 PM)
        # Pre-market: 4:00 AM - 9:30 AM
        # Regular: 9:30 AM - 4:00 PM
        # After-hours: 4:00 PM - 8:00 PM
        day_start = day_date.replace(hour=4, minute=0)
        day_end = day_date.replace(hour=20, minute=0)

        bar_time = day_start
        daily_return = np.random.normal(0.0005, 0.015)  # Small daily drift

        while bar_time < day_end:
            # Determine session type for volume and volatility adjustments
            hour = bar_time.hour
            minute = bar_time.minute

            if hour < 9 or (hour == 9 and minute < 30):
                # Pre-market (4:00 AM - 9:30 AM): Lower volume, higher volatility
                session_vol_multiplier = 0.3
                session_volatility = 0.004
            elif hour >= 16:
                # After-hours (4:00 PM - 8:00 PM): Lower volume, moderate volatility
                session_vol_multiplier = 0.4
                session_volatility = 0.0035
            else:
                # Regular hours (9:30 AM - 4:00 PM): Normal volume and volatility
                session_vol_multiplier = 1.0
                session_volatility = 0.003

            # Intraday price movement with session-specific volatility
            bar_return = np.random.normal(0, session_volatility)
            new_price = price * (1 + bar_return)

            # Generate OHLC with session-specific range
            if hour < 9 or hour >= 16:
                # Extended hours: Smaller ranges, more gaps
                range_pct = np.random.uniform(0.001, 0.004)
            else:
                # Regular hours: Normal ranges
                range_pct = np.random.uniform(0.002, 0.008)

            high = new_price * (1 + range_pct/2)
            low = new_price * (1 - range_pct/2)
            open_price = low + (high - low) * np.random.uniform(0.2, 0.8)
            close_price = low + (high - low) * np.random.uniform(0.2, 0.8)

            # Session-specific volume
            base_volume = np.random.uniform(500000, 3000000)
            volume = int(base_volume * session_vol_multiplier)

            data.append({
                'date': bar_time,
                'open': round(open_price, 2),
                'high': round(high, 2),
                'low': round(low, 2),
                'close': round(close_price, 2),
                'volume': volume
            })

            price = close_price
            bar_time += timedelta(minutes=freq_minutes)

    return pd.DataFrame(data)

def create_wzrd_chart_with_signals(strategy_artifact, selected_ticker, use_mock_data, start_date, end_date, chart_frequency="5min", template_config=None):
    """Create a proper WZRD chart with signals overlaid"""
    try:
        # Use default template if none provided
        if template_config is None:
            template_config = CHART_TEMPLATES["5min"]

        signals = strategy_artifact.get('signals', [])

        # Generate the base market data
        signal_dates = [pd.to_datetime(s['timestamp']) for s in signals] if signals else []
        df = generate_mock_data_for_strategy(selected_ticker, signal_dates, start_date, end_date, chart_frequency, signals)

        if df.empty:
            return None

        # Get template indicators
        indicators = template_config.get("indicators", {})

        # Map chart frequency to timeframe
        timeframe_map = {"5min": "5min", "15min": "15min", "1H": "hour"}
        timeframe = timeframe_map.get(chart_frequency, "5min")

        # Create the WZRD chart using the proper function
        # Use ALL available data for proper horizontal scaling
        display_bars = None  # Show all data to fill the chart width properly

        fig = create_chart(
            df=df,
            symbol=selected_ticker,
            timeframe=timeframe,
            display_bars=display_bars,
            show_vwap=indicators.get("vwap", True),
            show_prev_close=indicators.get("prev_close", True),
            show_920_bands=indicators.get("920_bands", True),
            show_920_cloud=indicators.get("920_cloud", True),
            show_7289_bands=indicators.get("7289_bands", timeframe in ["hour", "15min", "5min"]),
            show_7289_cloud=indicators.get("7289_cloud", timeframe in ["hour", "15min", "5min"]),
            zoom_to_candles=True  # Enable proper zoom to candle range
        )

        if fig is None:
            return None

        # Add signals as overlays
        if signals:
            print(f"🔍 DEBUG: Processing {len(signals)} signals")
            print(f"📊 Chart data range: {df['date'].min()} to {df['date'].max()}")
            print(f"💰 Chart price range: ${df['close'].min():.2f} to ${df['close'].max():.2f}")

            for i, signal in enumerate(signals):
                signal_time = pd.to_datetime(signal['timestamp'])
                signal_type = signal.get('type', 'unknown')
                signal_price = signal.get('price', 0)

                print(f"\n📍 Signal {i+1}:")
                print(f"   Time: {signal_time}")
                print(f"   Type: {signal_type}")
                print(f"   Price: ${signal_price}")

                # Check if signal time is within chart data range
                if signal_time < df['date'].min() or signal_time > df['date'].max():
                    print(f"   ⚠️  Signal time {signal_time} is OUTSIDE chart range!")
                    print(f"   📈 Chart range: {df['date'].min()} to {df['date'].max()}")

                # Check if signal price is reasonable
                if signal_price < df['close'].min() * 0.8 or signal_price > df['close'].max() * 1.2:
                    print(f"   ⚠️  Signal price ${signal_price} seems OUTSIDE normal price range!")
                    print(f"   📊 Chart price range: ${df['close'].min():.2f} to ${df['close'].max():.2f}")

                # If signal price is 0 or outside reasonable range, use nearby market price
                if signal_price <= 0 or signal_price < 400 or signal_price > 700:
                    # Find nearest price data point
                    time_diffs = abs(df['date'] - signal_time)
                    nearest_idx = time_diffs.argmin()
                    if nearest_idx < len(df):
                        signal_price = df.iloc[nearest_idx]['close']

                # Determine signal color and symbol
                print(f"DEBUG: Processing signal - type: '{signal_type}', direction: '{signal.get('direction', '')}'")

                # Handle both old format (entry_signal/exit_signal) and new format (entry_long/exit_long)
                if signal_type in ['entry_signal', 'entry_long']:
                    color = '#00FF00'  # Bright green
                    symbol = 'triangle-up'
                    marker_size = 15
                elif signal_type in ['exit_signal', 'exit_long', 'close_long']:
                    color = '#FFFF00'  # Bright yellow
                    symbol = 'x-thin'
                    marker_size = 18
                else:
                    color = 'white'
                    symbol = 'circle'
                    marker_size = 12
                    print(f"DEBUG: Signal fell into 'else' category - type: '{signal_type}'")

                # Add signal marker
                fig.add_trace(
                    go.Scatter(
                        x=[signal_time],
                        y=[signal_price],
                        mode='markers',
                        marker=dict(
                            color=color,
                            size=marker_size,
                            symbol=symbol,
                            line=dict(color='black', width=2)
                        ),
                        name=f"{signal_type}",
                        showlegend=False,
                        hovertemplate=f"<b>{signal.get('reason', 'Signal')}</b><br>" +
                                    f"Price: ${signal_price}<br>" +
                                    f"Time: {signal_time}<br>" +
                                    f"Type: {signal_type}<extra></extra>"
                    )
                )

        return fig

    except Exception as e:
        st.error(f"Error creating WZRD chart: {e}")
        return None

# Main UI
st.title("📊 Enhanced Strategy Viewer")
st.markdown("**Professional WZRD chart templates with strategy signals**")

# Chart template selection using WZRD templates
st.markdown("## 🎨 Chart Template")
chart_template = st.selectbox(
    "Choose timeframe template:",
    ["5min", "15min", "hour", "day"],
    index=0,
    help="Each template has optimized indicators and settings for that timeframe"
)

# Input section
st.markdown("## 📝 Input Strategy")
input_method = st.radio(
    "Choose input method:",
    ["Load Existing File", "Paste JSON"],
    horizontal=True
)

# Settings
st.markdown("## ⚙️ Chart Settings")
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    selected_ticker = st.selectbox("Ticker", ["SPY", "QQQ", "IWM", "AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "NVDA"], index=0)
    data_source = st.radio("Data Source", ["Mock Data", "Real Data"], index=0)

with col2:
    # Custom date range controls
    st.markdown("**Chart Date Range**")
    start_date = st.date_input("Start Date", value=datetime(2024, 10, 1).date())
    end_date = st.date_input("End Date", value=datetime(2024, 10, 3).date())
    chart_frequency = st.selectbox("Data Frequency", ["5min", "15min", "1H"], index=0)

with col3:
    api_key_status = '✅ Configured' if 'POLYGON_API_KEY' in os.environ else '❌ Missing'
    # Get template configuration
    template_config = CHART_TEMPLATES.get(chart_template, CHART_TEMPLATES["5min"])

    st.info(f"""
    **Ticker:** {selected_ticker}
    **Template:** {template_config["description"]}
    **Range:** {start_date} to {end_date}
    **Freq:** {chart_frequency}
    **API Key:** {api_key_status}
    """)

use_mock_data = data_source == "Mock Data"

# Strategy input
strategy_artifact = None

if input_method == "Load Existing File":
    # Get list of strategy files
    strategy_files = []
    try:
        for file in os.listdir('.'):
            if file.endswith('.json') and ('strategy' in file.lower() or 'signal' in file.lower()):
                strategy_files.append(file)
    except:
        pass

    if strategy_files:
        selected_file = st.selectbox("Select strategy file:", strategy_files)
        if st.button("Load Strategy"):
            try:
                with open(selected_file, 'r') as f:
                    strategy_artifact = json.load(f)
                st.success(f"✅ Loaded {selected_file}")
            except Exception as e:
                st.error(f"Error loading file: {e}")
    else:
        st.warning("No strategy files found in current directory")

else:  # Paste JSON
    strategy_json = st.text_area(
        "Paste strategy JSON:",
        height=200,
        help="Paste your strategy JSON here"
    )

    if st.button("Parse Strategy"):
        try:
            strategy_artifact = json.loads(strategy_json)
            st.success("✅ Strategy parsed successfully")
        except Exception as e:
            st.error(f"JSON parsing error: {e}")

# Generate chart
if strategy_artifact:
    st.markdown("## 📊 Strategy Chart")

    # Create chart based on selected template
    with st.spinner("Creating WZRD chart..."):
        fig = create_wzrd_chart_with_signals(strategy_artifact, selected_ticker, use_mock_data, start_date, end_date, chart_frequency, template_config)

        if fig:
            # Add strategy information
            st.info("📋 **Professional WZRD Chart**: Deviation bands, EMA clouds, and signal overlays")

            # Display the chart
            st.plotly_chart(fig, use_container_width=True, key="wzrd_chart")

            # Strategy statistics
            signals = strategy_artifact.get('signals', [])
            if signals:
                st.markdown("### 📊 Strategy Statistics")

                entry_signals = [s for s in signals if s.get('type') == 'entry_signal']
                exit_signals = [s for s in signals if s.get('type') == 'exit_signal']

                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.metric("Total Signals", len(signals))

                with col2:
                    st.metric("Entry Signals", len(entry_signals))

                with col3:
                    st.metric("Exit Signals", len(exit_signals))

                with col4:
                    total_pnl = sum([s.get('pnl', 0) for s in exit_signals])
                    st.metric("Total PnL", f"${total_pnl:.2f}")
        else:
            st.error("Failed to create chart")
else:
    st.info("👆 Load or paste a strategy to view the chart")