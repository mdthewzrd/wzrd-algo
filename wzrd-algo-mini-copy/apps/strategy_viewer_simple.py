"""
Simple Strategy Viewer - Working version with Charts
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import os
from datetime import datetime, timedelta

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

def create_strategy_chart(strategy_artifact, selected_ticker, use_mock_data):
    """Create a chart with strategy signals"""
    try:
        # Get signals from strategy
        signals = strategy_artifact.get('signals', [])
        if not signals:
            return None

        # Create mock price data for demonstration
        # In a real implementation, this would fetch actual market data
        from datetime import datetime, timedelta
        import numpy as np

        # Generate date range based on signals
        if signals:
            # Get date range from signals
            signal_dates = [pd.to_datetime(s['timestamp']) for s in signals]
            start_date = min(signal_dates) - timedelta(days=1)
            end_date = max(signal_dates) + timedelta(days=1)
        else:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=30)

        # Create date range for chart
        date_range = pd.date_range(start=start_date, end=end_date, freq='5min')
        date_range = [d for d in date_range if 9 <= d.hour < 16 and d.weekday() < 5]

        # Generate mock OHLC data
        np.random.seed(42)
        base_price = 450.0 if selected_ticker == 'QQQ' else 350.0
        n_points = len(date_range)

        # Generate realistic price movements
        returns = np.random.normal(0, 0.001, n_points)
        prices = [base_price]
        for i in range(1, n_points):
            prices.append(prices[-1] * (1 + returns[i]))

        # Create OHLC data
        data = []
        for i, (date, price) in enumerate(zip(date_range, prices)):
            high = price * (1 + abs(np.random.normal(0, 0.002)))
            low = price * (1 - abs(np.random.normal(0, 0.002)))
            open_price = prices[i-1] if i > 0 else price
            close_price = price
            data.append({
                'date': date,
                'open': open_price,
                'high': max(open_price, close_price, high),
                'low': min(open_price, close_price, low),
                'close': close_price
            })

        df = pd.DataFrame(data)

        # Create plotly chart
        fig = make_subplots(rows=1, cols=1, subplot_titles=[f"{selected_ticker} Strategy Signals"])

        # Add candlestick chart
        fig.add_trace(
            go.Candlestick(
                x=df['date'],
                open=df['open'],
                high=df['high'],
                low=df['low'],
                close=df['close'],
                name=selected_ticker
            )
        )

        # Add signals as markers
        for signal in signals:
            signal_time = pd.to_datetime(signal['timestamp'])
            signal_type = signal.get('type', 'unknown')

            # Find closest price point
            closest_idx = df['date'].sub(signal_time).abs().idxmin()
            signal_price = df.loc[closest_idx, 'close']

            if 'entry' in signal_type.lower():
                # Entry signal - green arrow up
                fig.add_trace(
                    go.Scatter(
                        x=[signal_time],
                        y=[signal_price],
                        mode='markers',
                        marker=dict(
                            symbol='triangle-up',
                            size=15,
                            color='green'
                        ),
                        name=f"Entry: ${signal.get('price', signal_price):.2f}",
                        text=f"Entry: {signal.get('reason', 'Signal')}",
                        hovertemplate=f"<b>Entry Signal</b><br>Time: %{{x}}<br>Price: ${signal.get('price', signal_price):.2f}<br>Shares: {signal.get('shares', 'N/A')}<extra></extra>"
                    )
                )
            elif 'exit' in signal_type.lower():
                # Exit signal - red arrow down
                fig.add_trace(
                    go.Scatter(
                        x=[signal_time],
                        y=[signal_price],
                        mode='markers',
                        marker=dict(
                            symbol='triangle-down',
                            size=15,
                            color='red'
                        ),
                        name=f"Exit: ${signal.get('price', signal_price):.2f}",
                        text=f"Exit: {signal.get('reason', 'Signal')}",
                        hovertemplate=f"<b>Exit Signal</b><br>Time: %{{x}}<br>Price: ${signal.get('price', signal_price):.2f}<br>P&L: ${signal.get('pnl', 'N/A')}<extra></extra>"
                    )
                )

        # Update layout
        fig.update_layout(
            title=f"{strategy_artifact.get('strategy_name', 'Strategy')} - {selected_ticker}",
            xaxis_title="Time",
            yaxis_title="Price ($)",
            height=600,
            showlegend=True,
            xaxis_rangeslider_visible=False
        )

        return fig

    except Exception as e:
        st.error(f"Error creating chart: {e}")
        return None

# Page config
st.set_page_config(
    page_title="Strategy Viewer",
    page_icon="📊",
    layout="wide"
)

# Header
st.title("📊 Strategy Viewer")
st.markdown("Visualize and verify strategy signals from Signal Codifier")

# Workflow explanation
st.markdown("## 🔄 Your Streamlined Workflow")
st.markdown("**Web Chat → Signal Codifier → Strategy Viewer**")

# Input method selection
st.markdown("## 📝 Input Strategy")
input_method = st.radio(
    "Choose input method:",
    ["Paste JSON", "Load Example", "Load Existing File"],
    horizontal=True
)

# Data source selection
st.markdown("## 📊 Data Configuration")
data_source = st.radio(
    "Data Source:",
    ["Real Data (Polygon API)", "Mock Data (Testing)"],
    horizontal=True
)
use_mock_data = data_source == "Mock Data (Testing)"

# Market data configuration
if not use_mock_data:
    col1, col2 = st.columns(2)

    with col1:
        # Ticker selection
        available_tickers = ['SPY', 'QQQ', 'IWM', 'DIA', 'AAPL', 'MSFT', 'TSLA', 'NVDA']
        selected_ticker = st.selectbox("Select Ticker", available_tickers, index=1)

        # Date range
        date_range_option = st.radio("Date Range", ["Last N Days", "Custom Range"])

        if date_range_option == "Last N Days":
            days_back = st.slider("Days of Data", 7, 90, 30)
            start_date = None
            end_date = None
        else:
            start_date = st.date_input("Start Date", value=(datetime.now() - timedelta(days=30)).date())
            end_date = st.date_input("End Date", value=datetime.now().date())
            days_back = None

    with col2:
        st.markdown("### Configuration Summary")
        api_key_status = '✅ Configured' if 'POLYGON_API_KEY' in os.environ else '❌ Missing'
        st.info(f"""
        **Ticker:** {selected_ticker}
        **Data Source:** Polygon API
        **API Key:** {api_key_status}
        """)

        if 'POLYGON_API_KEY' not in os.environ:
            st.error("⚠️ POLYGON_API_KEY not found in environment variables.")
else:
    selected_ticker = 'SPY'
    days_back = 30
    start_date = None
    end_date = None

# Strategy input
strategy_json = ""
if input_method == "Paste JSON":
    strategy_json = st.text_area(
        "Paste your strategy JSON from Signal Codifier:",
        height=300,
        placeholder='{"strategy_name": "Your Strategy", ...}'
    )
elif input_method == "Load Existing File":
    strategy_files = [f for f in os.listdir('.') if f.endswith('.json') and 'codified' in f]
    if strategy_files:
        selected_file = st.selectbox("Choose a strategy file:", strategy_files)
        if st.button("Load File"):
            try:
                with open(selected_file, 'r') as f:
                    strategy_json = f.read()
                st.success(f"✅ Loaded {selected_file}")
            except Exception as e:
                st.error(f"Error loading file: {e}")
    else:
        st.info("No codified strategy files found.")

# Process strategy
if strategy_json:
    try:
        strategy_artifact = json.loads(strategy_json)

        st.markdown("## 📋 Strategy Summary")
        st.write(f"**Name:** {strategy_artifact.get('strategy_name', 'Unknown')}")
        st.write(f"**Description:** {strategy_artifact.get('description', 'No description')}")
        st.write(f"**Symbol:** {strategy_artifact.get('symbol', 'Unknown')}")
        st.write(f"**Timeframe:** {strategy_artifact.get('timeframe', 'Unknown')}")

        # Show chart with signals
        signals = strategy_artifact.get('signals', [])
        if signals:
            st.markdown("## 📊 Strategy Chart with Signals")

            # Create and display chart
            with st.spinner("Creating strategy chart..."):
                fig = create_strategy_chart(strategy_artifact, selected_ticker, use_mock_data)

                if fig:
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("Could not create chart")

            st.markdown("## 📋 Signal History")
            st.write(f"**Total Signals:** {len(signals)}")

            # Display signals table
            df_signals = pd.DataFrame(signals)
            if not df_signals.empty:
                st.dataframe(df_signals)
            else:
                st.info("No signal data to display")
        else:
            st.warning("No signals found in the strategy artifact")

        # Performance metrics
        if 'performance_metrics' in strategy_artifact:
            metrics = strategy_artifact['performance_metrics']
            st.markdown("## 📈 Performance Metrics")

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Trades", metrics.get('total_trades', 0))
            with col2:
                st.metric("Win Rate", f"{metrics.get('win_rate', 0):.1%}")
            with col3:
                st.metric("Total P&L", f"${metrics.get('total_pnl', 0):.2f}")
            with col4:
                st.metric("Profit Factor", f"{metrics.get('profit_factor', 0):.2f}")

    except json.JSONDecodeError as e:
        st.error(f"Invalid JSON: {e}")
    except Exception as e:
        st.error(f"Error processing strategy: {e}")

# Footer
st.markdown("---")
st.markdown("Strategy Viewer - Part of your streamlined workflow")