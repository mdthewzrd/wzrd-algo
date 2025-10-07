#!/usr/bin/env python3
"""
Quick test script to verify the date selection fix is working
"""

import sys
import os
sys.path.append('/Users/michaeldurante/wzrd-algo/wzrd-algo-mini-clean')
sys.path.append('/Users/michaeldurante/wzrd-algo/wzrd-algo-mini-clean/apps')

# Import the fixed function
from strategy_platform_complete import create_overview_chart, load_strategy_with_real_data

def test_date_fix():
    """Test the date selection fix"""

    print("🧪 Testing Date Selection Fix")
    print("=" * 50)

    # Test with August 5, 2025 (different from default)
    test_date = "2025-08-05"
    strategy_file = "ema_dual_timeframe_strategy.json"

    print(f"📅 Testing with date: {test_date}")
    print(f"📈 Using strategy: {strategy_file}")
    print()

    try:
        # Load strategy and data
        print("📊 Loading strategy and data...")
        strategy, df = load_strategy_with_real_data(test_date, strategy_file, True, None)

        if strategy is None or df is None:
            print("❌ Failed to load strategy or data")
            return False

        print(f"✅ Loaded strategy with {len(strategy.get('signals', []))} signals")
        print(f"✅ Loaded {len(df)} data points")
        print(f"📊 Data range: {df['date'].min()} to {df['date'].max()}")
        print()

        # Test overview chart creation (this should trigger our debug messages)
        print("📈 Creating overview chart (this will show debug messages)...")
        print("-" * 30)

        signals = strategy.get('signals', [])
        fig = create_overview_chart(df, strategy, signals)

        print("-" * 30)

        if fig is not None:
            print("✅ Overview chart created successfully")
            print(f"📊 Chart has {len(fig.data)} traces")
            return True
        else:
            print("❌ Overview chart creation failed")
            return False

    except Exception as e:
        print(f"❌ Error during test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_date_fix()
    print()
    print("=" * 50)
    if success:
        print("🎉 Test completed - check debug messages above for date fix verification")
    else:
        print("💥 Test failed - see error messages above")