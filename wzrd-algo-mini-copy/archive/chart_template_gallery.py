"""
Chart Template Gallery - View all WZRD chart templates on SPY data
Shows Day, Hour, 15min, and 5min templates with different indicator combinations
"""

import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import yfinance as yf
from utils.chart_templates import CHART_TEMPLATES, CHART_STYLE

# Page config
st.set_page_config(
    page_title="WZRD Chart Template Gallery",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.title("📊 WZRD Chart Template Gallery")
st.markdown("**All chart layouts on SPY data** - View your professional chart templates")

# Create tabs for each timeframe
tab1, tab2, tab3, tab4 = st.tabs(["📈 Daily", "🕐 Hourly", "⏰ 15min", "⚡ 5min"])

@st.cache_data(ttl=300)  # Cache for 5 minutes
def get_spy_data(period="1y", interval="1d"):
    """Get SPY data from yfinance"""
    try:
        spy = yf.Ticker("SPY")
        data = spy.history(period=period, interval=interval, prepost=True)
        return data
    except Exception as e:
        st.error(f"Error fetching SPY data: {e}")
        return None

def calculate_ema(data, period):
    """Calculate EMA"""
    return data['Close'].ewm(span=period).mean()

def calculate_deviation_bands(ema_data, period=72, multiplier=6):
    """Calculate deviation bands"""
    std_dev = ema_data.rolling(window=period).std()
    upper_band = ema_data + (std_dev * multiplier)
    lower_band = ema_data - (std_dev * multiplier)
    return upper_band, lower_band

def create_chart(data, template_name, config):
    """Create chart with template configuration"""
    if data is None or data.empty:
        return None

    fig = go.Figure()

    # Add candlesticks
    fig.add_trace(go.Candlestick(
        x=data.index,
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close'],
        name="SPY",
        increasing_line_color=CHART_STYLE["candle_colors"]["increasing"],
        decreasing_line_color=CHART_STYLE["candle_colors"]["decreasing"],
        showlegend=False
    ))

    # Add indicators based on template config
    indicators = config.get("indicators", {})

    # VWAP (approximation using close * volume)
    if indicators.get("vwap", False):
        try:
            cumulative_pv = (data['Close'] * data['Volume']).cumsum()
            cumulative_volume = data['Volume'].cumsum()
            vwap = cumulative_pv / cumulative_volume
            fig.add_trace(go.Scatter(
                x=data.index, y=vwap,
                mode='lines',
                name='VWAP',
                line=dict(color=CHART_STYLE["indicator_colors"]["vwap"], width=1),
                showlegend=False
            ))
        except:
            pass

    # Previous close line
    if indicators.get("prev_close", False):
        try:
            prev_close = data['Close'].iloc[-1]
            fig.add_hline(
                y=prev_close,
                line_dash="dash",
                line_color=CHART_STYLE["indicator_colors"]["prev_close"],
                annotation_text="Prev Close"
            )
        except:
            pass

    # 9/20 EMA system
    if indicators.get("920_bands", False) or indicators.get("920_cloud", False):
        try:
            ema9 = calculate_ema(data, 9)
            ema20 = calculate_ema(data, 20)

            fig.add_trace(go.Scatter(
                x=data.index, y=ema9,
                mode='lines',
                name='EMA 9',
                line=dict(color=CHART_STYLE["indicator_colors"]["ema9"], width=1),
                showlegend=False
            ))

            fig.add_trace(go.Scatter(
                x=data.index, y=ema20,
                mode='lines',
                name='EMA 20',
                line=dict(color=CHART_STYLE["indicator_colors"]["ema20"], width=1),
                showlegend=False
            ))

            # EMA Cloud
            if indicators.get("920_cloud", False):
                fig.add_trace(go.Scatter(
                    x=data.index, y=ema9,
                    fill=None,
                    mode='lines',
                    line_color='rgba(0,0,0,0)',
                    showlegend=False
                ))
                fig.add_trace(go.Scatter(
                    x=data.index, y=ema20,
                    fill='tonexty',
                    mode='lines',
                    line_color='rgba(0,0,0,0)',
                    fillcolor='rgba(0,255,0,0.1)',
                    showlegend=False
                ))
        except:
            pass

    # 72/89 EMA system
    if indicators.get("7289_bands", False) or indicators.get("7289_cloud", False):
        try:
            ema72 = calculate_ema(data, 72)
            ema89 = calculate_ema(data, 89)

            fig.add_trace(go.Scatter(
                x=data.index, y=ema72,
                mode='lines',
                name='EMA 72',
                line=dict(color=CHART_STYLE["indicator_colors"]["ema72"], width=1),
                showlegend=False
            ))

            fig.add_trace(go.Scatter(
                x=data.index, y=ema89,
                mode='lines',
                name='EMA 89',
                line=dict(color=CHART_STYLE["indicator_colors"]["ema89"], width=1),
                showlegend=False
            ))

            # Deviation bands
            if indicators.get("7289_bands", False):
                upper_72, lower_72 = calculate_deviation_bands(ema72, 72, 6)
                upper_89, lower_89 = calculate_deviation_bands(ema89, 89, 6)

                fig.add_trace(go.Scatter(
                    x=data.index, y=upper_72,
                    mode='lines',
                    name='Upper Band 72',
                    line=dict(color=CHART_STYLE["indicator_colors"]["bands_above"], width=1, dash='dot'),
                    showlegend=False
                ))
                fig.add_trace(go.Scatter(
                    x=data.index, y=lower_72,
                    mode='lines',
                    name='Lower Band 72',
                    line=dict(color=CHART_STYLE["indicator_colors"]["bands_below"], width=1, dash='dot'),
                    showlegend=False
                ))
        except:
            pass

    # Apply template styling
    fig.update_layout(
        title=f"SPY - {config['description']}",
        template=CHART_STYLE["theme"],
        paper_bgcolor=CHART_STYLE["paper_bgcolor"],
        plot_bgcolor=CHART_STYLE["plot_bgcolor"],
        height=CHART_STYLE["layout"]["height"],
        margin=CHART_STYLE["layout"]["margin"],
        showlegend=CHART_STYLE["layout"]["showlegend"],
        hovermode=CHART_STYLE["layout"]["hovermode"],
        dragmode=CHART_STYLE["layout"]["dragmode"],
        xaxis=dict(
            gridcolor=CHART_STYLE["grid"]["color"],
            showgrid=True
        ),
        yaxis=dict(
            gridcolor=CHART_STYLE["grid"]["color"],
            showgrid=True
        )
    )

    return fig

# Daily Tab
with tab1:
    st.subheader("📈 Daily Chart Template")
    daily_config = CHART_TEMPLATES["day"]
    st.write(f"**Description:** {daily_config['description']}")

    # Get daily data
    daily_data = get_spy_data(period="1y", interval="1d")
    if daily_data is not None:
        daily_chart = create_chart(daily_data, "Daily", daily_config)
        if daily_chart:
            st.plotly_chart(daily_chart, use_container_width=True, key="daily_chart")

        # Show config
        with st.expander("📋 Template Configuration"):
            col1, col2 = st.columns(2)
            with col1:
                st.write("**Chart Settings:**")
                st.write(f"• Default days: {daily_config['default_days']}")
                st.write(f"• Bars per day: {daily_config['bars_per_day']}")
                st.write(f"• Warmup days: {daily_config['warmup_days']}")
            with col2:
                st.write("**Indicators:**")
                for indicator, enabled in daily_config["indicators"].items():
                    status = "✅" if enabled else "❌"
                    st.write(f"• {indicator}: {status}")

# Hourly Tab
with tab2:
    st.subheader("🕐 Hourly Chart Template")
    hourly_config = CHART_TEMPLATES["hour"]
    st.write(f"**Description:** {hourly_config['description']}")

    # Get hourly data - 30 days to show proper density
    hourly_data = get_spy_data(period="30d", interval="1h")
    if hourly_data is not None:
        # Filter to last 10 days for better visualization
        hourly_data = hourly_data.tail(10 * 24)  # ~10 days of hourly data
        hourly_chart = create_chart(hourly_data, "Hourly", hourly_config)
        if hourly_chart:
            st.plotly_chart(hourly_chart, use_container_width=True, key="hourly_chart")

        # Show config
        with st.expander("📋 Template Configuration"):
            col1, col2 = st.columns(2)
            with col1:
                st.write("**Chart Settings:**")
                st.write(f"• Default days: {hourly_config['default_days']}")
                st.write(f"• Bars per day: {hourly_config['bars_per_day']}")
                st.write(f"• Warmup days: {hourly_config['warmup_days']}")
            with col2:
                st.write("**Indicators:**")
                for indicator, enabled in hourly_config["indicators"].items():
                    status = "✅" if enabled else "❌"
                    st.write(f"• {indicator}: {status}")

# 15min Tab
with tab3:
    st.subheader("⏰ 15-Minute Chart Template")
    min15_config = CHART_TEMPLATES["15min"]
    st.write(f"**Description:** {min15_config['description']}")

    # Get 15min data - 60 days to get proper density
    min15_data = get_spy_data(period="60d", interval="15m")
    if min15_data is not None:
        # Filter to last 5 days for better visualization
        min15_data = min15_data.tail(5 * 4 * 13)  # ~5 days of 15min data (4 per hour × 13 hours)
        min15_chart = create_chart(min15_data, "15min", min15_config)
        if min15_chart:
            st.plotly_chart(min15_chart, use_container_width=True, key="min15_chart")

        # Show config
        with st.expander("📋 Template Configuration"):
            col1, col2 = st.columns(2)
            with col1:
                st.write("**Chart Settings:**")
                st.write(f"• Default days: {min15_config['default_days']}")
                st.write(f"• Bars per day: {min15_config['bars_per_day']}")
                st.write(f"• Warmup days: {min15_config['warmup_days']}")
            with col2:
                st.write("**Indicators:**")
                for indicator, enabled in min15_config["indicators"].items():
                    status = "✅" if enabled else "❌"
                    st.write(f"• {indicator}: {status}")

# 5min Tab
with tab4:
    st.subheader("⚡ 5-Minute Chart Template")
    min5_config = CHART_TEMPLATES["5min"]
    st.write(f"**Description:** {min5_config['description']}")

    # Get 5min data - 60 days to get proper density
    min5_data = get_spy_data(period="60d", interval="5m")
    if min5_data is not None:
        # Filter to last 3 days for better visualization (full density)
        min5_data = min5_data.tail(3 * 12 * 16)  # ~3 days of 5min data (12 per hour × 16 hours)
        min5_chart = create_chart(min5_data, "5min", min5_config)
        if min5_chart:
            st.plotly_chart(min5_chart, use_container_width=True, key="min5_chart")

        # Show config
        with st.expander("📋 Template Configuration"):
            col1, col2 = st.columns(2)
            with col1:
                st.write("**Chart Settings:**")
                st.write(f"• Default days: {min5_config['default_days']}")
                st.write(f"• Bars per day: {min5_config['bars_per_day']}")
                st.write(f"• Warmup days: {min5_config['warmup_days']}")
            with col2:
                st.write("**Indicators:**")
                for indicator, enabled in min5_config["indicators"].items():
                    status = "✅" if enabled else "❌"
                    st.write(f"• {indicator}: {status}")

# Footer
st.markdown("---")
st.markdown("**WZRD Chart Template Gallery** - Professional chart layouts for trading analysis")