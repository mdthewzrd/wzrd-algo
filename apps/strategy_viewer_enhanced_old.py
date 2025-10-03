"""
Enhanced Strategy Viewer - Multiple Chart Layouts with WZRD Chart Styles
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
from utils.wzrd_mini_chart import create_chart, calculate_ema, calculate_atr, calculate_vwap, calculate_920_deviation_bands, calculate_atr_deviation_bands, calculate_deviation_bands

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

def create_wzrd_chart(strategy_artifact, selected_ticker, use_mock_data, chart_days=7, chart_frequency="5min", template_config=None):
    """Create a proper WZRD-style chart using the actual chart implementation"""
    try:
        # Use default template if none provided
        if template_config is None:
            template_config = CHART_TEMPLATES["5min"]

        signals = strategy_artifact.get('signals', [])
        if not signals:
            return None

        # Generate mock price data based on chart_days
        signal_dates = [pd.to_datetime(s['timestamp']) for s in signals]
        if signal_dates:
            # Use signal dates but extend by chart_days
            start_date = max(min(signal_dates) - timedelta(days=1),
                           max(signal_dates) - timedelta(days=chart_days))
            end_date = max(signal_dates) + timedelta(hours=2)
        else:
            # Fallback if no signals
            end_date = datetime.now()
            start_date = end_date - timedelta(days=chart_days)

        # Generate MUCH denser data to match WZRD professional charts
        # For 7 days, we need LOTS of data points for proper density

        # Calculate total bars needed for professional density
        if chart_frequency == "5min":
            # 5min: 12 bars/hour * 6.5 hours * 7 days = ~546 bars
            total_bars = chart_days * 78  # 78 bars per trading day
            freq_minutes = 5
        elif chart_frequency == "15min":
            # 15min: 4 bars/hour * 6.5 hours * 7 days = ~182 bars
            total_bars = chart_days * 26  # 26 bars per trading day
            freq_minutes = 15
        else:
            # 1H: 6.5 bars/day * 7 days = ~46 bars
            total_bars = chart_days * 7  # 7 bars per trading day
            freq_minutes = 60

        # Create dense time series matching professional charts
        current_time = start_date.replace(hour=9, minute=30, second=0, microsecond=0)
        date_range = []

        days_added = 0
        while days_added < chart_days:
            # Skip weekends
            if current_time.weekday() < 5:  # Monday=0, Friday=4
                # Add trading day bars (9:30 AM to 4:00 PM)
                day_start = current_time.replace(hour=9, minute=30)
                day_end = current_time.replace(hour=16, minute=0)

                bar_time = day_start
                while bar_time < day_end:
                    date_range.append(bar_time)
                    bar_time += timedelta(minutes=freq_minutes)

                days_added += 1

            current_time += timedelta(days=1)

        # Ensure we have the right amount of data
        date_range = date_range[:total_bars] if len(date_range) > total_bars else date_range

        np.random.seed(42)
        base_price = 450.0 if selected_ticker == 'QQQ' else (550.0 if selected_ticker == 'SPY' else 225.0)
        n_points = len(date_range)

        # Generate realistic price movement with proper volatility
        returns = np.random.normal(0, 0.001, n_points)  # Professional volatility
        prices = [base_price]
        for i in range(1, n_points):
            new_price = prices[-1] * (1 + returns[i])
            prices.append(new_price)

        # Create OHLC data with indicators
        data = []
        for i, (date, price) in enumerate(zip(date_range, prices)):
            high = price * (1 + abs(np.random.normal(0, 0.002)))
            low = price * (1 - abs(np.random.normal(0, 0.002)))
            open_price = prices[i-1] if i > 0 else price
            close_price = price

            # Add indicators - proper EMA calculation based on 5min template
            alpha_9 = 2.0 / (9 + 1)
            alpha_20 = 2.0 / (20 + 1)
            alpha_7 = 2.0 / (7 + 1)
            alpha_28 = 2.0 / (28 + 1)
            alpha_89 = 2.0 / (89 + 1)

            volume = np.random.randint(1000000, 5000000)

            # Calculate VWAP (Volume Weighted Average Price)
            if i == 0:
                ema9 = price
                ema20 = price
                ema7 = price
                ema28 = price
                ema89 = price
                cumulative_volume = volume
                cumulative_pv = price * volume
                vwap = price
                prev_close = price
            else:
                ema9 = alpha_9 * price + (1 - alpha_9) * data[i-1]['ema9']
                ema20 = alpha_20 * price + (1 - alpha_20) * data[i-1]['ema20']
                ema7 = alpha_7 * price + (1 - alpha_7) * data[i-1]['ema7']
                ema28 = alpha_28 * price + (1 - alpha_28) * data[i-1]['ema28']
                ema89 = alpha_89 * price + (1 - alpha_89) * data[i-1]['ema89']

                # VWAP calculation
                cumulative_volume = data[i-1]['cumulative_volume'] + volume
                cumulative_pv = data[i-1]['cumulative_pv'] + (price * volume)
                vwap = cumulative_pv / cumulative_volume

                # Previous day's close (simplified as previous close)
                prev_close = data[i-1]['close'] if date.date() != data[i-1]['date'].date() else data[i-1]['prev_close']

            # Calculate deviation bands (simplified as 2.5 * ATR approximation)
            atr_approx = abs(high - low) * 0.01  # Simplified ATR
            ema920_upper = ema20 + (2.5 * atr_approx)
            ema920_lower = ema20 - (2.5 * atr_approx)
            ema7289_upper = ema89 + (2.5 * atr_approx)
            ema7289_lower = ema89 - (2.5 * atr_approx)

            rsi = 50 + np.random.normal(0, 15)

            data.append({
                'date': date,
                'open': open_price,
                'high': max(open_price, close_price, high),
                'low': min(open_price, close_price, low),
                'close': close_price,
                'ema9': ema9,
                'ema20': ema20,
                'ema7': ema7,
                'ema28': ema28,
                'ema89': ema89,
                'vwap': vwap,
                'prev_close': prev_close,
                'ema920_upper': ema920_upper,
                'ema920_lower': ema920_lower,
                'ema7289_upper': ema7289_upper,
                'ema7289_lower': ema7289_lower,
                'cumulative_volume': cumulative_volume,
                'cumulative_pv': cumulative_pv,
                'volume': volume,
                'rsi': max(0, min(100, rsi))
            })

        df = pd.DataFrame(data)

        # Create subplots based on template configuration
        indicators = template_config.get("indicators", {})

        # Always have price chart, add volume if needed
        if indicators.get("vwap", False) or any([indicators.get("920_bands"), indicators.get("7289_bands")]):
            # Full chart with price, volume, and RSI
            fig = make_subplots(
                rows=3, cols=1,
                subplot_titles=[f"{selected_ticker} - {template_config['description']}", "Volume", "RSI"],
                vertical_spacing=0.05,
                row_heights=[0.6, 0.2, 0.2]
            )
        else:
            # Simple price-only chart
            fig = make_subplots(
                rows=1, cols=1,
                subplot_titles=[f"{selected_ticker} - {template_config['description']}"]
            )

        # Main price chart with WZRD colors
        fig.add_trace(
            go.Candlestick(
                x=df['date'],
                open=df['open'],
                high=df['high'],
                low=df['low'],
                close=df['close'],
                name=selected_ticker,
                showlegend=False,
                increasing_line_color=CHART_STYLE["candle_colors"]["increasing"],
                decreasing_line_color=CHART_STYLE["candle_colors"]["decreasing"]
            ), row=1, col=1
        )

        # Add VWAP if enabled in template
        if indicators.get("vwap", False):
            fig.add_trace(
                go.Scatter(
                    x=df['date'],
                    y=df['vwap'],
                    mode='lines',
                    name='VWAP',
                    line=dict(color=CHART_STYLE["indicator_colors"]["vwap"], width=2)
                ), row=1, col=1
            )

        # Add Previous Close Line if enabled in template
        if indicators.get("prev_close", False):
            fig.add_trace(
                go.Scatter(
                    x=df['date'],
                    y=df['prev_close'],
                    mode='lines',
                    name='Prev Close',
                    line=dict(color=CHART_STYLE["indicator_colors"]["prev_close"], width=1, dash='dash')
                ), row=1, col=1
            )

        # Add 9/20 EMA Cloud if enabled in template
        if indicators.get("920_cloud", False):
            fig.add_trace(
                go.Scatter(
                    x=df['date'],
                    y=df['ema9'],
                    mode='lines',
                    name='EMA 9',
                    line=dict(color=CHART_STYLE["indicator_colors"]["ema9"], width=1)
                ), row=1, col=1
            )

            fig.add_trace(
                go.Scatter(
                    x=df['date'],
                    y=df['ema20'],
                mode='lines',
                name='EMA 20',
                line=dict(color=CHART_STYLE["indicator_colors"]["ema20"], width=1),
                fill='tonexty',
                fillcolor='rgba(0, 255, 0, 0.1)'  # Light green cloud
            ), row=1, col=1
        )

        # Add 7/28/89 EMAs
        fig.add_trace(
            go.Scatter(
                x=df['date'],
                y=df['ema7'],
                mode='lines',
                name='EMA 7',
                line=dict(color='#00FFFF', width=1)  # Cyan
            ), row=1, col=1
        )

        fig.add_trace(
            go.Scatter(
                x=df['date'],
                y=df['ema28'],
                mode='lines',
                name='EMA 28',
                line=dict(color='#FF69B4', width=1)  # Hot pink
            ), row=1, col=1
        )

        fig.add_trace(
            go.Scatter(
                x=df['date'],
                y=df['ema89'],
                mode='lines',
                name='EMA 89',
                line=dict(color='#FFA500', width=1)  # Orange
            ), row=1, col=1
        )

        # Add 9/20 Deviation Bands
        fig.add_trace(
            go.Scatter(
                x=df['date'],
                y=df['ema920_upper'],
                mode='lines',
                name='9/20 Upper Band',
                line=dict(color='#8B0000', width=1)  # Dark red
            ), row=1, col=1
        )

        fig.add_trace(
            go.Scatter(
                x=df['date'],
                y=df['ema920_lower'],
                mode='lines',
                name='9/20 Lower Band',
                line=dict(color=CHART_STYLE["indicator_colors"]["bands_below"], width=1)
            ), row=1, col=1
        )

        # Add 72/89 Deviation Bands
        fig.add_trace(
            go.Scatter(
                x=df['date'],
                y=df['ema7289_upper'],
                mode='lines',
                name='72/89 Upper Band',
                line=dict(color='#8B0000', width=1, dash='dot')  # Dark red dotted
            ), row=1, col=1
        )

        fig.add_trace(
            go.Scatter(
                x=df['date'],
                y=df['ema7289_lower'],
                mode='lines',
                name='72/89 Lower Band',
                line=dict(color=CHART_STYLE["indicator_colors"]["bands_below"], width=1, dash='dot')
            ), row=1, col=1
        )

        # Volume chart
        fig.add_trace(
            go.Bar(
                x=df['date'],
                y=df['volume'],
                name='Volume',
                marker_color='lightblue',
                showlegend=False
            ), row=2, col=1
        )

        # RSI chart
        fig.add_trace(
            go.Scatter(
                x=df['date'],
                y=df['rsi'],
                mode='lines',
                name='RSI',
                line=dict(color='purple'),
                showlegend=False
            ), row=3, col=1
        )

        # Add RSI levels
        fig.add_hline(y=70, line_dash="dash", line_color=CHART_STYLE["indicator_colors"]["bands_above"], row=3, col=1)
        fig.add_hline(y=30, line_dash="dash", line_color=CHART_STYLE["indicator_colors"]["bands_below"], row=3, col=1)

        # Add signals - filter by entry time and validate placement
        for signal in signals:
            signal_time = pd.to_datetime(signal['timestamp'])
            signal_type = signal.get('type', 'unknown')

            # Validate signal time is within chart range
            if signal_time < df['date'].min() or signal_time > df['date'].max():
                continue

            # For entry signals, check time filter (8am-1pm EST)
            if 'entry' in signal_type.lower():
                signal_hour = signal_time.hour
                if not (8 <= signal_hour <= 13):  # Entry only between 8am-1pm
                    continue

            closest_idx = df['date'].sub(signal_time).abs().idxmin()
            signal_price = df.loc[closest_idx, 'close']
            actual_time = df.loc[closest_idx, 'date']

            if 'entry' in signal_type.lower():
                fig.add_trace(
                    go.Scatter(
                        x=[actual_time],
                        y=[signal_price],
                        mode='markers',
                        marker=dict(symbol='triangle-up', size=15, color='lime'),
                        name=f"Entry: ${signal.get('price', signal_price):.2f}",
                        showlegend=True,
                        hovertemplate=f"<b>ENTRY</b><br>Time: {actual_time.strftime('%Y-%m-%d %H:%M')}<br>Price: ${signal_price:.2f}<br>Reason: {signal.get('reason', 'N/A')}<extra></extra>"
                    ), row=1, col=1
                )
            elif 'exit' in signal_type.lower():
                fig.add_trace(
                    go.Scatter(
                        x=[actual_time],
                        y=[signal_price],
                        mode='markers',
                        marker=dict(symbol='triangle-down', size=15, color='red'),
                        name=f"Exit: ${signal.get('price', signal_price):.2f}",
                        showlegend=True,
                        hovertemplate=f"<b>EXIT</b><br>Time: {actual_time.strftime('%Y-%m-%d %H:%M')}<br>Price: ${signal_price:.2f}<br>P&L: ${signal.get('pnl', 'N/A')}<extra></extra>"
                    ), row=1, col=1
                )

        # Apply WZRD Chart Styling - Professional layout
        fig.update_layout(
            title=f"{strategy_artifact.get('strategy_name', 'Strategy')} - {selected_ticker} (Detailed View)",
            height=1100,  # Bigger height for better visibility
            showlegend=False,  # Keep clean like WZRD charts
            template=CHART_STYLE["theme"],
            paper_bgcolor=CHART_STYLE["paper_bgcolor"],
            plot_bgcolor=CHART_STYLE["plot_bgcolor"],
            margin=dict(l=60, r=20, t=50, b=50),  # Proper margins for wide charts
            hovermode='x unified',
            dragmode='pan',  # Pan by default like professional charts
            xaxis3_title="Time",
            yaxis_title="Price ($)",
            yaxis2_title="Volume",
            yaxis3_title="RSI",
            xaxis=dict(
                rangeslider=dict(visible=False),
                type='date',
                autorange=True,
                fixedrange=False,
                showspikes=True,
                spikemode='across',
                spikesnap='cursor',
                gridcolor=CHART_STYLE["grid"]["color"],
                showgrid=True
            ),
            yaxis=dict(
                autorange=True,
                fixedrange=False,
                showspikes=True,
                spikemode='across',
                spikesnap='cursor',
                gridcolor=CHART_STYLE["grid"]["color"],
                showgrid=True
            ),
            yaxis2=dict(
                autorange=True,
                fixedrange=False,
                gridcolor=CHART_STYLE["grid"]["color"],
                showgrid=True
            ),
            yaxis3=dict(
                autorange=True,
                fixedrange=False,
                gridcolor=CHART_STYLE["grid"]["color"],
                showgrid=True
            )
        )

        return fig

    except Exception as e:
        st.error(f"Error creating detailed chart: {e}")
        return None

def create_simple_chart(strategy_artifact, selected_ticker, use_mock_data, chart_days=7, chart_frequency="5min"):
    """Create a simple price chart with signals"""
    try:
        signals = strategy_artifact.get('signals', [])
        if not signals:
            return None

        # Generate dense data for simple chart to match professional density
        signal_dates = [pd.to_datetime(s['timestamp']) for s in signals]
        if signal_dates:
            # Use signal dates but extend by chart_days
            start_date = max(min(signal_dates) - timedelta(days=1),
                           max(signal_dates) - timedelta(days=chart_days))
            end_date = max(signal_dates) + timedelta(hours=2)
        else:
            # Fallback if no signals
            end_date = datetime.now()
            start_date = end_date - timedelta(days=chart_days)

        # Generate dense time series like the detailed chart
        if chart_frequency == "5min":
            freq_minutes = 5
        elif chart_frequency == "15min":
            freq_minutes = 15
        else:
            freq_minutes = 60

        # Create dense time series
        current_time = start_date.replace(hour=9, minute=30, second=0, microsecond=0)
        date_range = []

        days_added = 0
        while days_added < chart_days:
            if current_time.weekday() < 5:  # Trading days only
                day_start = current_time.replace(hour=9, minute=30)
                day_end = current_time.replace(hour=16, minute=0)

                bar_time = day_start
                while bar_time < day_end:
                    date_range.append(bar_time)
                    bar_time += timedelta(minutes=freq_minutes)

                days_added += 1
            current_time += timedelta(days=1)

        np.random.seed(42)
        base_price = 450.0 if selected_ticker == 'QQQ' else (550.0 if selected_ticker == 'SPY' else 225.0)

        prices = []
        for i in range(len(date_range)):
            if i == 0:
                prices.append(base_price)
            else:
                prices.append(prices[-1] * (1 + np.random.normal(0, 0.001)))

        df = pd.DataFrame({'date': date_range, 'price': prices})

        # Create simple line chart
        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=df['date'],
                y=df['price'],
                mode='lines',
                name=selected_ticker,
                line=dict(color=CHART_STYLE["candle_colors"]["increasing"], width=2)
            )
        )

        # Add signals - filter by entry time and validate placement
        for signal in signals:
            signal_time = pd.to_datetime(signal['timestamp'])
            signal_type = signal.get('type', 'unknown')

            # Validate signal time is within chart range
            if signal_time < df['date'].min() or signal_time > df['date'].max():
                continue

            # For entry signals, check time filter (8am-1pm EST)
            if 'entry' in signal_type.lower():
                signal_hour = signal_time.hour
                if not (8 <= signal_hour <= 13):  # Entry only between 8am-1pm
                    continue

            closest_idx = df['date'].sub(signal_time).abs().idxmin()
            signal_price = df.loc[closest_idx, 'price']
            actual_time = df.loc[closest_idx, 'date']

            if 'entry' in signal_type.lower():
                fig.add_trace(
                    go.Scatter(
                        x=[actual_time],
                        y=[signal_price],
                        mode='markers',
                        marker=dict(symbol='circle', size=15, color='lime'),
                        name=f"Buy: ${signal.get('price', signal_price):.2f}",
                        hovertemplate=f"<b>ENTRY</b><br>Time: {actual_time.strftime('%Y-%m-%d %H:%M')}<br>Price: ${signal_price:.2f}<br>Reason: {signal.get('reason', 'N/A')}<extra></extra>"
                    )
                )
            elif 'exit' in signal_type.lower():
                fig.add_trace(
                    go.Scatter(
                        x=[actual_time],
                        y=[signal_price],
                        mode='markers',
                        marker=dict(symbol='circle', size=15, color='red'),
                        name=f"Sell: ${signal.get('price', signal_price):.2f}",
                        hovertemplate=f"<b>EXIT</b><br>Time: {actual_time.strftime('%Y-%m-%d %H:%M')}<br>Price: ${signal_price:.2f}<br>P&L: ${signal.get('pnl', 'N/A')}<extra></extra>"
                    )
                )

        # Apply WZRD Chart Styling - Professional layout
        fig.update_layout(
            title=f"{strategy_artifact.get('strategy_name', 'Strategy')} - {selected_ticker} (Simple View)",
            height=800,  # Bigger height for better visibility
            showlegend=False,  # Keep clean like WZRD charts
            template=CHART_STYLE["theme"],
            paper_bgcolor=CHART_STYLE["paper_bgcolor"],
            plot_bgcolor=CHART_STYLE["plot_bgcolor"],
            margin=dict(l=60, r=20, t=50, b=50),  # Proper margins for wide charts
            hovermode='x unified',
            dragmode='pan',  # Pan by default like professional charts
            xaxis_title="Time",
            yaxis_title="Price ($)",
            xaxis=dict(
                rangeslider=dict(visible=False),
                type='date',
                autorange=True,
                fixedrange=False,
                showspikes=True,
                spikemode='across',
                spikesnap='cursor',
                gridcolor=CHART_STYLE["grid"]["color"],
                showgrid=True
            ),
            yaxis=dict(
                autorange=True,
                fixedrange=False,
                showspikes=True,
                spikemode='across',
                spikesnap='cursor',
                gridcolor=CHART_STYLE["grid"]["color"],
                showgrid=True
            )
        )

        return fig

    except Exception as e:
        st.error(f"Error creating simple chart: {e}")
        return None

# Page config
st.set_page_config(
    page_title="Enhanced Strategy Viewer",
    page_icon="📊",
    layout="wide"
)

# Header
st.title("📊 Enhanced Strategy Viewer")
st.markdown("Multiple chart layouts for strategy visualization")

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
    ["Paste JSON", "Load Existing File"],
    horizontal=True
)

# Data configuration
st.markdown("## 📊 Data Configuration")
col1, col2, col3 = st.columns(3)

with col1:
    data_source = st.radio("Data Source:", ["Real Data", "Mock Data"], horizontal=True)
    available_tickers = ['SPY', 'QQQ', 'IWM', 'DIA', 'AAPL', 'MSFT', 'TSLA', 'NVDA']
    selected_ticker = st.selectbox("Select Ticker", available_tickers, index=1)

with col2:
    # Chart time range controls
    st.markdown("**📅 Chart Time Range**")
    chart_days = st.slider("Days to Display", min_value=1, max_value=10, value=3, step=1)
    chart_frequency = st.selectbox("Data Frequency", ["5min", "15min", "1H"], index=0)

with col3:
    api_key_status = '✅ Configured' if 'POLYGON_API_KEY' in os.environ else '❌ Missing'
    # Get template configuration
    template_config = CHART_TEMPLATES.get(chart_template, CHART_TEMPLATES["5min"])

    st.info(f"""
    **Ticker:** {selected_ticker}
    **Template:** {template_config["description"]}
    **Days:** {chart_days} days
    **Freq:** {chart_frequency}
    **API Key:** {api_key_status}
    """)

use_mock_data = data_source == "Mock Data"

# Strategy input
strategy_json = ""
if input_method == "Paste JSON":
    strategy_json = st.text_area(
        "Paste your strategy JSON:",
        height=300,
        placeholder='{"strategy_name": "Your Strategy", ...}'
    )
elif input_method == "Load Existing File":
    strategy_files = [f for f in os.listdir('.') if f.endswith('.json') and ('codified' in f or 'strategy' in f)]
    if strategy_files:
        selected_file = st.selectbox("Choose file:", strategy_files)
        if st.button("Load File"):
            try:
                with open(selected_file, 'r') as f:
                    strategy_json = f.read()
                st.success(f"✅ Loaded {selected_file}")
            except Exception as e:
                st.error(f"Error: {e}")

# Process strategy
if strategy_json:
    try:
        strategy_artifact = json.loads(strategy_json)

        st.markdown("## 📊 Strategy Chart")

        # Create chart based on selected template
        with st.spinner("Creating chart..."):
            fig = create_wzrd_chart(strategy_artifact, selected_ticker, use_mock_data, chart_days, chart_frequency, template_config)

            if fig:
                # Add strategy information and zoom instructions
                st.info("📋 **Strategy Rules**: Entry signals only between 8am-1pm EST. Direction must match 1hr EMA trend.")
                st.info("🔍 **Chart Controls**: Drag to zoom, double-click to reset. Both horizontal and vertical zoom enabled.")
                st.plotly_chart(fig, use_container_width=True, config={
                    'displayModeBar': True,
                    'displaylogo': False,
                    'modeBarButtonsToRemove': ['select2d', 'lasso2d'],
                    'scrollZoom': True
                })
            else:
                st.warning("Could not create chart")

        # Show signals table
        signals = strategy_artifact.get('signals', [])
        if signals:
            st.markdown("## 📋 Signal Details")
            df_signals = pd.DataFrame(signals)
            st.dataframe(df_signals)

    except json.JSONDecodeError as e:
        st.error(f"Invalid JSON: {e}")
    except Exception as e:
        st.error(f"Error: {e}")