#!/usr/bin/env python3
"""
Debug SPY Strategy - Test with real market-like data patterns
"""

import sys
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent))

from spy_multi_timeframe_strategy import SPYMultiTimeframeStrategy, SPYMultiTimeframeConfig

def create_test_data():
    """Create realistic test data with clear patterns."""
    print("🔧 Creating realistic test data with clear patterns...")

    # Create 1 year of hourly data
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)

    # Generate hourly timestamps
    dates = pd.date_range(start=start_date, end=end_date, freq='H')
    dates = dates[dates.hour < 20]  # Market hours only (approximate)

    # Base price around SPY level
    base_price = 500.0

    # Create realistic price movements with trends and dips
    np.random.seed(42)  # For reproducible results
    prices = []

    for i, date in enumerate(dates):
        if i == 0:
            price = base_price
        else:
            # Add trend component
            trend = 0.0001  # Slight upward trend

            # Add cyclical component (daily/weekly patterns)
            daily_cycle = 0.002 * np.sin(2 * np.pi * i / 24)  # Daily pattern
            weekly_cycle = 0.005 * np.sin(2 * np.pi * i / (24 * 5))  # Weekly pattern

            # Add random walk
            random_change = np.random.normal(0, 0.005)  # 0.5% std dev

            # Combine components
            price_change = trend + daily_cycle + weekly_cycle + random_change

            # Add some larger dips periodically
            if i % (24 * 10) == 0:  # Every 10 days
                price_change -= 0.02  # 2% dip

            price = prices[-1] * (1 + price_change)

        prices.append(max(price, 100))  # Prevent negative prices

    # Create DataFrame
    df = pd.DataFrame({
        'open': prices,
        'high': [p * (1 + abs(np.random.normal(0, 0.003))) for p in prices],
        'low': [p * (1 - abs(np.random.normal(0, 0.003))) for p in prices],
        'close': prices,
        'volume': [int(1e6 + np.random.normal(0, 2e5)) for _ in prices]
    }, index=dates)

    print(f"✅ Created {len(df)} hourly bars")
    return df

def debug_indicators():
    """Debug the indicator calculations and entry conditions."""
    config = SPYMultiTimeframeConfig(
        polygon_api_key=None,
        risk_per_trade=0.01,
        max_portfolio_heat=0.20,
        deviation_std=1.5
    )

    strategy = SPYMultiTimeframeStrategy(config)

    # Create test data
    hourly_data = create_test_data()

    # Resample to 4-hour and daily
    four_hour_data = strategy._resample_to_4hour(hourly_data.copy())
    daily_data = hourly_data.resample('D').agg({
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last',
        'volume': 'sum'
    }).dropna()

    print(f"📊 Data periods:")
    print(f"   Daily: {len(daily_data)} bars")
    print(f"   4-Hour: {len(four_hour_data)} bars")
    print(f"   Hourly: {len(hourly_data)} bars")

    # Calculate indicators
    print("\n📊 Calculating indicators...")

    # Daily regime
    daily_ema_9 = strategy.calculate_ema(daily_data['close'], 9)
    daily_ema_20 = strategy.calculate_ema(daily_data['close'], 20)
    bullish_regime = daily_ema_9 > daily_ema_20

    # 4-hour indicators
    four_hour_ema_9 = strategy.calculate_ema(four_hour_data['close'], 9)
    four_hour_ema_20 = strategy.calculate_ema(four_hour_data['close'], 20)
    four_hour_upper_dev, four_hour_lower_dev = strategy.calculate_deviation_bands(
        four_hour_data['close'], 9, config.deviation_std
    )

    # Hourly indicators
    hourly_ema_9 = strategy.calculate_ema(hourly_data['close'], 9)
    hourly_ema_20 = strategy.calculate_ema(hourly_data['close'], 20)

    # Check conditions
    print("\n🔍 Analyzing conditions...")

    # Count bullish periods
    daily_bullish_count = bullish_regime.sum()
    four_hour_bullish = four_hour_ema_9 > four_hour_ema_20
    four_hour_bullish_count = four_hour_bullish.sum()

    print(f"   Daily bullish periods: {daily_bullish_count}/{len(daily_data)} ({daily_bullish_count/len(daily_data):.1%})")
    print(f"   4-hour bullish periods: {four_hour_bullish_count}/{len(four_hour_data)} ({four_hour_bullish_count/len(four_hour_data):.1%})")

    # Check dip detection
    four_hour_dips = four_hour_data['close'] <= four_hour_lower_dev * 1.02
    dip_count = four_hour_dips.sum()

    print(f"   4-hour dips detected: {dip_count}/{len(four_hour_data)} ({dip_count/len(four_hour_data):.1%})")

    # Check combined conditions
    combined_conditions = []
    for i, (time, row) in enumerate(four_hour_data.iterrows()):
        if four_hour_dips.loc[time] and four_hour_bullish.loc[time]:
            daily_date = time.date()
            if daily_date in daily_data.index and bullish_regime.loc[daily_date]:
                combined_conditions.append(time)

    print(f"   Combined dip + bullish conditions: {len(combined_conditions)}")

    # Show some sample data
    if len(combined_conditions) > 0:
        print(f"\n📋 Sample dip opportunities:")
        for i, time in enumerate(combined_conditions[:5]):
            daily_date = time.date()
            four_hour_price = four_hour_data.loc[time, 'close']
            lower_dev = four_hour_lower_dev.loc[time]

            print(f"   {i+1}. {time.strftime('%Y-%m-%d %H:%M')}")
            print(f"      4-hour price: ${four_hour_price:.2f}")
            print(f"      Lower band: ${lower_dev:.2f}")
            print(f"      Daily bullish: {bullish_regime.loc[daily_date]}")

            # Check for hourly entries in next 8 hours
            entry_window_end = time + pd.Timedelta(hours=8)
            hourly_candidates = hourly_data[(hourly_data.index > time) & (hourly_data.index <= entry_window_end)]

            if len(hourly_candidates) > 0:
                print(f"      Hourly candidates: {len(hourly_candidates)} bars")
                # Show first few hourly prices
                for j, (h_time, h_row) in enumerate(hourly_candidates.head(3).iterrows()):
                    h_momentum = (h_row['close'] - four_hour_price) / four_hour_price
                    h_bullish = hourly_ema_9.loc[h_time] > hourly_ema_20.loc[h_time]
                    print(f"         {h_time.strftime('%H:%M')}: ${h_row['close']:.2f} "
                          f"(momentum: {h_momentum:+.2%}, bullish: {h_bullish})")

    return True

def main():
    """Main debug function."""
    print("🔧 SPY Strategy Debug Analysis")
    print("=" * 50)
    print("Testing with realistic market data patterns")

    debug_indicators()

    print(f"\n✅ Debug analysis complete!")
    print(f"   If no trades are found, the issue is likely:")
    print(f"   1. Entry conditions too strict")
    print(f"   2. Simulated data doesn't have clear patterns")
    print(f"   3. Indicator calculation issues")

if __name__ == "__main__":
    main()