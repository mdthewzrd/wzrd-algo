"""
WZRD Chart Templates - Default Configurations
These are the standard chart templates for Daily, Hourly, 15min, and 5min timeframes.
"""

# Chart template configurations
CHART_TEMPLATES = {
    "day": {
        "default_days": 60,
        "bars_per_day": 1,
        "warmup_days": 180,  # ~120 trading days for EMA 89
        "indicators": {
            "vwap": False,
            "prev_close": False,
            "920_bands": True,
            "920_cloud": True,
            "7289_bands": False,
            "7289_cloud": False,
        },
        "zoom_to_candles": True,
        "use_rangebreaks": False,
        "description": "Daily chart with 9/20 EMA cloud and deviation bands"
    },

    "hour": {
        "default_days": 5,
        "bars_per_day": 13.5,  # 6.5 hours regular + 4 hours pre-market + 3 hours after-hours
        "warmup_days": 30,  # ~22 trading days × 13.5 hours = ~300 bars
        "indicators": {
            "vwap": True,
            "prev_close": True,
            "920_bands": True,
            "920_cloud": True,
            "7289_bands": True,
            "7289_cloud": True,
        },
        "zoom_to_candles": False,
        "use_rangebreaks": True,
        "rangebreaks": {
            "weekends": {"bounds": ["sat", "mon"]},
            "non_trading_hours": {"bounds": [20, 4], "pattern": "hour"}  # 8pm-4am
        },
        "description": "Hourly chart with all indicators (VWAP, prev close, 9/20, 72/89)"
    },

    "15min": {
        "default_days": 2,
        "bars_per_day": 54,  # 4 bars/hour × 13.5 hours
        "warmup_days": 3,  # Minimal warmup for speed
        "indicators": {
            "vwap": True,
            "prev_close": True,
            "920_bands": True,
            "920_cloud": True,
            "7289_bands": False,  # Disable for speed
            "7289_cloud": False,  # Disable for speed
        },
        "zoom_to_candles": False,
        "use_rangebreaks": True,
        "rangebreaks": {
            "weekends": {"bounds": ["sat", "mon"]},
            "non_trading_hours": {"bounds": [20, 4], "pattern": "hour"}
        },
        "description": "15-minute chart with all indicators"
    },

    "5min": {
        "default_days": 1,
        "bars_per_day": 192,  # 12 bars/hour × 16 hours (4am-8pm)
        "warmup_days": 30,  # ~22 trading days × 192 bars = ~4224 bars
        "indicators": {
            "vwap": True,
            "prev_close": True,
            "920_bands": True,
            "920_cloud": True,
            "7289_bands": True,
            "7289_cloud": True,
        },
        "zoom_to_candles": False,
        "use_rangebreaks": True,
        "rangebreaks": {
            "weekends": {"bounds": ["sat", "mon"]},
            "non_trading_hours": {"bounds": [20, 4], "pattern": "hour"}
        },
        "description": "5-minute chart showing 4am-8pm with all indicators"
    }
}

# Chart styling configuration
CHART_STYLE = {
    "theme": "plotly_dark",
    "paper_bgcolor": "#000000",
    "plot_bgcolor": "#000000",
    "candle_colors": {
        "increasing": "#FFFFFF",  # White bullish candles
        "decreasing": "#FF0000"   # Red bearish candles
    },
    "indicator_colors": {
        "vwap": "#FFD700",           # Gold
        "prev_close": "#808080",     # Gray dashed line
        "ema9": "#00FF00",           # Green
        "ema20": "#32CD32",          # Lime green
        "ema72": "#00FF00",          # Green
        "ema89": "#32CD32",          # Lime green
        "cloud_bullish": "#00FF00",  # Green (with opacity)
        "cloud_bearish": "#FF0000",  # Red (with opacity)
        "bands_above": "#8B0000",    # Dark red
        "bands_below": "#006400",    # Dark green
    },
    "layout": {
        "height": 800,
        "margin": {"l": 0, "r": 0, "t": 50, "b": 10},
        "showlegend": False,
        "hovermode": "x",
        "dragmode": "pan"
    },
    "grid": {
        "color": "#333333"
    }
}

# Slider configuration for each timeframe
SLIDER_CONFIG = {
    "day": {
        "min": 30,
        "max": 365,
        "help": "Number of days of daily data to display"
    },
    "hour": {
        "min": 1,
        "max": 30,
        "help": "Number of days of hourly data to display"
    },
    "15min": {
        "min": 3,
        "max": 30,
        "help": "Number of days of 15-minute data to display (paid Polygon plan fetches additional warm-up data automatically)"
    },
    "5min": {
        "min": 1,
        "max": 10,
        "help": "Number of days of 5-minute data to display (paid Polygon plan fetches additional warm-up data automatically)"
    }
}

def get_template(timeframe):
    """Get chart template configuration for a specific timeframe"""
    return CHART_TEMPLATES.get(timeframe, CHART_TEMPLATES["day"])

def get_slider_config(timeframe):
    """Get slider configuration for a specific timeframe"""
    return SLIDER_CONFIG.get(timeframe, SLIDER_CONFIG["day"])

def get_indicator_defaults(timeframe):
    """Get default indicator settings for a timeframe"""
    template = get_template(timeframe)
    return template.get("indicators", {})
