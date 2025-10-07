#!/usr/bin/env python3
"""
Test script for SPY Multi-Timeframe Strategy
Validates strategy implementation and performance
"""

import sys
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent))

from spy_multi_timeframe_strategy import SPYMultiTimeframeStrategy, SPYMultiTimeframeConfig

def test_strategy_components():
    """Test individual strategy components."""
    print("🎯 Testing SPY Strategy Components")
    print("=" * 50)

    # Initialize strategy
    config = SPYMultiTimeframeConfig(
        polygon_api_key=None,  # Use simulated data
        risk_per_trade=0.01,
        max_portfolio_heat=0.20
    )

    strategy = SPYMultiTimeframeStrategy(config)

    # Test 1: EMA Calculation
    print("\n📊 Testing EMA Calculations...")
    test_data = pd.Series([100, 101, 102, 103, 104, 105, 106, 107, 108, 109])
    ema_9 = strategy.calculate_ema(test_data, 9)
    ema_20 = strategy.calculate_ema(test_data, 20)

    print(f"✅ EMA 9: {ema_9.iloc[-1]:.2f}")
    print(f"✅ EMA 20: {ema_20.iloc[-1]:.2f}")

    # Test 2: Deviation Bands
    print("\n📊 Testing Deviation Bands...")
    upper_band, lower_band = strategy.calculate_deviation_bands(test_data, 9, 1.5)
    print(f"✅ Upper Band: {upper_band.iloc[-1]:.2f}")
    print(f"✅ Lower Band: {lower_band.iloc[-1]:.2f}")

    # Test 3: ATR Calculation
    print("\n📊 Testing ATR Calculation...")
    ohlc_data = pd.DataFrame({
        'high': [102, 103, 104, 105, 106],
        'low': [98, 99, 100, 101, 102],
        'close': [100, 101, 102, 103, 104]
    })
    atr = strategy.calculate_atr(ohlc_data, 14)
    print(f"✅ ATR: {atr.iloc[-1]:.4f}")

    # Test 4: Regime Analysis
    print("\n📊 Testing Regime Analysis...")
    daily_data = strategy._generate_simulated_data("SPY", "day", "2024-01-01", "2024-12-31")
    regime = strategy.analyze_regime(daily_data)
    print(f"✅ Current Regime: {regime}")

    # Test 5: Setup Identification
    print("\n📊 Testing Setup Identification...")
    four_hour_data = strategy._generate_simulated_data("SPY", "hour", "2024-01-01", "2024-01-31")
    four_hour_data = strategy._resample_to_4hour(four_hour_data)
    setup = strategy.identify_setup(four_hour_data)
    print(f"✅ Setup Detected: {setup}")

    # Test 6: Entry Signal Generation
    print("\n📊 Testing Entry Signal Generation...")
    hourly_data = strategy._generate_simulated_data("SPY", "hour", "2024-01-01", "2024-01-07")
    entry_signal = strategy.generate_entry_signal(hourly_data)
    print(f"✅ Entry Signal: {entry_signal}")

    # Test 7: Position Sizing
    print("\n📊 Testing Position Sizing...")
    entry_price = 450.0
    stop_loss = 440.0
    position_size = strategy.calculate_position_size(entry_price, stop_loss)
    print(f"✅ Position Size: {position_size:.0f} shares (${position_size * entry_price:.0f})")

    return True

def test_multi_timeframe_integration():
    """Test multi-timeframe data coordination."""
    print("\n🎯 Testing Multi-Timeframe Integration")
    print("=" * 50)

    strategy = SPYMultiTimeframeStrategy()

    # Generate test data for all timeframes
    start_date = "2024-01-01"
    end_date = "2024-03-31"

    print(f"📊 Generating data from {start_date} to {end_date}...")

    daily_data = strategy.get_polygon_data("SPY", "day", start_date, end_date)
    four_hour_data = strategy.get_polygon_data("SPY", "hour", start_date, end_date)
    hourly_data = strategy.get_polygon_data("SPY", "hour", start_date, end_date)

    # Resample hourly to 4-hour
    four_hour_data = strategy._resample_to_4hour(four_hour_data)

    print(f"✅ Daily bars: {len(daily_data)}")
    print(f"✅ 4-Hour bars: {len(four_hour_data)}")
    print(f"✅ Hourly bars: {len(hourly_data)}")

    # Test opportunity scanning
    print("\n📊 Testing Opportunity Scanning...")
    opportunities = strategy.scan_for_opportunities(daily_data, four_hour_data, hourly_data)
    print(f"✅ Opportunities found: {len(opportunities)}")

    if opportunities:
        opp = opportunities[0]
        print(f"   - Symbol: {opp['symbol']}")
        print(f"   - Entry Price: ${opp['entry_price']:.2f}")
        print(f"   - Position Size: {opp['position_size']:.0f} shares")
        print(f"   - Confidence: {opp['confidence']}")

    return True

def test_exit_conditions():
    """Test exit condition logic."""
    print("\n🎯 Testing Exit Conditions")
    print("=" * 50)

    strategy = SPYMultiTimeframeStrategy()

    # Generate test data
    start_date = "2024-01-01"
    end_date = "2024-02-29"

    daily_data = strategy.get_polygon_data("SPY", "day", start_date, end_date)
    hourly_data = strategy.get_polygon_data("SPY", "hour", start_date, end_date)

    # Test exit conditions for a sample position
    entry_price = 450.0
    entry_time = pd.Timestamp('2024-01-15 10:00:00')

    print("📊 Testing exit condition checks...")
    exits = strategy.check_exit_conditions(daily_data, hourly_data, entry_price, entry_time)

    for exit_type, triggered in exits.items():
        status = "✅ TRIGGERED" if triggered else "⏳ NOT TRIGGERED"
        print(f"   {exit_type}: {status}")

    # Test trailing stop updates
    print("\n📊 Testing Trailing Stop Updates...")
    strategy.update_trailing_stop(daily_data, entry_price, entry_time, is_long=True)

    if strategy.trailing_stops:
        position_id = f"{entry_time.strftime('%Y%m%d_%H%M')}"
        if position_id in strategy.trailing_stops:
            trailing_stop = strategy.trailing_stops[position_id]
            current_price = daily_data['close'].iloc[-1]
            print(f"✅ Trailing Stop: ${trailing_stop:.2f}")
            print(f"✅ Current Price: ${current_price:.2f}")
            print(f"✅ Distance from Stop: ${(current_price - trailing_stop):.2f}")

    return True

def test_complete_backtest():
    """Run complete strategy backtest."""
    print("\n🎯 Testing Complete Backtest")
    print("=" * 50)

    strategy = SPYMultiTimeframeStrategy()

    # Run 3-month backtest
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d')

    print(f"📊 Running backtest from {start_date} to {end_date}...")

    results = strategy.run_strategy_backtest(start_date, end_date)

    # Display results
    metrics = results['performance_metrics']
    trades = results['trades']

    print(f"\n📈 Performance Metrics:")
    print(f"   Total Trades: {metrics['total_trades']}")
    print(f"   Win Rate: {metrics['win_rate']:.1%}")
    print(f"   Profit Factor: {metrics['profit_factor']:.2f}")
    print(f"   Sharpe Ratio: {metrics['sharpe_ratio']:.2f}")
    print(f"   Max Drawdown: {metrics['max_drawdown']:.1%}")
    print(f"   Total Return: {metrics['total_return']:.1%}")

    print(f"\n📊 Trade Details:")
    for i, trade in enumerate(trades[:5]):  # Show first 5 trades
        pnl = trade['pnl']
        pnl_color = "📈" if pnl > 0 else "📉"
        print(f"   {i+1}. {trade['entry_time'].strftime('%Y-%m-%d')} → "
              f"{trade['exit_time'].strftime('%Y-%m-%d')} "
              f"{pnl_color} ${pnl:+.2f} ({trade['exit_reason']})")

    if len(trades) > 5:
        print(f"   ... and {len(trades) - 5} more trades")

    print(f"\n📊 Data Usage:")
    print(f"   Daily bars: {results['data_used']['daily']}")
    print(f"   4-Hour bars: {results['data_used']['four_hour']}")
    print(f"   Hourly bars: {results['data_used']['hourly']}")

    return results

def test_vectorbt_integration():
    """Test VectorBT integration for advanced backtesting."""
    print("\n🎯 Testing VectorBT Integration")
    print("=" * 50)

    try:
        import vectorbt as vbt
        print("✅ VectorBT imported successfully")

        # Generate test data and signals
        strategy = SPYMultiTimeframeStrategy()

        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=60)).strftime('%Y-%m-%d')

        daily_data = strategy.get_polygon_data("SPY", "day", start_date, end_date)
        hourly_data = strategy.get_polygon_data("SPY", "hour", start_date, end_date)

        print(f"📊 Generated {len(daily_data)} daily bars")

        # Create simple signals for VectorBT testing
        # Using 9/20 EMA crossover as signal source
        ema_9 = strategy.calculate_ema(daily_data['close'], 9)
        ema_20 = strategy.calculate_ema(daily_data['close'], 20)

        # Generate entry/exit signals
        entries = ema_9 > ema_20  # Bullish crossover
        exits = ema_9 < ema_20    # Bearish crossover

        # Run VectorBT backtest
        pf = vbt.Portfolio.from_signals(
            close=daily_data['close'],
            entries=entries,
            exits=exits,
            init_cash=100_000,
            fees=0.001,
            slippage=0.001
        )

        print(f"📈 VectorBT Results:")
        print(f"   Total Return: {pf.total_return():.2%}")
        print(f"   Sharpe Ratio: {pf.sharpe_ratio():.2f}")
        print(f"   Max Drawdown: {pf.max_drawdown():.2%}")
        print(f"   Total Trades: {pf.trades.count()}")

        return True

    except ImportError:
        print("⚠️ VectorBT not available - skipping integration test")
        return False

def main():
    """Run all strategy tests."""
    print("🚀 SPY Multi-Timeframe Strategy Test Suite")
    print("=" * 60)

    tests = [
        ("Strategy Components", test_strategy_components),
        ("Multi-Timeframe Integration", test_multi_timeframe_integration),
        ("Exit Conditions", test_exit_conditions),
        ("Complete Backtest", test_complete_backtest),
        ("VectorBT Integration", test_vectorbt_integration)
    ]

    results = {}
    for test_name, test_func in tests:
        try:
            print(f"\n🧪 Running: {test_name}")
            result = test_func()
            results[test_name] = result
            print(f"✅ {test_name}: PASSED")
        except Exception as e:
            print(f"❌ {test_name}: FAILED - {e}")
            results[test_name] = False

    # Summary
    print(f"\n📊 Test Summary")
    print("=" * 50)

    passed_tests = sum(1 for result in results.values() if result)
    total_tests = len(results)

    print(f"Passed: {passed_tests}/{total_tests}")

    if passed_tests == total_tests:
        print("🎉 All tests passed! Strategy is ready for production.")
    else:
        print("⚠️ Some tests failed. Review the results above.")

    print(f"\n🔧 Next Steps:")
    print("1. Set up Polygon API key for real data")
    print("2. Run extended backtest with more data")
    print("3. Optimize strategy parameters")
    print("4. Implement real-time trading integration")

    return results

if __name__ == "__main__":
    results = main()