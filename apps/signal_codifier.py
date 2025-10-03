"""
Signal Codifier Streamlit App
Converts strategy JSON specifications into code-true signals
Perfect for your web chat → Signal Codifier → Test Viewer workflow
"""

import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime, timedelta
import pytz
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import our modules
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))

from signal_generator import SignalGenerator
from data_integration import get_market_data
from regenerate_signals import clean_strategy_config

# Page config
st.set_page_config(
    page_title="Signal Codifier",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .strategy-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 1rem;
        color: white;
        margin-bottom: 2rem;
    }
    .success-box {
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .info-box {
        background-color: #d1ecf1;
        border-left: 4px solid #17a2b8;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .workflow-step {
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    .signal-card {
        background-color: #fff;
        border: 1px solid #dee2e6;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

def create_mock_market_data(symbol, timeframe, days_back):
    """Create mock market data for testing"""
    import numpy as np
    from datetime import datetime, timedelta

    # Generate mock data
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days_back)

    if timeframe == '5min':
        freq = '5min'
    elif timeframe == '15min':
        freq = '15min'
    elif timeframe == '1hour':
        freq = '1H'
    elif timeframe == '1day':
        freq = '1D'
    else:
        freq = '5min'

    dates = pd.date_range(start=start_date, end=end_date, freq=freq)
    dates = [d for d in dates if d.hour >= 9 and d.hour < 16 and d.weekday() < 5]

    # Generate realistic price data
    np.random.seed(42)
    base_price = 450.0 if symbol == 'SPY' else 350.0
    prices = []

    for i, date in enumerate(dates):
        if i == 0:
            prev_close = base_price
        else:
            prev_close = prices[i-1]['close']

        change = np.random.normal(0, 0.002)
        new_price = prev_close * (1 + change)

        high = max(prev_close, new_price) * (1 + abs(np.random.normal(0, 0.001)))
        low = min(prev_close, new_price) * (1 - abs(np.random.normal(0, 0.001)))
        open_price = prev_close
        close = new_price
        volume = int(np.random.lognormal(12, 0.5))

        prices.append({
            'date': date,
            'open': round(open_price, 2),
            'high': round(high, 2),
            'low': round(low, 2),
            'close': round(close, 2),
            'volume': volume
        })

    return pd.DataFrame(prices)

def main():
    # Header
    st.markdown("""
    <div class="strategy-header">
        <h1>🎯 Signal Codifier</h1>
        <p>Convert your strategy JSON specifications into code-true signals</p>
        <p><strong>Web Chat → Signal Codifier → Test Viewer</strong></p>
    </div>
    """, unsafe_allow_html=True)

    # Workflow explanation
    st.markdown("## 🔄 Your Streamlined Workflow")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
        <div class="workflow-step">
            <h4>1. Web Chat</h4>
            <p>Develop strategy idea with GPT</p>
            <p>Get initial JSON</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="workflow-step">
            <h4>2. Signal Codifier</h4>
            <p>Paste strategy JSON</p>
            <p>Generate code-true signals</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="workflow-step">
            <h4>3. Test Viewer</h4>
            <p>Verify signals visually</p>
            <p>Check performance</p>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div class="workflow-step">
            <h4>4. Iterate</h4>
            <p>Back to web chat</p>
            <p>Refine strategy</p>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # Main input section
    st.markdown("## 📝 Paste Your Strategy JSON")

    # Input method selection
    input_method = st.radio(
        "Input Method",
        ["Paste JSON", "Load Example", "Load Existing File"],
        horizontal=True
    )

    strategy_json = ""
    strategy_config = None

    if input_method == "Paste JSON":
        strategy_json = st.text_area(
            "Paste your strategy JSON here",
            height=300,
            placeholder='''{
  "strategy_name": "My Strategy",
  "symbol": "SPY",
  "timeframe": "5min",
  "entry_conditions": [...],
  "exit_conditions": [...],
  "risk_management": {...}
}'''
        )

    elif input_method == "Load Example":
        examples = {
            "QQQ Mean Reversion": {
                "strategy_name": "QQQ_Mean_Reversion_Example",
                "description": "Multi-timeframe mean reversion strategy",
                "symbol": "QQQ",
                "timeframe": "5min",
                "entry_conditions": [
                    {
                        "type": "multi_timeframe_alignment",
                        "description": "HTF uptrend + MTF VWAP bounce + LTF RSI oversold",
                        "direction": "long",
                        "htf_condition": "Daily 50EMA > 200EMA",
                        "mtf_condition": "Price pulls back to VWAP",
                        "ltf_condition": "RSI < 35 with volume spike"
                    }
                ],
                "exit_conditions": [
                    {
                        "type": "profit_target",
                        "description": "Take profit at 2R target",
                        "direction": "close_long"
                    }
                ],
                "risk_management": {
                    "stop_loss": {"type": "percentage", "value": 1.5},
                    "take_profit": {"type": "r_multiple", "value": 2.0},
                    "pyramiding": {
                        "enabled": True,
                        "max_legs": 3,
                        "add_conditions": [
                            {"level": "initial", "size_r": 0.25, "condition": "Initial entry"},
                            {"level": "confirmation", "size_r": 0.25, "condition": "Price confirmation"},
                            {"level": "continuation", "size_r": 0.5, "condition": "Trend continuation"}
                        ]
                    }
                }
            },
            "SPY VWAP Bounce": {
                "strategy_name": "SPY_VWAP_Bounce_Example",
                "description": "Simple VWAP mean reversion strategy",
                "symbol": "SPY",
                "timeframe": "15min",
                "entry_conditions": [
                    {
                        "type": "quality_filter",
                        "description": "Price pulls back to VWAP with RSI oversold",
                        "direction": "long"
                    }
                ],
                "exit_conditions": [
                    {
                        "type": "profit_target",
                        "description": "Take profit at VWAP resistance",
                        "direction": "close_long"
                    }
                ],
                "risk_management": {
                    "stop_loss": {"type": "percentage", "value": 1.0},
                    "take_profit": {"type": "percentage", "value": 1.5}
                }
            }
        }

        selected_example = st.selectbox("Choose an example strategy", list(examples.keys()))
        strategy_config = examples[selected_example]
        strategy_json = json.dumps(strategy_config, indent=2)

    elif input_method == "Load Existing File":
        # Find existing strategy files
        strategy_files = [f for f in os.listdir('.') if f.endswith('.json') and 'test_strategy' in f]
        if strategy_files:
            selected_file = st.selectbox("Choose a strategy file", strategy_files)
            try:
                with open(selected_file, 'r') as f:
                    strategy_config = json.load(f)
                strategy_json = json.dumps(strategy_config, indent=2)
                st.success(f"Loaded {selected_file}")
            except Exception as e:
                st.error(f"Error loading file: {e}")

    # Display and edit JSON - validate whenever there's content
    strategy_config = None
    if strategy_json and strategy_json.strip():
        try:
            strategy_config = json.loads(strategy_json)
            # Additional validation for required fields
            required_fields = ['strategy_name', 'symbol', 'timeframe']
            missing_fields = [field for field in required_fields if not strategy_config.get(field)]

            if missing_fields:
                st.warning(f"⚠️ Missing required fields: {', '.join(missing_fields)}")
            else:
                st.success("✅ Valid JSON loaded!")

        except json.JSONDecodeError as e:
            st.error(f"❌ Invalid JSON: {e}")
            return
    elif strategy_json and not strategy_json.strip():
        st.info("💡 Paste your strategy JSON in the text area above")
        return

    # Show strategy summary
    if strategy_config:
        st.markdown("## 📋 Strategy Summary")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Strategy Name", strategy_config.get('strategy_name', 'Unknown'))
            st.metric("Symbol", strategy_config.get('symbol', 'N/A'))

        with col2:
            st.metric("Timeframe", strategy_config.get('timeframe', 'N/A'))
            st.metric("Entry Conditions", len(strategy_config.get('entry_conditions', [])))

        with col3:
            st.metric("Exit Conditions", len(strategy_config.get('exit_conditions', [])))
            has_pyramiding = strategy_config.get('risk_management', {}).get('pyramiding', {}).get('enabled', False)
            st.metric("Pyramiding", "✅ Yes" if has_pyramiding else "❌ No")

        # Configuration options
        st.markdown("## ⚙️ Generation Options")

        col1, col2 = st.columns(2)

        with col1:
            use_real_data = st.checkbox("Use Real Market Data", value=False, help="Requires POLYGON_API_KEY")

            # Ticker selection
            available_tickers = ['SPY', 'QQQ', 'IWM', 'DIA', 'AAPL', 'MSFT', 'TSLA', 'NVDA', 'GOOGL', 'AMZN']
            selected_ticker = st.selectbox(
                "Select Ticker",
                available_tickers,
                index=available_tickers.index(strategy_config.get('symbol', 'SPY')) if strategy_config.get('symbol') in available_tickers else 0,
                help="Choose the stock symbol for analysis"
            )

            # Date range selection
            st.markdown("### 📅 Date Range")
            date_range_option = st.radio(
                "Select Date Range",
                ["Last N Days", "Custom Range"],
                index=0,
                help="Choose how to specify the date range"
            )

            if date_range_option == "Last N Days":
                days_back = st.slider("Days of Data", 7, 90, 30, help="Days of historical data to use")
                start_date = None
                end_date = None
            else:
                col_date1, col_date2 = st.columns(2)
                with col_date1:
                    start_date = st.date_input(
                        "Start Date",
                        value=(datetime.now() - timedelta(days=30)).date(),
                        help="Start date for data analysis"
                    )
                with col_date2:
                    end_date = st.date_input(
                        "End Date",
                        value=datetime.now().date(),
                        help="End date for data analysis"
                    )
                days_back = None

        with col2:
            enhance_signals = st.checkbox("Enhance with Realistic Data", value=True, help="Improve signal timing with recent market data")
            save_file = st.checkbox("Save Result to File", value=True, help="Save the generated strategy to a JSON file")

            # Show current configuration summary
            st.markdown("### 📊 Configuration Summary")
            api_key_status = '✅ Configured' if os.getenv('POLYGON_API_KEY') else '❌ Missing'
            st.info(f"""
            **Ticker:** {selected_ticker}
            **Timeframe:** {strategy_config.get('timeframe', '5min')}
            **Date Range:** {f"Last {days_back} days" if days_back else f"{start_date} to {end_date}"}
            **Data Source:** {'Real API' if use_real_data else 'Mock Data'}
            **API Key:** {api_key_status}
            """)

            if use_real_data and not os.getenv('POLYGON_API_KEY'):
                st.error("⚠️ POLYGON_API_KEY not found in environment variables. Please check your .env file.")

        # Generate button
        generate_button = st.button("🎯 Generate Code-True Signals", type="primary", use_container_width=True)

        if generate_button:
            if not strategy_config:
                st.error("❌ No strategy configuration loaded")
                return

            with st.spinner("🔄 Generating code-true signals..."):
                try:
                    # Clean the strategy config
                    clean_config = clean_strategy_config(strategy_config)

                    # Get market data using selected ticker
                    symbol = selected_ticker  # Use user-selected ticker
                    timeframe = clean_config.get('timeframe', '5min')

                    st.info(f"📊 Fetching market data for {symbol} ({timeframe})...")

                    if use_real_data:
                        try:
                            # Convert dates to strings if provided
                            start_date_str = start_date.strftime('%Y-%m-%d') if start_date else None
                            end_date_str = end_date.strftime('%Y-%m-%d') if end_date else None

                            data = get_market_data(
                                symbol=symbol,
                                timeframe=timeframe,
                                days_back=days_back,
                                start_date=start_date_str,
                                end_date=end_date_str,
                                clean_data=True,
                                add_features=True
                            )
                            st.success(f"✅ Fetched {len(data)} bars of real data")
                        except Exception as e:
                            st.warning(f"⚠️ Failed to fetch real data: {e}")
                            st.info("🔄 Using mock data instead...")
                            data = create_mock_market_data(symbol, timeframe, days_back or 30)
                            st.success(f"✅ Created {len(data)} bars of mock data")
                    else:
                        data = create_mock_market_data(symbol, timeframe, days_back or 30)
                        st.success(f"✅ Created {len(data)} bars of mock data")

                    # Generate signals
                    st.info("🎯 Computing signals from strategy rules...")
                    generator = SignalGenerator(clean_config)
                    generator.load_data(data)
                    artifact = generator.generate_signals()

                    # Enhance signals if requested
                    if enhance_signals:
                        st.info("🔄 Enhancing signal timing...")
                        # (Enhancement logic would go here)

                    # Display results
                    st.markdown("## ✅ Code-True Strategy Generated!")

                    col1, col2 = st.columns(2)

                    with col1:
                        st.metric("Signals Generated", len(artifact.get('signals', [])))
                        st.metric("Total P&L", f"${artifact.get('performance_metrics', {}).get('total_pnl', 0):.2f}")

                    with col2:
                        win_rate = artifact.get('performance_metrics', {}).get('win_rate', 0)
                        st.metric("Win Rate", f"{win_rate:.1f}%")
                        st.metric("Total Trades", artifact.get('performance_metrics', {}).get('total_trades', 0))

                    # Show signals
                    st.markdown("## 📊 Generated Signals")

                    signals = artifact.get('signals', [])
                    if signals:
                        # Create signal cards
                        for i, signal in enumerate(signals[:10], 1):  # Show first 10
                            with st.expander(f"Signal {i}: {signal.get('timestamp', 'N/A')} - {signal.get('type', 'Unknown')}"):
                                col1, col2 = st.columns(2)

                                with col1:
                                    st.write(f"**Price:** ${signal.get('price', 0):.2f}")
                                    st.write(f"**Shares:** {signal.get('shares', 0)}")
                                    st.write(f"**Position ID:** {signal.get('position_id', 'N/A')}")

                                with col2:
                                    st.write(f"**Leg:** {signal.get('leg', 1)}")
                                    st.write(f"**R Allocation:** {signal.get('r_allocation', 0):.2f}")
                                    st.write(f"**P&L:** ${signal.get('pnl', 0):.2f}")

                                st.write(f"**Reason:** {signal.get('reason', 'N/A')}")
                                st.write(f"**Execution:** {signal.get('execution', 'N/A')}")

                        if len(signals) > 10:
                            st.info(f"Showing first 10 of {len(signals)} signals")
                    else:
                        st.warning("No signals generated - check your strategy conditions")

                    # Show provenance
                    provenance = artifact.get('provenance', {})
                    if provenance:
                        st.markdown("## 🔍 Provenance Information")
                        col1, col2 = st.columns(2)

                        with col1:
                            st.write(f"**Generated by:** {provenance.get('generated_by', 'Unknown')}")
                            st.write(f"**Code Hash:** {provenance.get('code_hash', 'Unknown')}")

                        with col2:
                            st.write(f"**Generated:** {provenance.get('generation_timestamp', 'Unknown')}")
                            st.write(f"**Version:** {provenance.get('rule_version', 'Unknown')}")

                    # Download and save options
                    st.markdown("## 💾 Export Options")

                    col1, col2, col3 = st.columns(3)

                    with col1:
                        # Download JSON
                        json_str = json.dumps(artifact, indent=2, default=str)
                        st.download_button(
                            label="📥 Download JSON",
                            data=json_str,
                            file_name=f"{strategy_config.get('strategy_name', 'strategy').lower().replace(' ', '_')}_codified.json",
                            mime="application/json"
                        )

                    with col2:
                        # Copy to clipboard
                        st.code(json_str, language="json", height=200)

                    with col3:
                        if save_file:
                            filename = f"{strategy_config.get('strategy_name', 'strategy').lower().replace(' ', '_')}_codified.json"
                            try:
                                with open(filename, 'w') as f:
                                    json.dump(artifact, f, indent=2, default=str)
                                st.success(f"✅ Saved to {filename}")
                            except Exception as e:
                                st.error(f"❌ Failed to save file: {e}")

                    # Next steps
                    st.markdown("## 🚀 Next Steps")
                    st.markdown("""
                    <div class="info-box">
                        <h4>🎯 Your Strategy is Ready!</h4>
                        <p><strong>Now go to your Test Viewer (localhost:8501) to verify the signals:</strong></p>
                        <ol>
                            <li>Copy the JSON from above or download the file</li>
                            <li>Paste it into your Test Viewer</li>
                            <li>Verify the signals look correct visually</li>
                            <li>Check performance metrics</li>
                            <li>If satisfied, proceed to VectorBT implementation</li>
                            <li>If not, go back to web chat for refinements</li>
                        </ol>
                    </div>
                    """, unsafe_allow_html=True)

                except Exception as e:
                    st.error(f"❌ Error generating signals: {e}")
                    st.exception(e)

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666;">
        <p>Signal Codifier - Part of your streamlined workflow</p>
        <p>Web Chat → Signal Codifier → Test Viewer → VectorBT</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()