#!/usr/bin/env python3
"""
SPY Multi-Timeframe EMA Strategy Implementation

Strategy Overview:
- Regime Filter: Daily 9 EMA > 20 EMA (bullish longs only)
- Setup: 4-hour price dips to 9-period EMA lower deviation band (1.5 std)
- Entry: Hourly break of previous bar highs
- Exit 1: 72/89 upper deviation band (primary target)
- Exit 2: Daily 9/20 EMA cross (regime change)
- Exit 3: Hourly pivot/swing breaks
- Risk Management: Daily trailing stop to protect gains

Author: WZRD AI Trading System
Date: 2025-01-29
"""

import numpy as np
import pandas as pd
import requests
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from datetime import datetime, timedelta
import logging
import warnings
warnings.filterwarnings('ignore')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class SPYMultiTimeframeConfig:
    """Configuration for SPY Multi-Timeframe Strategy."""

    # EMA Periods
    fast_ema_period: int = 9
    slow_ema_period: int = 20
    target_fast_ema: int = 72
    target_slow_ema: int = 89
    deviation_ema_period: int = 9

    # Deviation Bands
    deviation_std: float = 1.5

    # Risk Management
    atr_period: int = 14
    risk_per_trade: float = 0.01  # 1% of account
    max_portfolio_heat: float = 0.20  # 20% of account
    trail_atr_multiple: float = 2.0  # ATR multiple for trailing stop

    # Timeframes (in minutes)
    daily_tf: int = 1440
    four_hour_tf: int = 240
    hourly_tf: int = 60

    # Polygon API
    polygon_api_key: Optional[str] = None

    # Strategy Parameters
    min_profit_target: float = 0.02  # 2% minimum profit target
    max_hold_days: int = 10  # Maximum holding period

class SPYMultiTimeframeStrategy:
    """
    SPY Multi-Timeframe EMA Strategy Implementation

    This strategy combines multiple timeframes for high-probability SPY trading:
    - Daily chart for regime identification
    - 4-hour chart for setup identification
    - Hourly chart for entry execution and exit management
    """

    def __init__(self, config: SPYMultiTimeframeConfig = None):
        self.config = config or SPYMultiTimeframeConfig()
        self.positions = {}
        self.account_size = 100_000
        self.daily_equity = []
        self.trailing_stops = {}

    def calculate_ema(self, data: pd.Series, period: int) -> pd.Series:
        """Calculate Exponential Moving Average."""
        return data.ewm(span=period, adjust=False).mean()

    def calculate_atr(self, data: pd.DataFrame, period: int = 14) -> pd.Series:
        """Calculate Average True Range."""
        high = data['high']
        low = data['low']
        close = data['close'].shift(1)

        tr1 = high - low
        tr2 = np.abs(high - close)
        tr3 = np.abs(low - close)

        true_range = np.maximum(tr1, np.maximum(tr2, tr3))
        return true_range.rolling(window=period).mean()

    def calculate_deviation_bands(self, data: pd.Series, ema_period: int, std_dev: float = 1.5) -> Tuple[pd.Series, pd.Series]:
        """Calculate upper and lower deviation bands around EMA."""
        ema = self.calculate_ema(data, ema_period)
        rolling_std = data.rolling(window=ema_period).std()

        upper_band = ema + (rolling_std * std_dev)
        lower_band = ema - (rolling_std * std_dev)

        return upper_band, lower_band

    def get_polygon_data(self, symbol: str = "SPY", timespan: str = "day",
                         from_date: str = None, to_date: str = None,
                         multiplier: int = 1) -> pd.DataFrame:
        """
        Fetch market data from Polygon API.

        Args:
            symbol: Stock symbol (default: SPY)
            timespan: Time span (day, hour, minute)
            from_date: Start date (YYYY-MM-DD)
            to_date: End date (YYYY-MM-DD)
            multiplier: Multiplier for timespan

        Returns:
            DataFrame with OHLCV data
        """
        if not self.config.polygon_api_key:
            logger.warning("No Polygon API key provided, using simulated data")
            return self._generate_simulated_data(symbol, timespan, from_date, to_date)

        # Set default dates
        if not to_date:
            to_date = datetime.now().strftime('%Y-%m-%d')
        if not from_date:
            from_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')

        base_url = "https://api.polygon.io/v2/aggs/ticker"
        url = f"{base_url}/{symbol}/range/{multiplier}/{timespan}/{from_date}/{to_date}"

        params = {
            "apikey": self.config.polygon_api_key,
            "adjusted": "true",
            "sort": "asc"
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()

            data = response.json()

            if 'results' not in data:
                logger.error(f"No results in Polygon response: {data}")
                return self._generate_simulated_data(symbol, timespan, from_date, to_date)

            # Convert to DataFrame
            df = pd.DataFrame(data['results'])
            df['timestamp'] = pd.to_datetime(df['t'], unit='ms')
            df.set_index('timestamp', inplace=True)

            # Rename columns to standard format
            df = df.rename(columns={
                'o': 'open',
                'h': 'high',
                'l': 'low',
                'c': 'close',
                'v': 'volume'
            })

            # Select relevant columns
            df = df[['open', 'high', 'low', 'close', 'volume']]

            logger.info(f"Successfully fetched {len(df)} bars of {timespan} data for {symbol}")
            return df

        except Exception as e:
            logger.error(f"Error fetching Polygon data: {e}")
            return self._generate_simulated_data(symbol, timespan, from_date, to_date)

    def _generate_simulated_data(self, symbol: str, timespan: str,
                                 from_date: str, to_date: str) -> pd.DataFrame:
        """Generate realistic simulated data for testing."""

        # Parse dates
        start_date = pd.to_datetime(from_date)
        end_date = pd.to_datetime(to_date)

        # Generate date range based on timespan
        if timespan == "day":
            dates = pd.date_range(start=start_date, end=end_date, freq='D')
            dates = dates[dates.dayofweek < 5]  # Weekdays only
        elif timespan == "hour":
            dates = pd.date_range(start=start_date, end=end_date, freq='H')
            # Market hours: 9:30 AM to 4:00 PM
            dates = dates[(dates.hour >= 9) & (dates.hour < 16) & (dates.dayofweek < 5)]
        else:
            dates = pd.date_range(start=start_date, end=end_date, freq='4H')
            dates = dates[(dates.hour >= 9) & (dates.hour < 16) & (dates.dayofweek < 5)]

        if len(dates) == 0:
            return pd.DataFrame()

        # Generate realistic price movements
        np.random.seed(42)

        # SPY-like starting price
        base_price = 450.0

        # Generate returns with some trend and volatility
        n_periods = len(dates)

        if timespan == "day":
            # Daily data: lower volatility, slight upward trend
            daily_returns = np.random.normal(0.0005, 0.015, n_periods)
        elif timespan == "hour":
            # Hourly data: higher volatility
            daily_returns = np.random.normal(0.0001, 0.008, n_periods)
        else:
            # 4-hour data: medium volatility
            daily_returns = np.random.normal(0.0002, 0.012, n_periods)

        # Generate price series
        prices = [base_price]
        for ret in daily_returns:
            new_price = prices[-1] * (1 + ret)
            prices.append(max(new_price, 1))  # Prevent negative prices

        prices = prices[1:]  # Remove starting price

        # Create OHLCV data
        data = pd.DataFrame({
            'open': prices,
            'high': [p * (1 + abs(np.random.normal(0, 0.005))) for p in prices],
            'low': [p * (1 - abs(np.random.normal(0, 0.005))) for p in prices],
            'close': prices,
            'volume': np.random.randint(1_000_000, 10_000_000, len(prices))
        }, index=dates)

        logger.info(f"Generated {len(data)} bars of simulated {timespan} data for {symbol}")
        return data

    def analyze_regime(self, daily_data: pd.DataFrame) -> str:
        """
        Analyze market regime using daily 9/20 EMA.

        Returns:
            'bullish' if 9 EMA > 20 EMA, 'bearish' otherwise
        """
        if len(daily_data) < max(self.config.fast_ema_period, self.config.slow_ema_period):
            return 'insufficient_data'

        # Calculate EMAs
        ema_9 = self.calculate_ema(daily_data['close'], self.config.fast_ema_period)
        ema_20 = self.calculate_ema(daily_data['close'], self.config.slow_ema_period)

        current_ema_9 = ema_9.iloc[-1]
        current_ema_20 = ema_20.iloc[-1]

        return 'bullish' if current_ema_9 > current_ema_20 else 'bearish'

    def identify_setup(self, four_hour_data: pd.DataFrame) -> bool:
        """
        Identify setup on 4-hour timeframe.

        Setup: Price dips to or below 9-period EMA lower deviation band

        Returns:
            True if setup condition is met
        """
        if len(four_hour_data) < self.config.deviation_ema_period:
            return False

        # Calculate deviation bands
        upper_band, lower_band = self.calculate_deviation_bands(
            four_hour_data['close'],
            self.config.deviation_ema_period,
            self.config.deviation_std
        )

        # Check if current price is at or below lower deviation band
        current_price = four_hour_data['close'].iloc[-1]
        current_lower_band = lower_band.iloc[-1]

        # Setup condition: price touches or goes below lower deviation band
        return current_price <= current_lower_band

    def generate_entry_signal(self, hourly_data: pd.DataFrame) -> bool:
        """
        Generate entry signal on hourly timeframe.

        Entry: Break of previous hourly bar high

        Returns:
            True if entry condition is met
        """
        if len(hourly_data) < 2:
            return False

        # Current and previous bar
        current_bar = hourly_data.iloc[-1]
        previous_bar = hourly_data.iloc[-2]

        # Entry condition: current bar breaks previous bar high
        return current_bar['high'] > previous_bar['high']

    def check_exit_conditions(self, daily_data: pd.DataFrame, hourly_data: pd.DataFrame,
                             entry_price: float, entry_time: pd.Timestamp) -> Dict[str, bool]:
        """
        Check all exit conditions.

        Returns:
            Dictionary with exit condition statuses
        """
        exits = {
            'exit_1_target_reached': False,  # 72/89 upper deviation band
            'exit_2_regime_change': False,   # Daily 9/20 cross
            'exit_3_pivot_break': False,     # Hourly pivot/swing break
            'exit_trailing_stop': False,     # Daily trailing stop
            'exit_max_hold_time': False      # Maximum holding period
        }

        # Exit 1: 72/89 upper deviation band target
        if len(daily_data) >= max(self.config.target_fast_ema, self.config.target_slow_ema):
            upper_band, _ = self.calculate_deviation_bands(
                daily_data['close'],
                self.config.target_fast_ema,
                self.config.deviation_std
            )
            current_price = daily_data['close'].iloc[-1]
            current_upper_band = upper_band.iloc[-1]

            if current_price >= current_upper_band:
                exits['exit_1_target_reached'] = True

        # Exit 2: Daily regime change (9/20 EMA cross)
        regime = self.analyze_regime(daily_data)
        if regime == 'bearish':
            exits['exit_2_regime_change'] = True

        # Exit 3: Hourly pivot break
        if len(hourly_data) >= 2:
            # Simple pivot detection: close below previous bar low
            current_close = hourly_data['close'].iloc[-1]
            previous_low = hourly_data['low'].iloc[-2]

            if current_close < previous_low:
                exits['exit_3_pivot_break'] = True

        # Exit 4: Trailing stop
        position_id = f"{entry_time.strftime('%Y%m%d_%H%M')}"
        if position_id in self.trailing_stops:
            current_price = hourly_data['close'].iloc[-1]
            trailing_stop = self.trailing_stops[position_id]

            if current_price <= trailing_stop:
                exits['exit_trailing_stop'] = True

        # Exit 5: Maximum holding period
        hold_time = pd.Timestamp.now() - entry_time
        if hold_time.days > self.config.max_hold_days:
            exits['exit_max_hold_time'] = True

        return exits

    def update_trailing_stop(self, daily_data: pd.DataFrame, entry_price: float,
                            entry_time: pd.Timestamp, is_long: bool = True):
        """Update daily trailing stop."""

        if len(daily_data) < self.config.atr_period:
            return

        position_id = f"{entry_time.strftime('%Y%m%d_%H%M')}"

        # Calculate current ATR
        atr = self.calculate_atr(daily_data, self.config.atr_period).iloc[-1]
        current_price = daily_data['close'].iloc[-1]

        # Calculate trailing stop distance
        trail_distance = atr * self.config.trail_atr_multiple

        if is_long:
            # For long positions: stop moves up but not down
            new_trailing_stop = current_price - trail_distance

            if position_id not in self.trailing_stops:
                # Initialize trailing stop
                self.trailing_stops[position_id] = new_trailing_stop
            else:
                # Only move stop up (protect profits)
                current_stop = self.trailing_stops[position_id]
                if new_trailing_stop > current_stop:
                    self.trailing_stops[position_id] = new_trailing_stop
        else:
            # For short positions: stop moves down but not up
            new_trailing_stop = current_price + trail_distance

            if position_id not in self.trailing_stops:
                self.trailing_stops[position_id] = new_trailing_stop
            else:
                # Only move stop down (protect profits)
                current_stop = self.trailing_stops[position_id]
                if new_trailing_stop < current_stop:
                    self.trailing_stops[position_id] = new_trailing_stop

    def calculate_position_size(self, entry_price: float, stop_loss: float) -> float:
        """Calculate position size based on risk management."""

        risk_per_share = abs(entry_price - stop_loss)
        risk_amount = self.account_size * self.config.risk_per_trade

        position_size = risk_amount / risk_per_share

        # Check against maximum portfolio heat
        max_position_value = self.account_size * self.config.max_portfolio_heat
        position_value = position_size * entry_price

        if position_value > max_position_value:
            position_size = max_position_value / entry_price

        return position_size

    def scan_for_opportunities(self, daily_data: pd.DataFrame,
                              four_hour_data: pd.DataFrame,
                              hourly_data: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        Scan for trading opportunities across all timeframes.

        Returns:
            List of opportunity dictionaries
        """
        opportunities = []

        # Check if we have sufficient data
        if (len(daily_data) < 20 or len(four_hour_data) < 10 or len(hourly_data) < 2):
            logger.warning("Insufficient data for opportunity scanning")
            return opportunities

        # Step 1: Check daily regime
        regime = self.analyze_regime(daily_data)
        if regime != 'bullish':
            logger.info("Not in bullish regime, skipping long setups")
            return opportunities

        # Step 2: Check 4-hour setup
        setup_detected = self.identify_setup(four_hour_data)
        if not setup_detected:
            logger.info("No 4-hour setup detected")
            return opportunities

        # Step 3: Check hourly entry signal
        entry_signal = self.generate_entry_signal(hourly_data)
        if not entry_signal:
            logger.info("No hourly entry signal")
            return opportunities

        # All conditions met - create opportunity
        current_price = hourly_data['close'].iloc[-1]

        # Calculate stop loss (wide stop as described)
        atr = self.calculate_atr(hourly_data, self.config.atr_period).iloc[-1]
        stop_loss = current_price - (atr * 2.0)  # Wide stop - 2x ATR below entry

        # Calculate position size
        position_size = self.calculate_position_size(current_price, stop_loss)

        opportunity = {
            'symbol': 'SPY',
            'regime': regime,
            'setup_type': '4hour_lower_deviation_band',
            'entry_price': current_price,
            'stop_loss': stop_loss,
            'position_size': position_size,
            'timestamp': pd.Timestamp.now(),
            'confidence': 'high',  # All conditions met
            'timeframes': {
                'daily': 'bullish_9_above_20',
                '4hour': 'lower_deviation_band_touch',
                'hourly': 'previous_high_break'
            }
        }

        opportunities.append(opportunity)
        logger.info(f"Trading opportunity identified: {opportunity}")

        return opportunities

    def run_strategy_backtest(self, start_date: str, end_date: str) -> Dict[str, Any]:
        """
        Run complete strategy backtest.

        Args:
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)

        Returns:
            Dictionary with backtest results
        """
        logger.info(f"Starting backtest from {start_date} to {end_date}")

        # Fetch data for all timeframes
        daily_data = self.get_polygon_data("SPY", "day", start_date, end_date)
        four_hour_data = self.get_polygon_data("SPY", "hour", start_date, end_date)
        hourly_data = self.get_polygon_data("SPY", "hour", start_date, end_date)

        # Align data timestamps
        four_hour_data = self._resample_to_4hour(four_hour_data)

        # Initialize tracking variables
        positions = []
        equity_curve = [self.account_size]
        trades = []

        # Run through each day
        unique_days = daily_data.index.normalize().unique()

        for day in unique_days:
            # Get data up to current day
            daily_mask = daily_data.index.normalize() <= day
            current_daily = daily_data[daily_mask]

            hourly_mask = hourly_data.index.normalize() <= day
            current_hourly = hourly_data[hourly_mask]

            four_hour_mask = four_hour_data.index.normalize() <= day
            current_four_hour = four_hour_data[four_hour_mask]

            # Scan for opportunities
            opportunities = self.scan_for_opportunities(
                current_daily, current_four_hour, current_hourly
            )

            # Process opportunities
            for opp in opportunities:
                # Check if we're not already in a position
                active_positions = [p for p in positions if p['exit_time'] is None]

                if len(active_positions) == 0:
                    # Enter new position
                    position = {
                        'entry_time': opp['timestamp'],
                        'entry_price': opp['entry_price'],
                        'stop_loss': opp['stop_loss'],
                        'position_size': opp['position_size'],
                        'exit_time': None,
                        'exit_price': None,
                        'exit_reason': None,
                        'pnl': 0
                    }

                    positions.append(position)
                    logger.info(f"Entered position at {opp['entry_price']:.2f}")

            # Manage existing positions
            for position in positions:
                if position['exit_time'] is None:
                    # Update trailing stop
                    self.update_trailing_stop(
                        current_daily,
                        position['entry_price'],
                        position['entry_time']
                    )

                    # Check exit conditions
                    exits = self.check_exit_conditions(
                        current_daily,
                        current_hourly,
                        position['entry_price'],
                        position['entry_time']
                    )

                    # Exit if any condition is met
                    if any(exits.values()):
                        exit_reason = [k for k, v in exits.items() if v][0]
                        exit_price = current_hourly['close'].iloc[-1]

                        position['exit_time'] = day
                        position['exit_price'] = exit_price
                        position['exit_reason'] = exit_reason
                        position['pnl'] = (exit_price - position['entry_price']) * position['position_size']

                        trades.append(position)
                        logger.info(f"Exited position: {exit_reason} at {exit_price:.2f}")

            # Calculate daily equity
            active_positions = [p for p in positions if p['exit_time'] is None]
            daily_pnl = sum(
                (current_hourly['close'].iloc[-1] - p['entry_price']) * p['position_size']
                for p in active_positions
            )
            realized_pnl = sum(p['pnl'] for p in trades if p['exit_time'] and p['exit_time'].normalize() <= day)

            daily_equity = self.account_size + daily_pnl + realized_pnl
            equity_curve.append(daily_equity)

        # Calculate performance metrics
        backtest_results = self._calculate_performance_metrics(
            trades, equity_curve, self.account_size
        )

        logger.info(f"Backtest completed: {len(trades)} trades")

        return {
            'trades': trades,
            'equity_curve': equity_curve,
            'performance_metrics': backtest_results,
            'data_used': {
                'daily': len(daily_data),
                'four_hour': len(four_hour_data),
                'hourly': len(hourly_data)
            }
        }

    def _resample_to_4hour(self, hourly_data: pd.DataFrame) -> pd.DataFrame:
        """Resample hourly data to 4-hour timeframe."""

        # Group by 4-hour intervals
        resampled = hourly_data.resample('4H').agg({
            'open': 'first',
            'high': 'max',
            'low': 'min',
            'close': 'last',
            'volume': 'sum'
        })

        # Remove rows with NaN values (outside market hours)
        resampled = resampled.dropna()

        return resampled

    def _calculate_performance_metrics(self, trades: List[Dict],
                                    equity_curve: List[float],
                                    initial_capital: float) -> Dict[str, Any]:
        """Calculate comprehensive performance metrics."""

        if not trades:
            return {
                'total_trades': 0,
                'win_rate': 0,
                'profit_factor': 0,
                'sharpe_ratio': 0,
                'max_drawdown': 0,
                'total_return': 0
            }

        # Basic metrics
        winning_trades = [t for t in trades if t['pnl'] > 0]
        losing_trades = [t for t in trades if t['pnl'] <= 0]

        total_trades = len(trades)
        win_rate = len(winning_trades) / total_trades if total_trades > 0 else 0

        # Profit factor
        total_profit = sum(t['pnl'] for t in winning_trades)
        total_loss = abs(sum(t['pnl'] for t in losing_trades))
        profit_factor = total_profit / total_loss if total_loss > 0 else 0

        # Returns and drawdown
        equity_series = pd.Series(equity_curve)
        returns = equity_series.pct_change().dropna()

        total_return = (equity_curve[-1] - initial_capital) / initial_capital

        # Sharpe ratio (annualized)
        sharpe_ratio = (returns.mean() / returns.std()) * np.sqrt(252) if len(returns) > 0 else 0

        # Maximum drawdown
        cumulative_returns = (1 + returns).cumprod()
        running_max = cumulative_returns.expanding().max()
        drawdown = (cumulative_returns - running_max) / running_max
        max_drawdown = drawdown.min()

        return {
            'total_trades': total_trades,
            'win_rate': win_rate,
            'profit_factor': profit_factor,
            'sharpe_ratio': sharpe_ratio,
            'max_drawdown': max_drawdown,
            'total_return': total_return,
            'avg_win': total_profit / len(winning_trades) if winning_trades else 0,
            'avg_loss': total_loss / len(losing_trades) if losing_trades else 0
        }

# Example usage and testing
if __name__ == "__main__":
    # Initialize strategy
    config = SPYMultiTimeframeConfig(
        polygon_api_key=None,  # Set your Polygon API key here
        risk_per_trade=0.01,
        max_portfolio_heat=0.20
    )

    strategy = SPYMultiTimeframeStrategy(config)

    print("🚀 SPY Multi-Timeframe EMA Strategy")
    print("=" * 50)

    # Test with recent data
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d')

    print(f"Testing period: {start_date} to {end_date}")

    # Run backtest
    results = strategy.run_strategy_backtest(start_date, end_date)

    # Display results
    metrics = results['performance_metrics']

    print(f"\n📊 Backtest Results:")
    print(f"Total Trades: {metrics['total_trades']}")
    print(f"Win Rate: {metrics['win_rate']:.1%}")
    print(f"Profit Factor: {metrics['profit_factor']:.2f}")
    print(f"Sharpe Ratio: {metrics['sharpe_ratio']:.2f}")
    print(f"Max Drawdown: {metrics['max_drawdown']:.1%}")
    print(f"Total Return: {metrics['total_return']:.1%}")

    print(f"\n📈 Data Usage:")
    print(f"Daily bars: {results['data_used']['daily']}")
    print(f"4-Hour bars: {results['data_used']['four_hour']}")
    print(f"Hourly bars: {results['data_used']['hourly']}")