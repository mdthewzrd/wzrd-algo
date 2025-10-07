#!/usr/bin/env python3
"""
Simple test script to verify the polygon data date fix
"""

import sys
import os
sys.path.append('/Users/michaeldurante/wzrd-algo/wzrd-algo-mini-clean')
sys.path.append('/Users/michaeldurante/wzrd-algo/wzrd-algo-mini-clean/utils')

from polygon_data import get_spy_data_for_strategy
from datetime import datetime

def test_date_loading():
    """Test the date selection fix directly"""

    print("🧪 Testing Date Selection Fix")
    print("=" * 50)

    # Test with August 5, 2025 (different from default)
    test_date = "2025-08-05"

    print(f"📅 Testing with date: {test_date}")
    print(f"🔍 Expected: Data should be from exactly {test_date}")
    print()

    try:
        # Load data for the specific date
        print("📊 Loading data with get_spy_data_for_strategy...")
        df = get_spy_data_for_strategy(test_date, "5min")

        if df is None or len(df) == 0:
            print("❌ No data returned")
            return False

        print(f"✅ Loaded {len(df)} data points")

        # Check the date range of the data
        min_date = df['date'].min()
        max_date = df['date'].max()

        print(f"📊 Data range: {min_date} to {max_date}")

        # Extract just the date part for comparison
        min_date_str = min_date.strftime("%Y-%m-%d")
        max_date_str = max_date.strftime("%Y-%m-%d")

        print(f"📅 Date only: {min_date_str} to {max_date_str}")

        # Verify the date matches what we requested
        if min_date_str == test_date and max_date_str == test_date:
            print("✅ SUCCESS: Data matches requested date exactly!")
            return True
        elif min_date_str == test_date:
            print("✅ SUCCESS: Data starts from requested date (partial day data)")
            return True
        else:
            print(f"❌ FAIL: Data date range doesn't match requested date {test_date}")
            print(f"   Expected: {test_date}")
            print(f"   Got: {min_date_str} to {max_date_str}")
            return False

    except Exception as e:
        print(f"❌ Error during test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_date_loading()
    print()
    print("=" * 50)
    if success:
        print("🎉 Date selection fix is working correctly!")
    else:
        print("💥 Date selection fix needs attention")