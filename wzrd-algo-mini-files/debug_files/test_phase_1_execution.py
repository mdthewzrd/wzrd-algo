#!/usr/bin/env python3
"""
Phase 1 Testing: Basic EMA Crossover Signal Generation
Test the simplest case to verify signal generation works
"""

import sys
import os
sys.path.append('/Users/michaeldurante/wzrd-algo/wzrd-algo-mini')

# Load environment variables
from dotenv import load_dotenv
load_dotenv('/Users/michaeldurante/wzrd-algo/wzrd-algo-mini/.env')

import json
from utils.signal_generator import SignalGenerator
from utils.data_integration import get_market_data

def test_phase_1_basic_ema():
    """Test Phase 1: Basic EMA crossover only"""

    print("🧪 Phase 1 Testing: Basic EMA Crossover")
    print("=" * 50)

    # Load our Phase 1 test strategy
    strategy_path = '/Users/michaeldurante/wzrd-algo/wzrd-algo-mini/test_phase_1_basic_ema.json'

    try:
        with open(strategy_path, 'r') as f:
            strategy = json.load(f)

        print(f"✅ Loaded strategy: {strategy['strategy_name']}")
        print(f"📊 Symbol: {strategy['symbol']}")
        print(f"⏰ Timeframe: {strategy['timeframe']}")

    except Exception as e:
        print(f"❌ Error loading strategy: {e}")
        return False

    # Get market data with correct API signature
    print("\n📈 Fetching market data...")
    try:
        # Use correct signature: symbol, timeframe, days_back
        market_data = get_market_data('SPY', '5min', days_back=5)

        if market_data is None or market_data.empty:
            print("❌ No market data received")
            return False

        print(f"✅ Market data loaded: {len(market_data)} rows")
        print(f"📅 Date range: {market_data.index[0]} to {market_data.index[-1]}")

    except Exception as e:
        print(f"❌ Error fetching market data: {e}")
        return False

    # Generate signals
    print("\n🎯 Generating signals...")
    try:
        signal_generator = SignalGenerator(strategy)
        signal_generator.load_data(market_data)
        result = signal_generator.generate_signals()

        if 'error' in result:
            print(f"❌ Signal generation error: {result['error']}")
            return False

        signals = result.get('signals', [])
        print(f"✅ Signal generation completed")
        print(f"📊 Generated {len(signals)} signals")

        # Analyze signals
        if signals:
            print("\n📋 Signal Analysis:")
            entry_signals = [s for s in signals if s['type'] == 'entry_signal']
            exit_signals = [s for s in signals if s['type'] == 'exit_signal']

            print(f"  📈 Entry signals: {len(entry_signals)}")
            print(f"  📉 Exit signals: {len(exit_signals)}")

            # Show first few signals
            for i, signal in enumerate(signals[:5]):
                print(f"  {i+1}. {signal['timestamp']}: {signal['type']} at ${signal['price']} - {signal['reason']}")

            if len(signals) > 5:
                print(f"  ... and {len(signals) - 5} more signals")
        else:
            print("⚠️  No signals generated - this needs investigation")

            # Debug: Check if EMA data exists
            print("\n🔍 Debug Information:")
            print(f"Market data columns: {list(market_data.columns)}")
            print(f"Market data shape: {market_data.shape}")

            # Check if we have basic OHLCV data
            required_cols = ['open', 'high', 'low', 'close', 'volume']
            missing_cols = [col for col in required_cols if col not in market_data.columns]
            if missing_cols:
                print(f"❌ Missing required columns: {missing_cols}")
            else:
                print("✅ All required OHLCV columns present")

        return len(signals) > 0

    except Exception as e:
        print(f"❌ Error generating signals: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Starting Phase 1 Testing...")

    success = test_phase_1_basic_ema()

    if success:
        print("\n✅ Phase 1 PASSED: Basic EMA crossover signals generated!")
        print("🎯 Ready to proceed to Phase 2: Add 1hr EMA direction confirmation")
    else:
        print("\n❌ Phase 1 FAILED: Need to debug basic EMA signal generation")
        print("🔧 Check market data, EMA calculations, and entry conditions")

    print("\n" + "=" * 50)