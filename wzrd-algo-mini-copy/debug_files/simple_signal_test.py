#!/usr/bin/env python3
"""
Simple test to verify signals are working
"""

import streamlit as st
import json
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from apps.strategy_viewer_enhanced import create_wzrd_chart_with_signals
from datetime import datetime

# Test with the pre-filled signals strategy
WORKING_SIGNALS_STRATEGY = {
    "strategy_name": "SPY_Working_Signals_Test",
    "description": "SPY strategy with actual signals that will display",
    "timeframe": "5min",
    "symbol": "SPY",
    "signals": [
        {
            "type": "entry_signal",
            "timestamp": "2024-10-01 09:35:00",
            "price": 575.25,
            "shares": 100,
            "reason": "EMA 9 crosses above EMA 20 with volume confirmation",
            "direction": "long",
            "position_id": "pos_1"
        },
        {
            "type": "exit_signal",
            "timestamp": "2024-10-01 14:20:00",
            "price": 578.80,
            "shares": 100,
            "reason": "EMA 9 crosses below EMA 20",
            "direction": "close_long",
            "position_id": "pos_1",
            "pnl": 355.0
        }
    ]
}

st.title("🧪 Simple Signal Test")

st.write("Testing signal generation directly...")

# Create chart
start_date = datetime(2024, 10, 1).date()
end_date = datetime(2024, 10, 3).date()

try:
    fig = create_wzrd_chart_with_signals(
        strategy_artifact=WORKING_SIGNALS_STRATEGY,
        selected_ticker="SPY",
        use_mock_data=True,
        start_date=start_date,
        end_date=end_date,
        chart_frequency="5min"
    )

    if fig:
        st.success("✅ Chart created successfully!")
        st.plotly_chart(fig, use_container_width=True)

        # Count signal traces
        signal_traces = len([trace for trace in fig.data if hasattr(trace, 'marker') and hasattr(trace.marker, 'color')])
        st.info(f"📊 Chart contains {len(fig.data)} total traces")

        # Look for colored markers
        colored_traces = []
        for i, trace in enumerate(fig.data):
            if hasattr(trace, 'marker') and hasattr(trace.marker, 'color'):
                color = str(trace.marker.color)
                if any(c in color for c in ['#00FF00', '#FFFF00', 'lime', 'yellow']):
                    colored_traces.append(f"Trace {i}: {color}")

        if colored_traces:
            st.success(f"🎯 Found {len(colored_traces)} signal traces:")
            for trace in colored_traces:
                st.write(f"  - {trace}")
        else:
            st.warning("⚠️ No signal traces found in chart data")

    else:
        st.error("❌ Chart creation failed!")

except Exception as e:
    st.error(f"❌ Error: {e}")
    import traceback
    st.code(traceback.format_exc())