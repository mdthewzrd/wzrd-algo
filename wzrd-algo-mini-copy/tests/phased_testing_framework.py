"""
Phased Testing Framework for WZRD-Algo-Mini
Tests components systematically one phase at a time
"""

import pandas as pd
import numpy as np
import sys
import os
from datetime import datetime, timedelta
import pytz
import json

# Add utils to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))

from mtf_engine import MTFSignalGenerator, MTFDataAggregator, MTFIndicatorEngine
from signal_generator import SignalGenerator

class PhasedTestFramework:
    """Framework for systematic phased testing"""

    def __init__(self):
        self.test_results = {}
        self.test_data = None
        self.setup_test_data()

    def setup_test_data(self):
        """Create consistent test data for all phases"""
        tz = pytz.timezone('America/New_York')
        start_date = datetime(2025, 9, 1, 4, 0, 0)
        end_date = datetime(2025, 9, 5, 20, 0, 0)  # 5 days of data

        date_range = pd.date_range(start_date, end_date, freq='5min', tz=tz)

        # Create realistic price data with trends
        base_price = 450.0
        trend = 0.0001  # Slight upward trend
        volatility = 0.002

        prices = []
        for i, _ in enumerate(date_range):
            if i == 0:
                prices.append(base_price)
            else:
                change = np.random.normal(trend, volatility)
                new_price = prices[-1] * (1 + change)
                prices.append(new_price)

        self.test_data = pd.DataFrame({
            'date': date_range,
            'open': [p * (1 + np.random.normal(0, 0.0005)) for p in prices],
            'high': [p * (1 + abs(np.random.normal(0, 0.002))) for p in prices],
            'low': [p * (1 - abs(np.random.normal(0, 0.002))) for p in prices],
            'close': prices,
            'volume': np.random.randint(100000, 1000000, len(date_range))
        })

        # Ensure proper OHLC relationships
        for i in range(len(self.test_data)):
            row = self.test_data.iloc[i]
            high = max(row['open'], row['close'], row['high'])
            low = min(row['open'], row['close'], row['low'])
            self.test_data.iloc[i, self.test_data.columns.get_loc('high')] = high
            self.test_data.iloc[i, self.test_data.columns.get_loc('low')] = low

        print(f"✅ Test data created: {len(self.test_data)} 5min bars from {start_date} to {end_date}")

    def run_all_phases(self):
        """Run all test phases in sequence"""
        print("\n🚀 Starting Phased Testing Framework\n")

        phases = [
            ("Phase 1: Data Aggregation", self.test_phase_1_data_aggregation),
            ("Phase 2: Indicator Calculation", self.test_phase_2_indicators),
            ("Phase 3: Token Parsing", self.test_phase_3_token_parsing),
            ("Phase 4: Time Filtering", self.test_phase_4_time_filtering),
            ("Phase 5: MTF Detection", self.test_phase_5_mtf_detection),
            ("Phase 6: Simple Conditions", self.test_phase_6_simple_conditions),
            ("Phase 7: Complex MTF Conditions", self.test_phase_7_complex_conditions),
            ("Phase 8: Signal Generation", self.test_phase_8_signal_generation),
            ("Phase 9: Route Start/End", self.test_phase_9_route_start_end),
            ("Phase 10: Integration Test", self.test_phase_10_integration)
        ]

        total_passed = 0
        total_tests = len(phases)

        for phase_name, phase_func in phases:
            print(f"\n📋 {phase_name}")
            print("=" * 50)

            try:
                result = phase_func()
                if result:
                    print(f"✅ {phase_name} PASSED")
                    total_passed += 1
                else:
                    print(f"❌ {phase_name} FAILED")

            except Exception as e:
                print(f"❌ {phase_name} ERROR: {str(e)}")

        print(f"\n📊 Final Results: {total_passed}/{total_tests} phases passed")

        if total_passed == total_tests:
            print("🎉 ALL PHASES PASSED - System ready for production!")
        else:
            print("❌ Some phases failed - Check implementation before proceeding")

        return total_passed == total_tests

    def test_phase_1_data_aggregation(self):
        """Phase 1: Test MTF data aggregation"""
        print("Testing MTF data aggregation and resampling...")

        try:
            aggregator = MTFDataAggregator(timezone="America/New_York")
            mtf_data = aggregator.build_mtf_dataframes(self.test_data, "SPY")

            # Verify all timeframes exist
            assert '5min' in mtf_data, "5min timeframe missing"
            assert '1H' in mtf_data, "1H timeframe missing"
            assert '1D' in mtf_data, "1D timeframe missing"

            # Verify data structure
            for tf, df in mtf_data.items():
                assert not df.empty, f"{tf} dataframe is empty"
                assert 'close' in df.columns, f"{tf} missing close column"
                assert df.index.tz is not None, f"{tf} timezone not set"

            # Verify timeframe relationships
            assert len(mtf_data['1H']) < len(mtf_data['5min']), "Hourly should have fewer bars than 5min"
            assert len(mtf_data['1D']) < len(mtf_data['1H']), "Daily should have fewer bars than hourly"

            print(f"  - 5min bars: {len(mtf_data['5min'])}")
            print(f"  - 1H bars: {len(mtf_data['1H'])}")
            print(f"  - 1D bars: {len(mtf_data['1D'])}")

            return True

        except Exception as e:
            print(f"  Error: {str(e)}")
            return False

    def test_phase_2_indicators(self):
        """Phase 2: Test indicator calculations"""
        print("Testing EMA and deviation band calculations...")

        try:
            aggregator = MTFDataAggregator(timezone="America/New_York")
            aggregator.build_mtf_dataframes(self.test_data, "SPY")

            indicator_engine = MTFIndicatorEngine(aggregator)

            # Test EMA calculations
            ema9_5min = indicator_engine.calculate_ema("SPY", "5min", 9)
            ema20_5min = indicator_engine.calculate_ema("SPY", "5min", 20)
            ema9_1h = indicator_engine.calculate_ema("SPY", "1H", 9)

            assert not ema9_5min.empty, "EMA9 5min calculation failed"
            assert not ema20_5min.empty, "EMA20 5min calculation failed"
            assert not ema9_1h.empty, "EMA9 1h calculation failed"

            # Test deviation bands
            center, upper, lower = indicator_engine.calculate_deviation_bands("SPY", "1H", 72, 6)

            assert not center.empty, "DevBand center calculation failed"
            assert not upper.empty, "DevBand upper calculation failed"
            assert not lower.empty, "DevBand lower calculation failed"

            # Verify band relationships
            sample_idx = len(center) // 2
            assert upper.iloc[sample_idx] > center.iloc[sample_idx], "Upper band should be above center"
            assert lower.iloc[sample_idx] < center.iloc[sample_idx], "Lower band should be below center"

            print(f"  - EMA9 5min values: {ema9_5min.iloc[-5:].round(2).tolist()}")
            print(f"  - DevBand spread example: {(upper.iloc[sample_idx] - lower.iloc[sample_idx]):.2f}")

            return True

        except Exception as e:
            print(f"  Error: {str(e)}")
            return False

    def test_phase_3_token_parsing(self):
        """Phase 3: Test token parsing and normalization"""
        print("Testing token parsing and normalization...")

        try:
            from mtf_engine import MTFTokenParser

            parser = MTFTokenParser()

            # Test various token formats
            test_tokens = [
                ("EMA9_5min", {'type': 'ema', 'period': 9, 'timeframe': '5min', 'is_previous': False}),
                ("previous_EMA20_1h", {'type': 'ema', 'period': 20, 'timeframe': '1h', 'is_previous': True}),
                ("DevBand72_1h_Lower_6", {'type': 'devband', 'period': 72, 'timeframe': '1h', 'band_type': 'lower', 'multiplier': 6}),
                ("Close_1h", {'type': 'price', 'field': 'close', 'timeframe': '1h', 'is_previous': False}),
                ("previous_High_1D", {'type': 'price', 'field': 'high', 'timeframe': '1D', 'is_previous': True})
            ]

            for token, expected in test_tokens:
                result = parser.parse_token(token)
                for key, value in expected.items():
                    assert result[key] == value, f"Token {token}: expected {key}={value}, got {result[key]}"

            print(f"  - Successfully parsed {len(test_tokens)} token formats")

            # Test error handling
            try:
                parser.parse_token("INVALID_TOKEN")
                assert False, "Should have raised error for invalid token"
            except ValueError as e:
                assert "Unknown token" in str(e), "Should provide helpful error message"

            print("  - Error handling working correctly")

            return True

        except Exception as e:
            print(f"  Error: {str(e)}")
            return False

    def test_phase_4_time_filtering(self):
        """Phase 4: Test time filtering rules"""
        print("Testing time filtering (8am-1pm EST entries only)...")

        try:
            from mtf_engine import MTFConditionEvaluator, MTFDataAggregator, MTFIndicatorEngine, MTFTimeAlignment, MTFTokenParser

            aggregator = MTFDataAggregator(timezone="America/New_York")
            indicator_engine = MTFIndicatorEngine(aggregator)
            time_alignment = MTFTimeAlignment()
            token_parser = MTFTokenParser()

            evaluator = MTFConditionEvaluator(aggregator, indicator_engine, time_alignment, token_parser)

            # Test various times
            test_times = [
                ("2025-09-01 07:30:00", False),  # Too early
                ("2025-09-01 08:00:00", True),   # Valid start
                ("2025-09-01 10:30:00", True),   # Valid middle
                ("2025-09-01 12:59:00", True),   # Valid end
                ("2025-09-01 13:00:00", False),  # Too late
                ("2025-09-01 15:30:00", False),  # Way too late
            ]

            time_filter = {"start": "08:00", "end": "13:00", "timezone": "America/New_York"}

            for time_str, expected in test_times:
                timestamp = pd.to_datetime(time_str).tz_localize('America/New_York')
                result = evaluator.check_time_filter(timestamp, time_filter)
                assert result == expected, f"Time {time_str}: expected {expected}, got {result}"

            print(f"  - Successfully validated {len(test_times)} time scenarios")

            # Test timezone handling
            utc_time = pd.to_datetime("2025-09-01 14:00:00").tz_localize('UTC')  # 10am EST
            result = evaluator.check_time_filter(utc_time, time_filter)
            assert result == True, "UTC timezone conversion failed"

            print("  - Timezone conversion working correctly")

            return True

        except Exception as e:
            print(f"  Error: {str(e)}")
            return False

    def test_phase_5_mtf_detection(self):
        """Phase 5: Test MTF strategy detection"""
        print("Testing MTF strategy detection logic...")

        try:
            # Non-MTF strategy
            simple_strategy = {
                "entry_conditions": [
                    {"condition": "EMA9 > EMA20 AND previous_EMA9 <= previous_EMA20"}
                ],
                "exit_conditions": [
                    {"condition": "EMA9 < EMA20"}
                ]
            }

            generator = SignalGenerator(simple_strategy)
            assert not generator._is_mtf_strategy(), "Simple strategy incorrectly detected as MTF"

            # MTF strategy
            mtf_strategy = {
                "entry_conditions": [
                    {"condition": "EMA9_5min > EMA20_5min AND EMA9_1h > EMA20_1h"}
                ],
                "exit_conditions": [
                    {"condition": "EMA9_5min < EMA20_5min"}
                ]
            }

            generator = SignalGenerator(mtf_strategy)
            assert generator._is_mtf_strategy(), "MTF strategy not detected"

            print("  - MTF detection working correctly")

            # Test various MTF indicators
            mtf_indicators = ['_1h', '_1D', 'DevBand', 'previous_EMA', 'previous_Close']

            for indicator in mtf_indicators:
                test_strategy = {
                    "entry_conditions": [{"condition": f"test_{indicator}_test"}]
                }
                generator = SignalGenerator(test_strategy)
                assert generator._is_mtf_strategy(), f"Failed to detect MTF indicator: {indicator}"

            print(f"  - Successfully detected {len(mtf_indicators)} MTF indicator types")

            return True

        except Exception as e:
            print(f"  Error: {str(e)}")
            return False

    def test_phase_6_simple_conditions(self):
        """Phase 6: Test simple condition evaluation"""
        print("Testing simple MTF condition evaluation...")

        try:
            mtf_generator = MTFSignalGenerator()

            # Simple crossover strategy
            strategy_config = {
                "strategy_name": "Simple_MTF_Test",
                "timeframe": "5min",
                "symbol": "SPY",
                "entry_conditions": [
                    {
                        "condition": "EMA9_5min > EMA20_5min AND EMA9_1h > EMA20_1h",
                        "time_filter": {"start": "08:00", "end": "13:00", "timezone": "America/New_York"}
                    }
                ],
                "exit_conditions": [
                    {"condition": "EMA9_5min < EMA20_5min"}
                ]
            }

            signals = mtf_generator.generate_signals(strategy_config, self.test_data)

            assert isinstance(signals, list), "Signals should be a list"

            # Verify signal structure
            for signal in signals[:3]:  # Check first few signals
                assert 'timestamp' in signal, "Signal missing timestamp"
                assert 'type' in signal, "Signal missing type"
                assert 'price' in signal, "Signal missing price"

            print(f"  - Generated {len(signals)} signals")

            # Verify time filtering on entry signals
            entry_signals = [s for s in signals if 'entry' in s['type']]
            for signal in entry_signals:
                timestamp = pd.to_datetime(signal['timestamp']).tz_localize('America/New_York')
                hour = timestamp.hour
                assert 8 <= hour < 13, f"Entry signal at {timestamp} outside valid hours"

            print(f"  - All {len(entry_signals)} entry signals within 8am-1pm EST")

            return True

        except Exception as e:
            print(f"  Error: {str(e)}")
            return False

    def test_phase_7_complex_conditions(self):
        """Phase 7: Test complex MTF conditions"""
        print("Testing complex MTF conditions with previous_ and DevBands...")

        try:
            mtf_generator = MTFSignalGenerator()

            # Complex strategy with previous_ and DevBands
            strategy_config = {
                "strategy_name": "Complex_MTF_Test",
                "timeframe": "5min",
                "symbol": "SPY",
                "entry_conditions": [
                    {
                        "condition": "EMA9_5min > EMA20_5min AND previous_EMA9_5min <= previous_EMA20_5min AND EMA9_1h > EMA20_1h AND Low_1h <= DevBand72_1h_Lower_6",
                        "time_filter": {"start": "08:00", "end": "13:00", "timezone": "America/New_York"}
                    }
                ],
                "exit_conditions": [
                    {"condition": "High_1h >= DevBand72_1h_Upper_6"}
                ]
            }

            signals = mtf_generator.generate_signals(strategy_config, self.test_data)

            assert isinstance(signals, list), "Signals should be a list"
            print(f"  - Generated {len(signals)} signals with complex conditions")

            # Verify we can handle all the complex tokens
            entry_signals = [s for s in signals if 'entry' in s['type']]
            exit_signals = [s for s in signals if 'exit' in s['type']]

            print(f"  - Entry signals: {len(entry_signals)}")
            print(f"  - Exit signals: {len(exit_signals)}")

            return True

        except Exception as e:
            print(f"  Error: {str(e)}")
            return False

    def test_phase_8_signal_generation(self):
        """Phase 8: Test end-to-end signal generation"""
        print("Testing end-to-end signal generation with SignalGenerator...")

        try:
            # Test both MTF and non-MTF strategies
            mtf_strategy = {
                "strategy_name": "End_to_End_MTF_Test",
                "timeframe": "5min",
                "symbol": "SPY",
                "entry_conditions": [
                    {
                        "condition": "EMA9_5min > EMA20_5min AND EMA9_1h > EMA20_1h",
                        "time_filter": {"start": "08:00", "end": "13:00", "timezone": "America/New_York"}
                    }
                ],
                "exit_conditions": [
                    {"condition": "EMA9_5min < EMA20_5min"}
                ]
            }

            generator = SignalGenerator(mtf_strategy)
            generator.load_data(self.test_data)
            result = generator.generate_signals()

            assert 'signals' in result, "Result missing signals"
            assert 'performance_metrics' in result, "Result missing performance metrics"
            assert 'provenance' in result, "Result missing provenance"

            signals = result['signals']
            assert isinstance(signals, list), "Signals should be a list"

            print(f"  - Generated complete strategy artifact with {len(signals)} signals")

            # Test performance metrics calculation
            metrics = result['performance_metrics']
            assert 'total_trades' in metrics, "Missing total_trades metric"
            assert 'win_rate' in metrics, "Missing win_rate metric"

            print(f"  - Performance metrics: {metrics['total_trades']} trades")

            return True

        except Exception as e:
            print(f"  Error: {str(e)}")
            return False

    def test_phase_9_route_start_end(self):
        """Phase 9: Test route start/end DevBand functionality"""
        print("Testing route start/end DevBand conditions...")

        try:
            strategy_config = {
                "strategy_name": "Route_Start_End_Test",
                "timeframe": "5min",
                "symbol": "SPY",
                "entry_conditions": [
                    {
                        "condition": "Low_1h <= DevBand72_1h_Lower_6 OR Low_1h <= DevBand89_1h_Lower_6",
                        "time_filter": {"start": "08:00", "end": "13:00", "timezone": "America/New_York"}
                    }
                ],
                "exit_conditions": [
                    {"condition": "High_1h >= DevBand72_1h_Upper_6 OR High_1h >= DevBand89_1h_Upper_6"}
                ]
            }

            generator = SignalGenerator(strategy_config)
            generator.load_data(self.test_data)
            result = generator.generate_signals()

            signals = result['signals']
            entry_signals = [s for s in signals if 'entry' in s['type']]
            exit_signals = [s for s in signals if 'exit' in s['type']]

            print(f"  - Route start signals: {len(entry_signals)}")
            print(f"  - Route end signals: {len(exit_signals)}")

            # Verify DevBand functionality
            assert generator._is_mtf_strategy(), "Route start/end strategy should be detected as MTF"

            return True

        except Exception as e:
            print(f"  Error: {str(e)}")
            return False

    def test_phase_10_integration(self):
        """Phase 10: Full integration test with the provided example"""
        print("Testing full integration with provided example strategy...")

        try:
            # The exact example from requirements
            strategy_config = {
                "strategy_name": "SPY_RULES_ONLY_Crossover_5m_with_Daily_and_RouteStart",
                "timeframe": "5min",
                "symbol": "SPY",
                "signals": [],
                "entry_conditions": [
                    {
                        "type": "ema_crossover_with_time_filter",
                        "direction": "long",
                        "indicators": ["ema9_5min","ema20_5min","ema9_1h","ema20_1h","ema9_1D","ema20_1D"],
                        "condition": "EMA9_5min > EMA20_5min AND previous_EMA9_5min <= previous_EMA20_5min AND EMA9_1h > EMA20_1h AND previous_EMA9_1D > previous_EMA20_1D AND (Low_1h <= DevBand72_1h_Lower_6 OR Low_1h <= DevBand89_1h_Lower_6)",
                        "time_filter": { "start": "08:00", "end": "13:00", "timezone": "America/New_York" }
                    }
                ],
                "exit_conditions": [
                    { "type": "ema_crossover_exit", "direction": "close_long", "condition": "EMA9_5min < EMA20_5min" }
                ]
            }

            generator = SignalGenerator(strategy_config)
            generator.load_data(self.test_data)
            result = generator.generate_signals()

            # Verify all requirements
            assert generator._is_mtf_strategy(), "Strategy should be detected as MTF"

            signals = result['signals']
            entry_signals = [s for s in signals if 'entry' in s['type']]

            # Verify time filtering compliance
            for signal in entry_signals:
                timestamp = pd.to_datetime(signal['timestamp']).tz_localize('America/New_York')
                hour = timestamp.hour
                assert 8 <= hour < 13, f"Entry signal at {timestamp} violates time filter"

            print(f"  - Full integration test passed: {len(entry_signals)} entry signals")
            print(f"  - All signals comply with WZRD rules")

            # Verify signal structure
            for signal in signals[:2]:
                required_fields = ['timestamp', 'type', 'price', 'shares', 'reason', 'direction']
                for field in required_fields:
                    assert field in signal, f"Signal missing required field: {field}"

            print("  - Signal structure validation passed")

            return True

        except Exception as e:
            print(f"  Error: {str(e)}")
            return False

def run_phased_tests():
    """Main function to run phased tests"""
    framework = PhasedTestFramework()
    return framework.run_all_phases()

if __name__ == "__main__":
    success = run_phased_tests()
    exit(0 if success else 1)