#!/usr/bin/env python3
"""
Quick test to verify timezone handling is working
"""

import pandas as pd
from datetime import datetime
import pytz
from signal_generator import RulesEngine

def test_timezone_handling():
    """Test timezone handling in signal generation"""
    print("🔧 Testing timezone handling...")

    # Create mock data with timezone
    eastern = pytz.timezone('US/Eastern')
    dates = pd.date_range('2024-10-01 09:30', '2024-10-01 16:00', freq='5min', tz=eastern)

    # Create mock market data
    data = pd.DataFrame({
        'date': dates,
        'open': [100.0] * len(dates),
        'high': [101.0] * len(dates),
        'low': [99.0] * len(dates),
        'close': [100.5] * len(dates),
        'volume': [1000] * len(dates),
        'ema20': [100.0] * len(dates),
        'ema50': [99.0] * len(dates),
        'rsi': [35.0] * len(dates),
        'volume_ratio': [1.2] * len(dates)
    })

    # Simple strategy config
    strategy_config = {
        'symbol': 'TEST',
        'timeframe': '5min',
        'entry_conditions': [
            {
                'type': 'simple',
                'description': 'RSI oversold',
                'direction': 'long',
                'indicators': ['rsi'],
                'conditions': 'RSI < 40'
            }
        ],
        'exit_conditions': [],
        'risk_management': {
            'stop_loss': {'type': 'percentage', 'value': 1.0},
            'take_profit': {'type': 'r_multiple', 'value': 2.0},
            'position_size': {'type': 'r_based', 'value': 1.0},
            'pyramiding': {'enabled': False}
        }
    }

    try:
        # Create signal engine
        engine = RulesEngine(data, strategy_config)

        # Test timestamp conversion
        test_timestamp = dates[10]  # Pick a timestamp from our data
        converted = engine._convert_timestamp_with_tz(test_timestamp)

        print(f"✅ Original timestamp: {test_timestamp}")
        print(f"✅ Converted timestamp: {converted}")
        print(f"✅ Timezone match: {test_timestamp.tz == converted.tz}")

        # Test entry reason generation
        reason = engine._generate_entry_reason(converted, 'long')
        print(f"✅ Generated reason: {reason}")

        print("✅ Timezone handling test passed!")
        return True

    except Exception as e:
        print(f"❌ Timezone handling test failed: {e}")
        return False

if __name__ == "__main__":
    test_timezone_handling()