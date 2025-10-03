import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
import numpy as np
from datetime import datetime, timedelta
import time
import pytz
import pandas_market_calendars as mcal

# Set page config for dark theme
st.set_page_config(
    page_title="WZRD Mini Chart Viewer",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark theme
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

# Polygon API configuration
POLYGON_API_KEY = "Fm7brz4s23eSocDErnL68cE7wspz2K1I"  # Embedded API key

def get_polygon_data(symbol, timeframe="day", days_back=60):
    """Fetch data from Polygon API"""
    # Use Eastern timezone
    eastern = pytz.timezone('US/Eastern')
    now_eastern = datetime.now(eastern)
    end_date = now_eastern.strftime('%Y-%m-%d')
    start_date = (now_eastern - timedelta(days=days_back)).strftime('%Y-%m-%d')

    # Map timeframe to Polygon API format (multiplier/timespan)
    timeframe_map = {
        "day": "1/day",
        "hour": "1/hour",
        "15min": "15/minute",
        "5min": "5/minute"
    }
    api_timeframe = timeframe_map.get(timeframe, "1/day")

    # Stock data (SPY and IBIT are regular stocks)
    # Paid plans support limit up to 50,000 bars
    url = f"https://api.polygon.io/v2/aggs/ticker/{symbol}/range/{api_timeframe}/{start_date}/{end_date}?adjusted=true&sort=asc&limit=50000&apikey={POLYGON_API_KEY}"

    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            data = response.json()
            if data.get('results') and len(data['results']) > 0:
                df = pd.DataFrame(data['results'])
                if timeframe in ["hour", "15min", "5min"]:
                    # Convert to Eastern timezone for hourly and 15min
                    df['date'] = pd.to_datetime(df['t'], unit='ms').dt.tz_localize('UTC').dt.tz_convert('US/Eastern')
                else:
                    # Keep as naive datetime for daily charts (avoid timezone issues)
                    df['date'] = pd.to_datetime(df['t'], unit='ms')
                df.rename(columns={
                    'o': 'open',
                    'h': 'high',
                    'l': 'low',
                    'c': 'close',
                    'v': 'volume'
                }, inplace=True)
                return df[['date', 'open', 'high', 'low', 'close', 'volume']]
            else:
                st.warning(f"No data found for {symbol} - {timeframe}")
                return None
        else:
            st.error(f"API Error: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.Timeout:
        st.error("Request timeout. Please try again.")
        return None
    except Exception as e:
        st.error(f"Error fetching data: {str(e)}")
        return None

def filter_trading_days(df):
    """Filter out weekends and holidays using NYSE calendar"""
    if len(df) == 0:
        return df

    # Get NYSE calendar
    nyse = mcal.get_calendar('NYSE')

    # Extract date range from dataframe
    df_copy = df.copy()

    # Ensure date column is timezone-aware or convert to naive
    if df_copy['date'].dt.tz is not None:
        # Convert to US/Eastern and then make naive
        dates_naive = df_copy['date'].dt.tz_convert('US/Eastern').dt.tz_localize(None)
    else:
        dates_naive = df_copy['date']

    start_date = dates_naive.min()
    end_date = dates_naive.max()

    # Get valid trading days for the date range
    schedule = nyse.schedule(start_date=start_date, end_date=end_date)
    valid_trading_days = schedule.index.date

    # Filter dataframe to only include valid trading days
    df_copy['date_only'] = dates_naive.dt.date
    df_filtered = df_copy[df_copy['date_only'].isin(valid_trading_days)].copy()
    df_filtered = df_filtered.drop('date_only', axis=1)

    return df_filtered

def create_continuous_daily_chart(df):
    """Create a continuous daily chart without weekend gaps"""
    # Filter trading days first
    df_filtered = filter_trading_days(df).copy()

    # Create a continuous index for x-axis
    df_filtered['continuous_date'] = range(len(df_filtered))

    return df_filtered

def calculate_vwap(df):
    """Calculate session-anchored VWAP (resets each trading day)"""
    df = df.copy()
    df['datetime'] = pd.to_datetime(df['date'])
    df['date_only'] = df['datetime'].dt.date

    typical_price = (df['high'] + df['low'] + df['close']) / 3
    df['vp'] = typical_price * df['volume']

    # Group by date and calculate cumulative sums within each session
    vwap_values = []
    for date, group in df.groupby('date_only'):
        cum_vp = group['vp'].cumsum()
        cum_vol = group['volume'].cumsum()
        session_vwap = cum_vp / cum_vol
        vwap_values.extend(session_vwap.values)

    return pd.Series(vwap_values, index=df.index)

def calculate_ema(df, period):
    """Calculate EMA"""
    return df['close'].ewm(span=period, adjust=False).mean()

def calculate_atr(df, period):
    """Calculate ATR using True Range"""
    high_low = df['high'] - df['low']
    high_close = np.abs(df['high'] - df['close'].shift())
    low_close = np.abs(df['low'] - df['close'].shift())

    true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    atr = true_range.rolling(window=period).mean()
    return atr

def calculate_deviation_bands(df):
    """Calculate 9/20 EMA cloud"""
    ema9 = calculate_ema(df, 9)
    ema20 = calculate_ema(df, 20)

    # Determine which is above for coloring
    ema9_above_ema20 = ema9 > ema20

    return ema9, ema20, ema9_above_ema20

def calculate_atr_deviation_bands(df):
    """Calculate 72/89 ATR deviation bands with 6.9 range"""
    ema72 = calculate_ema(df, 72)
    ema89 = calculate_ema(df, 89)

    atr72 = calculate_atr(df, 72)
    atr89 = calculate_atr(df, 89)

    # Deviation bands - 6.4 to 7.4 for wider cloud
    deviation_above1 = ema72 + (7.4 * atr72)  # Outer
    deviation_above2 = ema72 + (6.4 * atr72)  # Inner
    deviation_below1 = ema89 - (6.4 * atr89)  # Inner
    deviation_below2 = ema89 - (7.4 * atr89)  # Outer

    return {
        'deviation_above1': deviation_above1,
        'deviation_above2': deviation_above2,
        'deviation_below1': deviation_below1,
        'deviation_below2': deviation_below2
    }

def calculate_920_deviation_bands(df):
    """Calculate 9/20 EMA deviation bands
    Upper: 0.5 to 1.0 multiplier
    Lower: 2.0 to 2.5 multiplier
    """
    ema9 = calculate_ema(df, 9)
    ema20 = calculate_ema(df, 20)

    atr9 = calculate_atr(df, 9)
    atr20 = calculate_atr(df, 20)

    # Upper bands (lighter red)
    deviation_920_above1 = ema9 + (1.0 * atr9)
    deviation_920_above2 = ema9 + (0.5 * atr9)

    # Lower bands (lighter green)
    deviation_920_below1 = ema20 - (2.0 * atr20)
    deviation_920_below2 = ema20 - (2.5 * atr20)

    return {
        'deviation_920_above1': deviation_920_above1,
        'deviation_920_above2': deviation_920_above2,
        'deviation_920_below1': deviation_920_below1,
        'deviation_920_below2': deviation_920_below2
    }

def create_chart(df, symbol, timeframe="day", display_bars=None, show_vwap=True, show_prev_close=True, show_920_bands=True, show_920_cloud=True, show_7289_bands=True, show_7289_cloud=True, zoom_to_candles=False):
    """Create chart with WZRD styling

    Args:
        df: Full dataset including warm-up period
        symbol: Trading symbol
        timeframe: 'day' or 'hour'
        display_bars: Number of bars to display (None = display all)
        show_vwap: Show VWAP indicator
        show_prev_close: Show previous day close line
        show_920_bands: Show 9/20 deviation bands
        show_920_cloud: Show 9/20 EMA cloud
        show_7289_bands: Show 72/89 deviation bands
        zoom_to_candles: Scale y-axis to candle high/low only
    """
    try:
        # Validate input data
        if df is None or len(df) == 0:
            raise ValueError("No data provided for chart")

        required_columns = ['date', 'open', 'high', 'low', 'close', 'volume']
        for col in required_columns:
            if col not in df.columns:
                raise ValueError(f"Missing required column: {col}")

        # Calculate indicators on FULL dataset (including warm-up period)
        # This ensures indicators have proper values from the first displayed candle
        df_full = df.copy()

        # Handle trading days differently for daily vs hourly
        if timeframe == "day":
            df_full = create_continuous_daily_chart(df_full)
            use_continuous_x = True
        else:
            df_full = filter_trading_days(df_full)
            use_continuous_x = False

        # Calculate indicators on FULL dataset BEFORE slicing
        # This ensures proper warm-up period for EMA/ATR calculations
        vwap_full = calculate_vwap(df_full)

        # Calculate 9/20 bands for both timeframes
        bands_920_full = calculate_920_deviation_bands(df_full)

        # Calculate 9/20 EMA cloud (for both timeframes)
        ema9_full, ema20_full, ema9_above_ema20_full = calculate_deviation_bands(df_full)

        # Calculate 72/89 bands and EMAs for hourly and 15min
        if timeframe in ["hour", "15min", "5min"]:
            bands_full = calculate_atr_deviation_bands(df_full)
            # Calculate 72/89 EMAs on FULL dataset for proper warm-up
            ema72_full = df_full['close'].ewm(span=72, adjust=False).mean()
            ema89_full = df_full['close'].ewm(span=89, adjust=False).mean()

        # Determine display window (last N bars if display_bars specified)
        if display_bars is not None and len(df_full) > display_bars:
            display_start_idx = len(df_full) - display_bars
            df_display = df_full.iloc[display_start_idx:].copy()
            # Slice indicators to match display window
            vwap = vwap_full.iloc[display_start_idx:]
            bands_920 = {k: v.iloc[display_start_idx:] for k, v in bands_920_full.items()}
            ema9 = ema9_full.iloc[display_start_idx:]
            ema20 = ema20_full.iloc[display_start_idx:]
            ema9_above_ema20 = ema9_above_ema20_full.iloc[display_start_idx:]
            if timeframe in ["hour", "15min", "5min"]:
                bands = {k: v.iloc[display_start_idx:] for k, v in bands_full.items()}
                ema72 = ema72_full.iloc[display_start_idx:]
                ema89 = ema89_full.iloc[display_start_idx:]
        else:
            df_display = df_full.copy()
            display_start_idx = 0
            vwap = vwap_full
            bands_920 = bands_920_full
            ema9 = ema9_full
            ema20 = ema20_full
            ema9_above_ema20 = ema9_above_ema20_full
            if timeframe in ["hour", "15min", "5min"]:
                bands = bands_full
                ema72 = ema72_full
                ema89 = ema89_full

        # Use df_display for chart rendering
        df = df_display

        # Create subplots - 2 rows: main chart, volume (no titles to avoid extra chart elements)
        fig = make_subplots(
            rows=2, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.02,  # Reduced spacing
            row_heights=[0.75, 0.25]
        )

        # Candlestick chart - White/Red candles only
        x_data = df['continuous_date'] if use_continuous_x else df['date']
        fig.add_trace(
            go.Candlestick(
                x=x_data,
                open=df['open'],
                high=df['high'],
                low=df['low'],
                close=df['close'],
                increasing_line_color='#FFFFFF',  # White bullish candles
                decreasing_line_color='#FF0000',  # Red bearish candles
                name=symbol,
                showlegend=False,
                # Fix candlestick width
                increasing_fillcolor='#FFFFFF',
                decreasing_fillcolor='#FF0000'
            ),
            row=1, col=1
        )

        # Previous day close line (only for hourly and 15min charts)
        if show_prev_close and timeframe in ["hour", "15min", "5min"] and len(df) > 1:
            # For hourly/15min: add a line for each day showing previous day's 4:00 PM close
            df_with_hour = df.copy()
            df_with_hour['datetime'] = pd.to_datetime(df_with_hour['date'])
            df_with_hour['hour'] = df_with_hour['datetime'].dt.hour
            df_with_hour['date_only'] = df_with_hour['datetime'].dt.date
            df_with_hour['x_value'] = x_data  # Add x-axis values

            # Group by date to find first and last x-values for each day
            daily_groups = df_with_hour.groupby('date_only')

            # Get unique dates in order
            unique_dates = sorted(df_with_hour['date_only'].unique())

            # For each date (except the first), draw the previous day's close
            for i in range(1, len(unique_dates)):
                current_date = unique_dates[i]
                prev_date = unique_dates[i-1]

                # Get previous day's close (use 4 PM close if available, else last bar of day)
                prev_day_data = df_with_hour[df_with_hour['date_only'] == prev_date]
                close_4pm = prev_day_data[prev_day_data['hour'] == 16]

                if len(close_4pm) > 0:
                    prev_close = close_4pm['close'].iloc[0]
                else:
                    # Use last bar of previous day
                    prev_close = prev_day_data['close'].iloc[-1]

                # Get current day's x-range
                current_day_data = df_with_hour[df_with_hour['date_only'] == current_date]

                if len(current_day_data) > 0:
                    x_start = current_day_data['x_value'].iloc[0]
                    x_end = current_day_data['x_value'].iloc[-1]

                    # Add horizontal line for this day showing previous close
                    fig.add_trace(
                        go.Scatter(
                            x=[x_start, x_end],
                            y=[prev_close, prev_close],
                            mode='lines',
                            line=dict(color='#808080', width=1, dash='dash'),
                            opacity=0.7,
                            showlegend=False,
                            hoverinfo='skip'
                        ),
                        row=1, col=1
                    )

        # VWAP for both daily and hourly charts (already calculated on full dataset)
        # VWAP only on hourly and 15min charts
        if show_vwap and timeframe in ["hour", "15min", "5min"]:
            fig.add_trace(
                go.Scatter(
                    x=x_data,
                    y=vwap,
                    line=dict(color='#00FF00', width=1),  # Green VWAP
                    name="VWAP",
                    opacity=0.8,
                    showlegend=False  # Hide legend
                ),
                row=1, col=1
            )

        # Add deviation bands (calculated on full dataset with warm-up)
        # 9/20 bands for both timeframes, 72/89 only for hourly
        if show_920_bands:
            # Add 9/20 deviation bands FIRST (darker, behind 72/89 bands)
            # Upper red 9/20 cloud (darker red)
            fig.add_trace(
                go.Scatter(
                    x=x_data,
                    y=bands_920['deviation_920_above1'],
                    mode='lines',
                    line=dict(width=0),
                    showlegend=False,
                    hoverinfo='skip',
                    connectgaps=True,
                    name='920_upper1'
                ),
                row=1, col=1
            )

            fig.add_trace(
                go.Scatter(
                    x=x_data,
                    y=bands_920['deviation_920_above2'],
                    mode='lines',
                    line=dict(width=0),
                    fill='tonexty',
                    fillcolor='rgba(200, 0, 0, 0.15)',  # Less vibrant red for 9/20 bands
                    showlegend=False,
                    hoverinfo='skip',
                    connectgaps=True,
                    name='920_upper2'
                ),
                row=1, col=1
            )

            # Lower green 9/20 cloud (darker green)
            fig.add_trace(
                go.Scatter(
                    x=x_data,
                    y=bands_920['deviation_920_below1'],
                    mode='lines',
                    line=dict(width=0),
                    showlegend=False,
                    hoverinfo='skip',
                    connectgaps=True,
                    name='920_lower1'
                ),
                row=1, col=1
            )

            fig.add_trace(
                go.Scatter(
                    x=x_data,
                    y=bands_920['deviation_920_below2'],
                    mode='lines',
                    line=dict(width=0),
                    fill='tonexty',
                    fillcolor='rgba(0, 200, 0, 0.15)',  # Less vibrant green for 9/20 bands
                    showlegend=False,
                    hoverinfo='skip',
                    connectgaps=True,
                    name='920_lower2'
                ),
                row=1, col=1
            )

        # Add 9/20 EMA cloud (both timeframes) - more vibrant than deviation bands
        # Cloud is green when EMA9 > EMA20 (bullish), red when EMA9 < EMA20 (bearish)
        if show_920_cloud:
            # Create masks for bullish and bearish periods
            bullish = ema9 > ema20

            # Find segments where condition changes
            # We need to create separate polygon traces for each continuous segment

            # Create a DataFrame to track segments
            df_cloud = pd.DataFrame({
                'x': x_data,
                'ema9': ema9.values,
                'ema20': ema20.values,
                'bullish': bullish.values
            })

            # Find where bullish state changes
            df_cloud['state_change'] = df_cloud['bullish'].ne(df_cloud['bullish'].shift())
            df_cloud['segment'] = df_cloud['state_change'].cumsum()

            # For each segment, create a filled polygon
            for segment_id in df_cloud['segment'].unique():
                segment_df = df_cloud[df_cloud['segment'] == segment_id]

                if len(segment_df) < 2:
                    continue

                is_bullish = segment_df['bullish'].iloc[0]

                # Create closed polygon: go along ema9, then back along ema20
                x_coords = list(segment_df['x']) + list(segment_df['x'][::-1])
                y_coords = list(segment_df['ema9']) + list(segment_df['ema20'][::-1])

                fillcolor = 'rgba(100, 255, 100, 0.3)' if is_bullish else 'rgba(255, 100, 100, 0.3)'

                fig.add_trace(
                    go.Scatter(
                        x=x_coords,
                        y=y_coords,
                        fill='toself',
                        fillcolor=fillcolor,
                        mode='lines',
                        line=dict(width=0, color='rgba(0,0,0,0)'),  # Fully transparent line
                        showlegend=False,
                        hoverinfo='skip',
                        name=f'cloud_{"green" if is_bullish else "red"}_{segment_id}'
                    ),
                    row=1, col=1
                )

        # Add 72/89 bands for hourly and 15min charts
        if show_7289_bands and timeframe in ["hour", "15min", "5min"]:
            # Now add 72/89 bands (lighter, on top with lower opacity)
            # Upper red 72/89 cloud (very light red, semi-transparent)
            fig.add_trace(
                go.Scatter(
                    x=x_data,
                    y=bands['deviation_above1'],
                    mode='lines',
                    line=dict(width=0),
                    showlegend=False,
                    hoverinfo='skip',
                    connectgaps=True,
                    name='upper1'
                ),
                row=1, col=1
            )

            fig.add_trace(
                go.Scatter(
                    x=x_data,
                    y=bands['deviation_above2'],
                    mode='lines',
                    line=dict(width=0),
                    fill='tonexty',
                    fillcolor='rgba(255, 50, 50, 0.12)',  # Very light red for 72/89
                    showlegend=False,
                    hoverinfo='skip',
                    connectgaps=True,
                    name='upper2'
                ),
                row=1, col=1
            )

            # Lower green 72/89 cloud (very light green, semi-transparent)
            fig.add_trace(
                go.Scatter(
                    x=x_data,
                    y=bands['deviation_below1'],
                    mode='lines',
                    line=dict(width=0),
                    showlegend=False,
                    hoverinfo='skip',
                    connectgaps=True,
                    name='lower1'
                ),
                row=1, col=1
            )

            fig.add_trace(
                go.Scatter(
                    x=x_data,
                    y=bands['deviation_below2'],
                    mode='lines',
                    line=dict(width=0),
                    fill='tonexty',
                    fillcolor='rgba(50, 255, 50, 0.12)',  # Very light green for 72/89
                    showlegend=False,
                    hoverinfo='skip',
                    connectgaps=True,
                    name='lower2'
                ),
                row=1, col=1
            )

        # Add 72/89 EMA cloud for hourly and 15min charts - more vibrant than deviation bands
        # Cloud is green when EMA72 > EMA89 (bullish), red when EMA72 < EMA89 (bearish)
        # EMAs are pre-calculated on full dataset with warmup, then sliced
        if show_7289_cloud and timeframe in ["hour", "15min", "5min"]:
            # Create masks for bullish and bearish periods
            bullish = ema72 > ema89

            # Create a DataFrame to track segments
            df_cloud = pd.DataFrame({
                'x': x_data,
                'ema72': ema72.values,
                'ema89': ema89.values,
                'bullish': bullish.values
            })

            # Find where bullish state changes
            df_cloud['state_change'] = df_cloud['bullish'].ne(df_cloud['bullish'].shift())
            df_cloud['segment'] = df_cloud['state_change'].cumsum()

            # For each segment, create a filled polygon
            for segment_id in df_cloud['segment'].unique():
                segment_df = df_cloud[df_cloud['segment'] == segment_id]

                if len(segment_df) < 2:
                    continue

                is_bullish = segment_df['bullish'].iloc[0]

                # Create closed polygon: go along ema72, then back along ema89
                x_coords = list(segment_df['x']) + list(segment_df['x'][::-1])
                y_coords = list(segment_df['ema72']) + list(segment_df['ema89'][::-1])

                fillcolor = 'rgba(100, 255, 100, 0.25)' if is_bullish else 'rgba(255, 100, 100, 0.25)'

                fig.add_trace(
                    go.Scatter(
                        x=x_coords,
                        y=y_coords,
                        fill='toself',
                        fillcolor=fillcolor,
                        mode='lines',
                        line=dict(width=0, color='rgba(0,0,0,0)'),  # Fully transparent line
                        showlegend=False,
                        hoverinfo='skip',
                        name=f'7289_cloud_{"green" if is_bullish else "red"}_{segment_id}'
                    ),
                    row=1, col=1
                )

        # Add after-hours shading for hourly and 15min charts (4pm to 9:30am next day)
        if timeframe in ["hour", "15min", "5min"] and len(df) > 0:
            try:
                # Get the full date range from first to last date in the data
                df['date_dt'] = pd.to_datetime(df['date'])
                min_date = df['date_dt'].min().date()
                max_date = df['date_dt'].max().date()

                # Create a complete date range including all days in the data
                complete_date_range = pd.date_range(start=min_date, end=max_date, freq='D')

                for date in complete_date_range:
                    date_str = str(date.date())
                    next_date_str = str((date + pd.Timedelta(days=1)).date())

                    # Pre-market shading: midnight to 9:30am - MAIN CHART
                    fig.add_vrect(
                        x0=f"{date_str} 00:00:00", x1=f"{date_str} 09:30:00",
                        fillcolor="rgba(120, 120, 120, 0.3)",  # Lighter grey
                        opacity=0.3,
                        layer="below", line_width=0,
                        row=1, col=1
                    )

                    # Pre-market shading: midnight to 9:30am - VOLUME CHART (congruent)
                    fig.add_vrect(
                        x0=f"{date_str} 00:00:00", x1=f"{date_str} 09:30:00",
                        fillcolor="rgba(120, 120, 120, 0.3)",  # Lighter grey
                        opacity=0.3,
                        layer="below", line_width=0,
                        row=2, col=1
                    )

                    # After-hours shading: 4pm to midnight - MAIN CHART
                    fig.add_vrect(
                        x0=f"{date_str} 16:00:00", x1=f"{date_str} 23:59:59",
                        fillcolor="rgba(120, 120, 120, 0.3)",  # Lighter grey
                        opacity=0.3,
                        layer="below", line_width=0,
                        row=1, col=1
                    )

                    # After-hours shading: 4pm to midnight - VOLUME CHART (congruent)
                    fig.add_vrect(
                        x0=f"{date_str} 16:00:00", x1=f"{date_str} 23:59:59",
                        fillcolor="rgba(120, 120, 120, 0.3)",  # Lighter grey
                        opacity=0.3,
                        layer="below", line_width=0,
                        row=2, col=1
                    )

                # Clean up the temporary column
                df.drop('date_dt', axis=1, inplace=True)

            except Exception as e:
                # If shading fails, continue without it
                pass

        # Volume bars at the bottom
        df['vol_color'] = np.where(df['close'] >= df['open'], '#FFFFFF', '#FF0000')  # White/Red volume
        fig.add_trace(
            go.Bar(
                x=x_data,
                y=df['volume'],
                marker_color=df['vol_color'],
                name="Volume",
                opacity=0.6,
                showlegend=False
            ),
            row=2, col=1
        )

        # Update layout for dark theme
        fig.update_layout(
            title={
                'text': f"{symbol} - WZRD Chart Viewer ({timeframe.title()})",
                'x': 0.5,
                'xanchor': 'center',
                'font': {'color': '#FFFFFF', 'size': 20}
            },
            template="plotly_dark",
            paper_bgcolor="#000000",
            plot_bgcolor="#000000",
            xaxis_rangeslider_visible=False,  # Disable rangeslider to remove unwanted mini chart
            height=800,
            showlegend=False,  # Hide legend completely
            hovermode='x',  # Enable hover for data inspection
            hoverlabel=dict(bgcolor="#1a1a1a", font=dict(color="#FFFFFF", size=12)),
            # Add dragmode for easy navigation
            dragmode='pan',
            # Minimize horizontal margins to maximize chart space
            margin=dict(l=0, r=0, t=50, b=10)
        )

        # Add rangebreaks for hourly charts only (daily charts use continuous x-axis)
        if timeframe != "day":
            # Calculate tight range from actual data
            x_min = x_data.min()
            x_max = x_data.max()

            # Hourly chart - hide weekends and non-trading hours
            fig.update_layout(
                xaxis=dict(
                    rangebreaks=[
                        dict(bounds=["sat", "mon"]),  # Hide weekends
                        dict(bounds=[20, 4], pattern="hour")  # Hide non-trading hours (8pm-4am Eastern)
                    ],
                    fixedrange=False,  # Allow zoom/pan
                    constrain="domain",  # Constrain to plot area
                    range=[x_min, x_max]  # Set exact data range
                ),
                xaxis2=dict(
                    rangebreaks=[
                        dict(bounds=["sat", "mon"]),  # Hide weekends for volume chart
                        dict(bounds=[20, 4], pattern="hour")  # Hide non-trading hours for volume
                    ],
                    fixedrange=False,
                    constrain="domain",
                    range=[x_min, x_max]  # Set exact data range
                )
            )

        # Update axes
        if timeframe == "day":
            # Daily chart settings - use linear for continuous x-axis
            fig.update_xaxes(
                gridcolor="#333333",
                showgrid=True,
                zeroline=False,
                tickfont=dict(color="#FFFFFF"),
                row=1, col=1,
                type='linear',  # Use linear type for continuous index
                tickmode='auto',
                nticks=20,  # Limit number of ticks for cleaner display
                showspikes=False  # Disable crosshair spikes
            )
        else:
            # Hourly chart settings (keep rangebreaks)
            fig.update_xaxes(
                gridcolor="#333333",
                showgrid=True,
                zeroline=False,
                tickfont=dict(color="#FFFFFF"),
                row=1, col=1,
                showspikes=False,  # Disable crosshair spikes
                automargin=False,  # Disable auto margins
                autorange=True,  # Auto-range based on data
                rangemode='normal'  # No padding around data
            )

        # Simplified volume chart configuration
        fig.update_xaxes(
            gridcolor="#333333",
            showgrid=True,
            zeroline=False,
            tickfont=dict(color="#FFFFFF"),
            row=2, col=1,
            showspikes=False  # Disable crosshair spikes
        )

        # Y-axis configuration for main chart
        y_axis_config = dict(
            gridcolor="#333333",
            showgrid=True,
            zeroline=False,
            tickfont=dict(color="#FFFFFF"),
            showspikes=False  # Disable crosshair spikes
        )

        # If zoom_to_candles is enabled, set y-axis range to candle high/low
        if zoom_to_candles:
            candle_high = df['high'].max()
            candle_low = df['low'].min()
            padding = (candle_high - candle_low) * 0.05  # 5% padding
            y_axis_config['range'] = [candle_low - padding, candle_high + padding]

        fig.update_yaxes(**y_axis_config, row=1, col=1)

        fig.update_yaxes(
            gridcolor="#333333",
            showgrid=True,
            zeroline=False,
            tickfont=dict(color="#FFFFFF"),
            row=2, col=1,
            showspikes=False  # Disable crosshair spikes
        )

        return fig

    except Exception as e:
        # Create a simple error chart
        fig = go.Figure()
        fig.add_annotation(
            text=f"Chart Error: {str(e)}",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(color="red", size=14)
        )
        fig.update_layout(
            title=f"{symbol} - Error",
            template="plotly_dark",
            paper_bgcolor="#000000",
            plot_bgcolor="#000000",
            height=400
        )
        return fig

def main():
    st.title("📈 WZRD Mini Chart Viewer")
    st.markdown("---")

    # Sidebar for configuration
    with st.sidebar:
        st.header("Configuration")

        # Timeframe selection (will be controlled by chart dropdown, but we need initial state)
        if 'timeframe' not in st.session_state:
            st.session_state.timeframe = "day"

        # Adjust days back based on timeframe
        if st.session_state.timeframe == "hour":
            days_back = st.slider(
                "Days of data to display",
                min_value=5,
                max_value=30,
                value=7,
                help="Number of days of hourly data to display (paid Polygon plan fetches additional warm-up data automatically)"
            )
        elif st.session_state.timeframe == "15min":
            days_back = st.slider(
                "Days of data to display",
                min_value=3,
                max_value=30,
                value=5,
                help="Number of days of 15-minute data to display (paid Polygon plan fetches additional warm-up data automatically)"
            )
        elif st.session_state.timeframe == "5min":
            days_back = st.slider(
                "Days of data to display",
                min_value=1,
                max_value=10,
                value=1,
                help="Number of days of 5-minute data to display (paid Polygon plan fetches additional warm-up data automatically)"
            )
        else:
            days_back = st.slider(
                "Days of data",
                min_value=30,
                max_value=365,
                value=60,
                help="Number of trading days to display"
            )

        refresh_button = st.button("🔄 Refresh Data", type="primary")

    # Main content area - API key is already embedded

    # Timeframe selector and indicator toggles
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        timeframe_options = ["day", "hour", "15min", "5min"]
        current_index = 0
        if st.session_state.timeframe == "hour":
            current_index = 1
        elif st.session_state.timeframe == "15min":
            current_index = 2
        elif st.session_state.timeframe == "5min":
            current_index = 3

        timeframe = st.selectbox(
            "Timeframe",
            timeframe_options,
            index=current_index,
            key="chart_timeframe",
            label_visibility="visible"
        )

    with col3:
        st.markdown("**Indicators**")
        show_vwap = st.checkbox("VWAP", value=True, key="show_vwap")
        show_prev_close = st.checkbox("Prev Close", value=True, key="show_prev_close")
        show_920_bands = st.checkbox("9/20 Bands", value=True, key="show_920")
        show_920_cloud = st.checkbox("9/20 Cloud", value=True, key="show_920_cloud")
        # 72/89 indicators available for hour and 15min
        if st.session_state.timeframe in ["hour", "15min", "5min"]:
            show_7289_bands = st.checkbox("72/89 Bands", value=True, key="show_7289")
            show_7289_cloud = st.checkbox("72/89 Cloud", value=True, key="show_7289_cloud")
        else:
            show_7289_bands = False  # Not available for daily
            show_7289_cloud = False
        zoom_to_candles = st.checkbox("Zoom to Candles", value=False, key="zoom_candles")

    # Update session state when timeframe changes
    if timeframe != st.session_state.timeframe:
        st.session_state.timeframe = timeframe
        st.rerun()

    # Display SPY chart (default symbol)
    symbol = "SPY"

    try:
        # Add warm-up period for indicator calculations
        # EMA(89) and ATR(89) need significant warm-up for accurate values
        # For hourly charts: Need at least 300 bars before the display window
        # Adding 30 calendar days (~22 trading days × 13.5 hours = ~300 bars)
        if st.session_state.timeframe == "hour":
            # For hourly: add 30 extra calendar days for warm-up (minimum)
            warmup_days = 30
            data_days_with_warmup = days_back + warmup_days
        elif st.session_state.timeframe == "15min":
            # For 15min: add 30 extra calendar days for warm-up
            # (~22 trading days × 54 bars/day = ~1200 bars for 72/89 indicators)
            warmup_days = 30
            data_days_with_warmup = days_back + warmup_days
        elif st.session_state.timeframe == "5min":
            # For 5min: add 30 extra calendar days for warm-up
            # (~22 trading days × 162 bars/day = ~3600 bars for 72/89 indicators)
            warmup_days = 30
            data_days_with_warmup = days_back + warmup_days
        else:
            # For daily: add 120 trading days for warm-up (EMA 89 needs ~250 bars)
            warmup_days = 180  # Calendar days to ensure 120+ trading days
            data_days_with_warmup = days_back + warmup_days

        # Fetch data with warm-up period
        data = get_polygon_data(symbol, st.session_state.timeframe, data_days_with_warmup)

        if data is not None and len(data) > 0:
            # Calculate expected display bars (from user's days_back setting)
            if st.session_state.timeframe == "hour":
                # Approximate: 13.5 trading hours per day
                display_bars = int(days_back * 13.5)
            elif st.session_state.timeframe == "15min":
                # Approximate: 4 bars per hour × 13.5 trading hours = 54 bars per day
                display_bars = int(days_back * 54)
            elif st.session_state.timeframe == "5min":
                # For 5min: 4 AM to 8 PM = 16 hours
                # 12 bars per hour × 16 hours = 192 bars per day
                display_bars = int(days_back * 192)
            else:
                # Daily: each day is one bar (trading days only)
                display_bars = days_back

            # Debug info - show actual vs display bars
            st.write(f"Debug: Loaded {len(data)} records (displaying last {min(display_bars, len(data))}) for {symbol} - {st.session_state.timeframe}")

            chart_fig = create_chart(
                data,
                symbol,
                st.session_state.timeframe,
                display_bars=display_bars,
                show_vwap=show_vwap,
                show_prev_close=show_prev_close,
                show_920_bands=show_920_bands,
                show_920_cloud=show_920_cloud,
                show_7289_bands=show_7289_bands,
                show_7289_cloud=show_7289_cloud,
                zoom_to_candles=zoom_to_candles
            )
            st.plotly_chart(chart_fig, use_container_width=True)

            # Show recent stats
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Last Price", f"${data['close'].iloc[-1]:.2f}")
            with col2:
                change = data['close'].iloc[-1] - data['close'].iloc[-2] if len(data) > 1 else 0
                st.metric("Change", f"${change:.2f}")
            with col3:
                change_pct = (change / data['close'].iloc[-2] * 100) if len(data) > 1 else 0
                st.metric("Change %", f"{change_pct:.2f}%")
            with col4:
                avg_volume = data['volume'].mean()
                st.metric("Avg Volume", f"{avg_volume:,.0f}")
        else:
            st.error(f"No data available for {symbol} - {st.session_state.timeframe}")
            st.info("Please try switching back to Daily timeframe or refreshing")
    except Exception as e:
        st.error(f"Error processing chart: {str(e)}")
        st.info("Please try refreshing the page or switching timeframes")

if __name__ == "__main__":
    main()