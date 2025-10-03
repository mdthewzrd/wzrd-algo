"""
Multi-TimeFrame (MTF) Engine for WZRD Codifier
Implements reliable multi-timeframe support with EMA + dev-bands + time filters
"""

import pandas as pd
import numpy as np
import pytz
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple, Union
import re
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MTFDataAggregator:
    """Handles multi-timeframe data aggregation with timezone awareness"""

    def __init__(self, timezone: str = "America/New_York"):
        self.timezone = timezone
        self.tz = pytz.timezone(timezone)
        self.data_cache = {}

    def normalize_timeframe(self, timeframe: str) -> str:
        """Normalize timeframe tokens"""
        timeframe = timeframe.lower().strip()

        # Handle aliases
        aliases = {
            '1h': '1H', '1hr': '1H', '1hour': '1H', '60min': '1H', '60m': '1H',
            '1d': '1D', '1day': '1D', 'daily': '1D',
            '5m': '5min', '5min': '5min',
            '15m': '15min', '15min': '15min',
            '1min': '1min', '1m': '1min'
        }

        return aliases.get(timeframe, timeframe)

    def build_mtf_dataframes(self, base_data: pd.DataFrame, symbol: str) -> Dict[str, pd.DataFrame]:
        """Build aligned dataframes for different timeframes"""

        # Ensure base data is timezone aware
        if base_data['date'].dt.tz is None:
            base_data = base_data.copy()
            base_data['date'] = base_data['date'].dt.tz_localize(self.tz)
        else:
            base_data = base_data.copy()
            base_data['date'] = base_data['date'].dt.tz_convert(self.tz)

        # Set date as index for resampling
        base_data_indexed = base_data.set_index('date')

        # Create different timeframes
        dataframes = {
            '5min': self._ensure_5min_data(base_data_indexed),
            '1H': self._resample_to_hourly(base_data_indexed),
            '1D': self._resample_to_daily(base_data_indexed)
        }

        # Cache the dataframes
        self.data_cache[symbol] = dataframes

        return dataframes

    def _ensure_5min_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """Ensure we have 5min data, resample if needed"""
        if data.index.to_series().diff().median() <= pd.Timedelta('5min'):
            # Data is 5min or finer, resample to exactly 5min
            return data.resample('5min').agg({
                'open': 'first',
                'high': 'max',
                'low': 'min',
                'close': 'last',
                'volume': 'sum'
            }).dropna()
        else:
            # Data is coarser than 5min, keep as is
            return data

    def _resample_to_hourly(self, data: pd.DataFrame) -> pd.DataFrame:
        """Resample to hourly data with RTH handling"""
        hourly = data.resample('1H').agg({
            'open': 'first',
            'high': 'max',
            'low': 'min',
            'close': 'last',
            'volume': 'sum'
        }).dropna()

        return hourly

    def _resample_to_daily(self, data: pd.DataFrame) -> pd.DataFrame:
        """Resample to daily data (RTH only: 9:30-16:00)"""
        # Filter for RTH hours (9:30 AM to 4:00 PM)
        rth_data = data.between_time('09:30', '16:00')

        daily = rth_data.resample('1D').agg({
            'open': 'first',
            'high': 'max',
            'low': 'min',
            'close': 'last',
            'volume': 'sum'
        }).dropna()

        return daily

    def get_series(self, symbol: str, timeframe: str, field: str) -> pd.Series:
        """Get a specific data series for a symbol/timeframe/field"""
        normalized_tf = self.normalize_timeframe(timeframe)

        if symbol not in self.data_cache:
            raise ValueError(f"No data cached for symbol {symbol}")

        if normalized_tf not in self.data_cache[symbol]:
            raise ValueError(f"Timeframe {normalized_tf} not available for {symbol}")

        field_lower = field.lower()
        if field_lower not in ['open', 'high', 'low', 'close', 'volume']:
            raise ValueError(f"Invalid field {field}. Must be one of: Open, High, Low, Close, Volume")

        return self.data_cache[symbol][normalized_tf][field_lower]

class MTFIndicatorEngine:
    """Calculate indicators across multiple timeframes"""

    def __init__(self, data_aggregator: MTFDataAggregator):
        self.data_aggregator = data_aggregator
        self.indicator_cache = {}

    def calculate_ema(self, symbol: str, timeframe: str, period: int) -> pd.Series:
        """Calculate EMA for a specific timeframe"""
        cache_key = f"{symbol}_{timeframe}_EMA{period}"

        if cache_key not in self.indicator_cache:
            close_series = self.data_aggregator.get_series(symbol, timeframe, 'close')
            ema = close_series.ewm(span=period, adjust=False).mean()
            self.indicator_cache[cache_key] = ema

        return self.indicator_cache[cache_key]

    def calculate_deviation_bands(self, symbol: str, timeframe: str, period: int, multiplier: float) -> Tuple[pd.Series, pd.Series, pd.Series]:
        """Calculate EMA deviation bands"""
        cache_key = f"{symbol}_{timeframe}_DevBand{period}_{multiplier}"

        if cache_key not in self.indicator_cache:
            close_series = self.data_aggregator.get_series(symbol, timeframe, 'close')
            center = self.calculate_ema(symbol, timeframe, period)

            # Use rolling standard deviation with minimum periods
            # Set min_periods to allow calculation with fewer periods if needed
            min_periods = min(period, max(1, len(close_series) // 4))
            deviation = close_series.rolling(window=period, min_periods=min_periods).std()

            # Handle cases where deviation is still NaN or zero
            # Use a small fallback deviation based on price level
            fallback_deviation = center * 0.001  # 0.1% of center price
            deviation = deviation.fillna(fallback_deviation)

            # Replace zeros with fallback using where
            deviation = deviation.where(deviation != 0, fallback_deviation)

            upper = center + (multiplier * deviation)
            lower = center - (multiplier * deviation)

            self.indicator_cache[cache_key] = (center, upper, lower)

        return self.indicator_cache[cache_key]

    def get_previous_value(self, series: pd.Series, timestamp: pd.Timestamp, timeframe: str) -> float:
        """Get previous value in the indicator's timeframe"""
        try:
            # Get the index position of the timestamp
            if timestamp in series.index:
                pos = series.index.get_loc(timestamp)
                if pos > 0:
                    return series.iloc[pos - 1]
            else:
                # Find the closest timestamp before this one
                before_mask = series.index < timestamp
                if before_mask.any():
                    last_idx = series.index[before_mask][-1]
                    pos = series.index.get_loc(last_idx)
                    if pos > 0:
                        return series.iloc[pos - 1]

            return np.nan
        except (IndexError, KeyError):
            return np.nan

class MTFTimeAlignment:
    """Handle time alignment using as-of joins"""

    def __init__(self, base_timeframe: str = '5min'):
        self.base_timeframe = base_timeframe

    def asof_join(self, base_index: pd.DatetimeIndex, higher_tf_series: pd.Series) -> pd.Series:
        """Perform as-of join to align higher timeframe data to base timeframe"""
        # Create a DataFrame with the base index
        result_df = pd.DataFrame(index=base_index)

        # Perform as-of merge (forward fill)
        aligned = higher_tf_series.reindex(base_index, method='ffill')

        return aligned

    def align_all_indicators(self, base_data: pd.DataFrame, mtf_indicators: Dict[str, pd.Series]) -> pd.DataFrame:
        """Align all MTF indicators to base timeframe"""
        base_index = base_data.index if isinstance(base_data.index, pd.DatetimeIndex) else base_data['date']

        aligned_data = base_data.copy()

        for indicator_name, series in mtf_indicators.items():
            aligned_data[indicator_name] = self.asof_join(base_index, series)

        return aligned_data

class MTFTokenParser:
    """Parse and normalize MTF indicator tokens"""

    def __init__(self):
        self.token_patterns = {
            'ema': r'(?:previous_)?EMA(\d+)_(\w+)',
            'devband': r'DevBand(\d+)_(\w+)_(Upper|Lower)_(\d+)',
            'price': r'(?:previous_)?(Open|High|Low|Close)_(\w+)',
            'volume': r'(?:previous_)?Volume_(\w+)'
        }

    def parse_token(self, token: str) -> Dict[str, Any]:
        """Parse a token and return its components"""
        token = token.strip()

        # Check for previous_ prefix
        is_previous = token.startswith('previous_')
        if is_previous:
            token = token[9:]  # Remove 'previous_' prefix

        # Try to match each pattern
        for pattern_name, pattern in self.token_patterns.items():
            match = re.match(pattern, token, re.IGNORECASE)
            if match:
                if pattern_name == 'ema':
                    return {
                        'type': 'ema',
                        'period': int(match.group(1)),
                        'timeframe': match.group(2),
                        'is_previous': is_previous
                    }
                elif pattern_name == 'devband':
                    return {
                        'type': 'devband',
                        'period': int(match.group(1)),
                        'timeframe': match.group(2),
                        'band_type': match.group(3).lower(),
                        'multiplier': int(match.group(4)),
                        'is_previous': is_previous
                    }
                elif pattern_name == 'price':
                    return {
                        'type': 'price',
                        'field': match.group(1).lower(),
                        'timeframe': match.group(2),
                        'is_previous': is_previous
                    }
                elif pattern_name == 'volume':
                    return {
                        'type': 'volume',
                        'timeframe': match.group(1),
                        'is_previous': is_previous
                    }

        # If no pattern matches, raise an error with suggestions
        suggestions = self._get_suggestions(token)
        raise ValueError(f"Unknown token '{token}'. Did you mean: {', '.join(suggestions)}")

    def _get_suggestions(self, token: str) -> List[str]:
        """Provide suggestions for unknown tokens"""
        suggestions = []
        token_lower = token.lower()

        if 'ema' in token_lower:
            if '60min' in token_lower:
                suggestions.append(token.replace('60min', '1h'))
            suggestions.extend(['EMA9_5min', 'EMA20_1h', 'EMA9_1D'])

        if 'devband' in token_lower:
            suggestions.extend(['DevBand72_1h_Lower_6', 'DevBand89_1h_Upper_6'])

        return suggestions[:3]  # Return top 3 suggestions

class MTFConditionEvaluator:
    """Evaluate MTF conditions with proper time filtering"""

    def __init__(self, data_aggregator: MTFDataAggregator, indicator_engine: MTFIndicatorEngine,
                 time_alignment: MTFTimeAlignment, token_parser: MTFTokenParser):
        self.data_aggregator = data_aggregator
        self.indicator_engine = indicator_engine
        self.time_alignment = time_alignment
        self.token_parser = token_parser
        self.timezone = data_aggregator.timezone

    def evaluate_condition(self, condition_str: str, symbol: str, timestamp: pd.Timestamp) -> bool:
        """Evaluate a condition string at a specific timestamp"""
        try:
            # Parse tokens in the condition
            tokens = self._extract_tokens(condition_str)

            # Resolve token values
            token_values = {}
            for token in tokens:
                try:
                    parsed = self.token_parser.parse_token(token)
                    value = self._resolve_token_value(parsed, symbol, timestamp)
                    token_values[token] = value

                    # Log first 10 evaluations for debugging
                    if len(token_values) <= 10:
                        logger.info(f"Token {token} = {value} at {timestamp}")

                except Exception as e:
                    logger.warning(f"Failed to resolve token {token}: {e}")
                    return False

            # Replace tokens in condition string with values
            evaluated_condition = condition_str
            for token, value in token_values.items():
                if pd.isna(value):
                    return False  # Fail if any value is NaN
                evaluated_condition = evaluated_condition.replace(token, str(value))

            # Evaluate the boolean expression
            return self._safe_eval(evaluated_condition)

        except Exception as e:
            logger.error(f"Error evaluating condition '{condition_str}': {e}")
            return False

    def _extract_tokens(self, condition_str: str) -> List[str]:
        """Extract all tokens from a condition string"""
        # Pattern to match our token formats
        patterns = [
            r'\bprevious_EMA\d+_\w+\b',
            r'\bEMA\d+_\w+\b',
            r'\bDevBand\d+_\w+_(?:Upper|Lower)_\d+\b',
            r'\bprevious_(?:Open|High|Low|Close)_\w+\b',
            r'\b(?:Open|High|Low|Close)_\w+\b',
            r'\bprevious_Volume_\w+\b',
            r'\bVolume_\w+\b'
        ]

        tokens = []
        for pattern in patterns:
            matches = re.findall(pattern, condition_str, re.IGNORECASE)
            tokens.extend(matches)

        return list(set(tokens))  # Remove duplicates

    def _resolve_token_value(self, parsed_token: Dict[str, Any], symbol: str, timestamp: pd.Timestamp) -> float:
        """Resolve a parsed token to its numeric value"""
        token_type = parsed_token['type']
        timeframe = self.data_aggregator.normalize_timeframe(parsed_token['timeframe'])
        is_previous = parsed_token.get('is_previous', False)

        if token_type == 'ema':
            period = parsed_token['period']
            series = self.indicator_engine.calculate_ema(symbol, timeframe, period)

            if is_previous:
                return self.indicator_engine.get_previous_value(series, timestamp, timeframe)
            else:
                # Get current value using as-of logic
                return self._get_asof_value(series, timestamp)

        elif token_type == 'devband':
            period = parsed_token['period']
            multiplier = parsed_token['multiplier']
            band_type = parsed_token['band_type']

            center, upper, lower = self.indicator_engine.calculate_deviation_bands(
                symbol, timeframe, period, multiplier
            )

            target_series = upper if band_type == 'upper' else lower

            if is_previous:
                return self.indicator_engine.get_previous_value(target_series, timestamp, timeframe)
            else:
                return self._get_asof_value(target_series, timestamp)

        elif token_type in ['price', 'volume']:
            field = parsed_token.get('field', 'volume')
            series = self.data_aggregator.get_series(symbol, timeframe, field)

            if is_previous:
                return self.indicator_engine.get_previous_value(series, timestamp, timeframe)
            else:
                return self._get_asof_value(series, timestamp)

        return np.nan

    def _get_asof_value(self, series: pd.Series, timestamp: pd.Timestamp) -> float:
        """Get as-of value from series at timestamp"""
        try:
            if timestamp in series.index:
                return series.loc[timestamp]
            else:
                # Find the last known value before this timestamp
                before_mask = series.index <= timestamp
                if before_mask.any():
                    last_idx = series.index[before_mask][-1]
                    return series.loc[last_idx]
                return np.nan
        except (IndexError, KeyError):
            return np.nan

    def _safe_eval(self, expression: str) -> bool:
        """Safely evaluate a boolean expression"""
        try:
            # Replace logical operators
            expression = expression.replace(' AND ', ' and ')
            expression = expression.replace(' OR ', ' or ')
            expression = expression.replace(' NOT ', ' not ')

            # Only allow specific operators and functions
            allowed_names = {
                "__builtins__": {},
                "True": True,
                "False": False,
                "and": lambda x, y: x and y,
                "or": lambda x, y: x or y,
                "not": lambda x: not x
            }

            return eval(expression, allowed_names)
        except:
            return False

    def check_time_filter(self, timestamp: pd.Timestamp, time_filter: Dict[str, Any]) -> bool:
        """Check if timestamp passes time filter (8am-1pm EST for entries)"""
        try:
            start_time = time_filter.get('start', '08:00')
            end_time = time_filter.get('end', '13:00')
            timezone = time_filter.get('timezone', 'America/New_York')

            # Convert to specified timezone
            if timestamp.tz is None:
                local_time = timestamp.tz_localize(pytz.timezone(timezone))
            else:
                local_time = timestamp.tz_convert(pytz.timezone(timezone))

            # Extract hour and minute
            hour = local_time.hour
            minute = local_time.minute

            # Parse start and end times
            start_hour, start_minute = map(int, start_time.split(':'))
            end_hour, end_minute = map(int, end_time.split(':'))

            # Convert to minutes for easier comparison
            current_minutes = hour * 60 + minute
            start_minutes = start_hour * 60 + start_minute
            end_minutes = end_hour * 60 + end_minute

            return start_minutes <= current_minutes < end_minutes

        except Exception as e:
            logger.error(f"Error checking time filter: {e}")
            return False

class MTFSignalGenerator:
    """Main MTF signal generator"""

    def __init__(self, timezone: str = "America/New_York"):
        self.data_aggregator = MTFDataAggregator(timezone)
        self.indicator_engine = MTFIndicatorEngine(self.data_aggregator)
        self.time_alignment = MTFTimeAlignment()
        self.token_parser = MTFTokenParser()
        self.condition_evaluator = MTFConditionEvaluator(
            self.data_aggregator, self.indicator_engine,
            self.time_alignment, self.token_parser
        )

    def generate_signals(self, strategy_config: Dict[str, Any], base_data: pd.DataFrame) -> List[Dict[str, Any]]:
        """Generate signals using MTF analysis"""
        symbol = strategy_config.get('symbol', 'UNKNOWN')

        # Build MTF dataframes
        self.data_aggregator.build_mtf_dataframes(base_data, symbol)

        # Get base 5min data for iteration
        base_5min = self.data_aggregator.data_cache[symbol]['5min'].reset_index()

        signals = []

        # Process entry conditions
        entry_conditions = strategy_config.get('entry_conditions', [])
        exit_conditions = strategy_config.get('exit_conditions', [])

        for i, row in base_5min.iterrows():
            timestamp = row['date']

            # Check entry conditions
            for entry_condition in entry_conditions:
                condition_str = entry_condition.get('condition', '')
                time_filter = entry_condition.get('time_filter', {})
                direction = entry_condition.get('direction', 'long')

                # Check time filter for entries
                if not self.condition_evaluator.check_time_filter(timestamp, time_filter):
                    continue

                # Check if 1h EMA direction confirmation is required
                if not self._check_1h_ema_confirmation(symbol, timestamp, direction):
                    continue

                # Evaluate condition
                if self.condition_evaluator.evaluate_condition(condition_str, symbol, timestamp):
                    signals.append({
                        'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                        'type': f'entry_signal',
                        'price': row['close'],
                        'shares': 100,  # Default shares
                        'reason': f"MTF condition met: {condition_str[:50]}...",
                        'direction': direction
                    })

            # Check exit conditions (no time restrictions)
            for exit_condition in exit_conditions:
                condition_str = exit_condition.get('condition', '')
                direction = exit_condition.get('direction', 'close_long')

                if self.condition_evaluator.evaluate_condition(condition_str, symbol, timestamp):
                    signals.append({
                        'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                        'type': 'exit_signal',
                        'price': row['close'],
                        'shares': 100,
                        'reason': f"MTF exit condition met: {condition_str[:50]}...",
                        'direction': direction,
                        'pnl': 500.0  # Default P&L for demo
                    })

        return signals

    def _check_1h_ema_confirmation(self, symbol: str, timestamp: pd.Timestamp, direction: str) -> bool:
        """Check mandatory 1h EMA direction confirmation"""
        try:
            ema9_1h = self.indicator_engine.calculate_ema(symbol, '1H', 9)
            ema20_1h = self.indicator_engine.calculate_ema(symbol, '1H', 20)

            ema9_value = self.condition_evaluator._get_asof_value(ema9_1h, timestamp)
            ema20_value = self.condition_evaluator._get_asof_value(ema20_1h, timestamp)

            if pd.isna(ema9_value) or pd.isna(ema20_value):
                return False

            if direction == 'long':
                return ema9_value > ema20_value
            elif direction == 'short':
                return ema9_value < ema20_value

            return True
        except Exception as e:
            logger.error(f"Error checking 1h EMA confirmation: {e}")
            return False

# Example usage function for testing
def test_mtf_engine():
    """Test the MTF engine with sample data"""
    # Create sample 5min data
    dates = pd.date_range('2025-09-01 09:30:00', '2025-09-01 16:00:00', freq='5min', tz='America/New_York')
    sample_data = pd.DataFrame({
        'date': dates,
        'open': np.random.uniform(450, 460, len(dates)),
        'high': np.random.uniform(455, 465, len(dates)),
        'low': np.random.uniform(445, 455, len(dates)),
        'close': np.random.uniform(450, 460, len(dates)),
        'volume': np.random.randint(100000, 1000000, len(dates))
    })

    # Create sample strategy
    strategy_config = {
        "strategy_name": "SPY_MTF_Test",
        "timeframe": "5min",
        "symbol": "SPY",
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

    # Test MTF signal generation
    mtf_generator = MTFSignalGenerator()
    signals = mtf_generator.generate_signals(strategy_config, sample_data)

    print(f"Generated {len(signals)} signals")
    for signal in signals[:5]:  # Show first 5 signals
        print(f"  {signal['timestamp']}: {signal['type']} @ ${signal['price']:.2f}")

    return signals

if __name__ == "__main__":
    test_mtf_engine()