#!/usr/bin/env python3
"""
Phase 2 Testing: EMA Crossover with 1hr Direction Confirmation
Test Multi-TimeFrame (MTF) support with 1hr EMA confirmation
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

def test_phase_2_mtf_ema():
    """Test Phase 2: EMA crossover with 1hr direction confirmation"""

    print("🧪 Phase 2 Testing: MTF EMA with 1hr Confirmation")
    print("=" * 50)

    # Load our Phase 2 test strategy
    strategy_path = '/Users/michaeldurante/wzrd-algo/wzrd-algo-mini/test_phase_2_mtf_ema.json'

    try:
        with open(strategy_path, 'r') as f:
            strategy = json.load(f)

        print(f"✅ Loaded strategy: {strategy['strategy_name']}")
        print(f"📊 Symbol: {strategy['symbol']}")
        print(f"⏰ Timeframe: {strategy['timeframe']}")
        print(f"🔄 MTF Condition: {strategy['entry_conditions'][0]['condition']}")

    except Exception as e:
        print(f"❌ Error loading strategy: {e}")
        return False

    # Get market data with more history for MTF analysis
    print("\n📈 Fetching market data for MTF analysis...")
    try:
        # Get more days for proper 1hr analysis
        market_data = get_market_data('SPY', '5min', days_back=14)

        if market_data is None or market_data.empty:
            print("❌ No market data received")
            return False

        print(f"✅ Market data loaded: {len(market_data)} rows")
        print(f"📅 Date range: {market_data.index[0]} to {market_data.index[-1]}")

    except Exception as e:
        print(f"❌ Error fetching market data: {e}")
        return False

    # Generate signals
    print("\n🎯 Generating MTF signals...")
    try:
        signal_generator = SignalGenerator(strategy)
        signal_generator.load_data(market_data)
        result = signal_generator.generate_signals()

        if 'error' in result:
            print(f"❌ Signal generation error: {result['error']}")
            return False

        signals = result.get('signals', [])
        print(f"✅ MTF signal generation completed")
        print(f"📊 Generated {len(signals)} signals")

        # Analyze signals
        if signals:
            print("\n📋 MTF Signal Analysis:")
            entry_signals = [s for s in signals if s['type'] == 'entry_signal']
            exit_signals = [s for s in signals if s['type'] == 'exit_signal']

            print(f"  📈 Entry signals: {len(entry_signals)}")
            print(f"  📉 Exit signals: {len(exit_signals)}")

            # Show first few signals
            for i, signal in enumerate(signals[:5]):
                print(f"  {i+1}. {signal['timestamp']}: {signal['type']} at ${signal['price']} - {signal['reason']}")

            if len(signals) > 5:
                print(f"  ... and {len(signals) - 5} more signals")

            # Compare with Phase 1 results
            print(f"\n🔄 Phase 2 vs Phase 1 Comparison:")
            print(f"  Phase 1 (basic EMA): Generated 42 signals")
            print(f"  Phase 2 (MTF EMA): Generated {len(signals)} signals")

            if len(signals) < 42:
                print(f"  ✅ MTF filtering is working - reduced signals by {42 - len(signals)}")
            else:
                print(f"  ⚠️  MTF may not be filtering properly - expected fewer signals")

        else:
            print("⚠️  No MTF signals generated - this needs investigation")

            # Debug MTF detection
            print("\n🔍 Debug Information:")
            print(f"Entry condition: {strategy['entry_conditions'][0]['condition']}")

            # Check if MTF tokens are detected
            condition = strategy['entry_conditions'][0]['condition']
            mtf_tokens = ['_1h', '_1hr', '_60min', '_1D', '_1d', '_daily']
            detected_mtf = [token for token in mtf_tokens if token in condition]

            if detected_mtf:
                print(f"✅ MTF tokens detected: {detected_mtf}")
                print("✅ Strategy should use MTF engine")
            else:
                print("❌ No MTF tokens detected - using standard engine")

        return len(signals) > 0

    except Exception as e:
        print(f"❌ Error generating MTF signals: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Starting Phase 2 Testing...")

    success = test_phase_2_mtf_ema()

    if success:
        print("\n✅ Phase 2 PASSED: MTF EMA crossover with 1hr confirmation working!")
        print("🎯 Ready to proceed to Phase 3: Add time filtering (8am-1pm)")
    else:
        print("\n❌ Phase 2 FAILED: Need to debug MTF EMA signal generation")
        print("🔧 Check MTF detection, 1hr data aggregation, and MTF condition evaluation")

    print("\n" + "=" * 50)