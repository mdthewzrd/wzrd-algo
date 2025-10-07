"""
MTF Acceptance Tests
Tests for Multi-TimeFrame signal generation according to WZRD requirements
"""

import pandas as pd
import numpy as np
import sys
import os
from datetime import datetime, timedelta
import pytz

# Add utils to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))

from mtf_engine import MTFSignalGenerator
from signal_generator import SignalGenerator

class TestMTFAcceptance:
    """Acceptance tests for MTF functionality"""

    def setup_method(self):
        """Setup test data and configurations"""
        # Create sample data for September 2025
        self.tz = pytz.timezone('America/New_York')
        start_date = datetime(2025, 9, 1, 4, 0, 0)  # 4 AM ET
        end_date = datetime(2025, 9, 30, 20, 0, 0)  # 8 PM ET

        # Generate 5-minute data
        date_range = pd.date_range(start_date, end_date, freq='5min', tz=self.tz)

        # Create realistic price movement
        base_price = 450.0
        price_changes = np.random.normal(0, 0.001, len(date_range))
        prices = [base_price]

        for change in price_changes[1:]:
            new_price = prices[-1] * (1 + change)
            prices.append(new_price)

        self.sample_data = pd.DataFrame({
            'date': date_range,
            'open': [p * (1 + np.random.normal(0, 0.0005)) for p in prices],
            'high': [p * (1 + abs(np.random.normal(0, 0.002))) for p in prices],
            'low': [p * (1 - abs(np.random.normal(0, 0.002))) for p in prices],
            'close': prices,
            'volume': np.random.randint(100000, 1000000, len(date_range))
        })

        # Ensure proper OHLC relationships
        for i in range(len(self.sample_data)):
            row = self.sample_data.iloc[i]
            high = max(row['open'], row['close'], row['high'])
            low = min(row['open'], row['close'], row['low'])
            self.sample_data.iloc[i, self.sample_data.columns.get_loc('high')] = high
            self.sample_data.iloc[i, self.sample_data.columns.get_loc('low')] = low

    def test_golden_baseline_qqq(self):
        """Test 1: Golden Baseline - QQQ 5m EMA9 cross above EMA20 with 1h confirm"""
        strategy_config = {
            "strategy_name": "Golden_Baseline_QQQ_EMA9x20_1hConfirm",
            "description": "5m EMA9 cross above EMA20 with 1h confirmation",
            "timeframe": "5min",
            "symbol": "QQQ",
            "signals": [],
            "entry_conditions": [
                {
                    "type": "ema_crossover_with_time_filter",
                    "direction": "long",
                    "indicators": ["ema9_5min", "ema20_5min", "ema9_1h", "ema20_1h"],
                    "condition": "EMA9_5min > EMA20_5min AND previous_EMA9_5min <= previous_EMA20_5min AND EMA9_1h > EMA20_1h",
                    "time_filter": {"start": "08:00", "end": "13:00", "timezone": "America/New_York"}
                }
            ],
            "exit_conditions": [
                {"type": "ema_crossover_exit", "direction": "close_long", "condition": "EMA9_5min < EMA20_5min"}
            ]
        }

        generator = SignalGenerator(strategy_config)
        generator.load_data(self.sample_data)
        result = generator.generate_signals()

        signals = result['signals']
        entry_signals = [s for s in signals if 'entry' in s['type']]

        # Assert we have at least 1 signal in September 2025
        assert len(entry_signals) >= 1, f"Expected at least 1 entry signal, got {len(entry_signals)}"

        # Verify time filtering - all entries between 8am-1pm EST
        for signal in entry_signals:
            timestamp = pd.to_datetime(signal['timestamp']).tz_localize('America/New_York')
            hour = timestamp.hour
            assert 8 <= hour < 13, f"Entry signal at {timestamp} outside 8am-1pm window"

        print(f"✅ Golden Baseline QQQ: {len(entry_signals)} signals generated")

    def test_golden_baseline_spy(self):
        """Test 2: Golden Baseline - SPY version"""
        strategy_config = {
            "strategy_name": "Golden_Baseline_SPY_EMA9x20_1hConfirm",
            "timeframe": "5min",
            "symbol": "SPY",
            "signals": [],
            "entry_conditions": [
                {
                    "type": "ema_crossover_with_time_filter",
                    "direction": "long",
                    "condition": "EMA9_5min > EMA20_5min AND previous_EMA9_5min <= previous_EMA20_5min AND EMA9_1h > EMA20_1h",
                    "time_filter": {"start": "08:00", "end": "13:00", "timezone": "America/New_York"}
                }
            ],
            "exit_conditions": [
                {"type": "ema_crossover_exit", "direction": "close_long", "condition": "EMA9_5min < EMA20_5min"}
            ]
        }

        generator = SignalGenerator(strategy_config)
        generator.load_data(self.sample_data)
        result = generator.generate_signals()

        entry_signals = [s for s in result['signals'] if 'entry' in s['type']]
        assert len(entry_signals) >= 1, "Expected at least 1 entry signal for SPY"

        print(f"✅ Golden Baseline SPY: {len(entry_signals)} signals generated")

    def test_daily_gate_on(self):
        """Test 3: Daily Gate On - Add daily EMA condition"""
        strategy_config = {
            "strategy_name": "SPY_DailyGate_EMA9x20_with_Daily",
            "timeframe": "5min",
            "symbol": "SPY",
            "signals": [],
            "entry_conditions": [
                {
                    "type": "ema_crossover_with_time_filter",
                    "direction": "long",
                    "condition": "EMA9_5min > EMA20_5min AND previous_EMA9_5min <= previous_EMA20_5min AND EMA9_1h > EMA20_1h AND previous_EMA9_1d > previous_EMA20_1d",
                    "time_filter": {"start": "08:00", "end": "13:00", "timezone": "America/New_York"}
                }
            ],
            "exit_conditions": [
                {"type": "ema_crossover_exit", "direction": "close_long", "condition": "EMA9_5min < EMA20_5min"}
            ]
        }

        generator = SignalGenerator(strategy_config)
        generator.load_data(self.sample_data)
        result = generator.generate_signals()

        entry_signals = [s for s in result['signals'] if 'entry' in s['type']]

        # Should still have some signals (not necessarily as many due to additional filter)
        print(f"✅ Daily Gate On: {len(entry_signals)} signals generated with daily filter")

    def test_hourly_pullback_proxy(self):
        """Test 4: Hourly Pullback Proxy"""
        strategy_config = {
            "strategy_name": "SPY_HourlyPullback_Proxy",
            "timeframe": "5min",
            "symbol": "SPY",
            "signals": [],
            "entry_conditions": [
                {
                    "type": "ema_crossover_with_time_filter",
                    "direction": "long",
                    "condition": "EMA9_5min > EMA20_5min AND previous_EMA9_5min <= previous_EMA20_5min AND EMA9_1h > EMA20_1h AND previous_Close_1h < previous_EMA20_1h AND Close_1h > EMA20_1h",
                    "time_filter": {"start": "08:00", "end": "13:00", "timezone": "America/New_York"}
                }
            ],
            "exit_conditions": [
                {"type": "ema_crossover_exit", "direction": "close_long", "condition": "EMA9_5min < EMA20_5min"}
            ]
        }

        generator = SignalGenerator(strategy_config)
        generator.load_data(self.sample_data)
        result = generator.generate_signals()

        entry_signals = [s for s in result['signals'] if 'entry' in s['type']]

        # Should have at least some signals (pullback conditions are common)
        print(f"✅ Hourly Pullback Proxy: {len(entry_signals)} signals generated")

    def test_route_start_dev_bands(self):
        """Test 5: Route Start with DevBands"""
        strategy_config = {
            "strategy_name": "SPY_RouteStart_DevBands",
            "timeframe": "5min",
            "symbol": "SPY",
            "signals": [],
            "entry_conditions": [
                {
                    "type": "ema_crossover_with_time_filter",
                    "direction": "long",
                    "condition": "EMA9_5min > EMA20_5min AND previous_EMA9_5min <= previous_EMA20_5min AND EMA9_1h > EMA20_1h AND (Low_1h <= DevBand72_1h_Lower_6 OR Low_1h <= DevBand89_1h_Lower_6)",
                    "time_filter": {"start": "08:00", "end": "13:00", "timezone": "America/New_York"}
                }
            ],
            "exit_conditions": [
                {"type": "ema_crossover_exit", "direction": "close_long", "condition": "EMA9_5min < EMA20_5min"}
            ]
        }

        generator = SignalGenerator(strategy_config)
        generator.load_data(self.sample_data)
        result = generator.generate_signals()

        entry_signals = [s for s in result['signals'] if 'entry' in s['type']]

        print(f"✅ Route Start DevBands: {len(entry_signals)} signals generated")

    def test_time_filter_robustness(self):
        """Test 6: Time Filter Robustness - No entries outside 8am-1pm"""
        strategy_config = {
            "strategy_name": "TimeFilter_Robustness_Test",
            "timeframe": "5min",
            "symbol": "SPY",
            "signals": [],
            "entry_conditions": [
                {
                    "type": "ema_crossover_with_time_filter",
                    "direction": "long",
                    "condition": "EMA9_5min > EMA20_5min AND EMA9_1h > EMA20_1h",
                    "time_filter": {"start": "08:00", "end": "13:00", "timezone": "America/New_York"}
                }
            ],
            "exit_conditions": [
                {"type": "ema_crossover_exit", "direction": "close_long", "condition": "EMA9_5min < EMA20_5min"}
            ]
        }

        generator = SignalGenerator(strategy_config)
        generator.load_data(self.sample_data)
        result = generator.generate_signals()

        entry_signals = [s for s in result['signals'] if 'entry' in s['type']]

        # Verify NO entries outside time window
        for signal in entry_signals:
            timestamp = pd.to_datetime(signal['timestamp']).tz_localize('America/New_York')
            hour = timestamp.hour
            assert 8 <= hour < 13, f"VIOLATION: Entry signal at {timestamp} outside 8am-1pm window"

        print(f"✅ Time Filter Robustness: All {len(entry_signals)} entries within 8am-1pm EST")

    def test_comprehensive_rules_only_strategy(self):
        """Test 7: The comprehensive example from requirements"""
        strategy_config = {
            "strategy_name": "SPY_RULES_ONLY_Crossover_5m_with_Daily_and_RouteStart",
            "timeframe": "5min",
            "symbol": "SPY",
            "signals": [],
            "entry_conditions": [
                {
                    "type": "ema_crossover_with_time_filter",
                    "direction": "long",
                    "indicators": ["ema9_5min", "ema20_5min", "ema9_1h", "ema20_1h", "ema9_1D", "ema20_1D"],
                    "condition": "EMA9_5min > EMA20_5min AND previous_EMA9_5min <= previous_EMA20_5min AND EMA9_1h > EMA20_1h AND previous_EMA9_1D > previous_EMA20_1D AND (Low_1h <= DevBand72_1h_Lower_6 OR Low_1h <= DevBand89_1h_Lower_6)",
                    "time_filter": {"start": "08:00", "end": "13:00", "timezone": "America/New_York"}
                }
            ],
            "exit_conditions": [
                {"type": "ema_crossover_exit", "direction": "close_long", "condition": "EMA9_5min < EMA20_5min"}
            ]
        }

        generator = SignalGenerator(strategy_config)
        generator.load_data(self.sample_data)
        result = generator.generate_signals()

        signals = result['signals']
        entry_signals = [s for s in signals if 'entry' in s['type']]
        exit_signals = [s for s in signals if 'exit' in s['type']]

        # Verify MTF detection worked
        assert generator._is_mtf_strategy(), "Strategy should be detected as MTF"

        # Verify time filtering
        for signal in entry_signals:
            timestamp = pd.to_datetime(signal['timestamp']).tz_localize('America/New_York')
            hour = timestamp.hour
            assert 8 <= hour < 13, f"Entry signal at {timestamp} outside 8am-1pm window"

        # Verify we have proper signal structure
        for signal in entry_signals:
            assert 'timestamp' in signal
            assert 'type' in signal
            assert 'price' in signal
            assert 'shares' in signal
            assert 'reason' in signal
            assert 'direction' in signal

        print(f"✅ Comprehensive Strategy: {len(entry_signals)} entries, {len(exit_signals)} exits")

    def test_mtf_detection(self):
        """Test 8: MTF Detection Logic"""
        # Non-MTF strategy
        simple_strategy = {
            "entry_conditions": [
                {"condition": "EMA9 > EMA20 AND previous_EMA9 <= previous_EMA20"}
            ],
            "exit_conditions": [
                {"condition": "EMA9 < EMA20"}
            ]
        }

        generator1 = SignalGenerator(simple_strategy)
        assert not generator1._is_mtf_strategy(), "Simple strategy should not be MTF"

        # MTF strategy
        mtf_strategy = {
            "entry_conditions": [
                {"condition": "EMA9_5min > EMA20_5min AND EMA9_1h > EMA20_1h"}
            ],
            "exit_conditions": [
                {"condition": "EMA9_5min < EMA20_5min"}
            ]
        }

        generator2 = SignalGenerator(mtf_strategy)
        assert generator2._is_mtf_strategy(), "MTF strategy should be detected as MTF"

        print("✅ MTF Detection: Working correctly")

    def test_performance_and_caching(self):
        """Test 9: Performance and Caching"""
        strategy_config = {
            "strategy_name": "Performance_Test",
            "timeframe": "5min",
            "symbol": "SPY",
            "signals": [],
            "entry_conditions": [
                {
                    "condition": "EMA9_5min > EMA20_5min AND EMA9_1h > EMA20_1h AND EMA89_1h > EMA72_1h",
                    "time_filter": {"start": "08:00", "end": "13:00", "timezone": "America/New_York"}
                }
            ],
            "exit_conditions": [
                {"condition": "EMA9_5min < EMA20_5min"}
            ]
        }

        generator = SignalGenerator(strategy_config)
        generator.load_data(self.sample_data)

        # First run
        import time
        start_time = time.time()
        result1 = generator.generate_signals()
        first_run_time = time.time() - start_time

        # Second run (should use cached indicators)
        start_time = time.time()
        result2 = generator.generate_signals()
        second_run_time = time.time() - start_time

        # Results should be identical
        assert len(result1['signals']) == len(result2['signals'])

        print(f"✅ Performance Test: First run: {first_run_time:.3f}s, Second run: {second_run_time:.3f}s")

def run_acceptance_tests():
    """Run all acceptance tests"""
    test_instance = TestMTFAcceptance()
    test_instance.setup_method()

    tests = [
        test_instance.test_golden_baseline_qqq,
        test_instance.test_golden_baseline_spy,
        test_instance.test_daily_gate_on,
        test_instance.test_hourly_pullback_proxy,
        test_instance.test_route_start_dev_bands,
        test_instance.test_time_filter_robustness,
        test_instance.test_comprehensive_rules_only_strategy,
        test_instance.test_mtf_detection,
        test_instance.test_performance_and_caching
    ]

    print("\n🚀 Running MTF Acceptance Tests...\n")

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"❌ {test.__name__}: {str(e)}")
            failed += 1

    print(f"\n📊 Test Results: {passed} passed, {failed} failed")

    if failed == 0:
        print("🎉 All acceptance tests passed!")
        return True
    else:
        print("❌ Some tests failed. Check implementation.")
        return False

if __name__ == "__main__":
    run_acceptance_tests()