#!/usr/bin/env python3
"""
VectorBT Backtesting Suite for SPY Multi-Timeframe Strategy
Provides professional-grade performance analysis
"""

import sys
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent))

from spy_multi_timeframe_strategy import SPYMultiTimeframeStrategy, SPYMultiTimeframeConfig

def run_vectorbt_backtest():
    """Run comprehensive VectorBT backtesting for SPY strategy."""
    print("🚀 VectorBT Backtesting Suite for SPY Strategy")
    print("=" * 60)

    try:
        import vectorbt as vbt
        print("✅ VectorBT imported successfully")
    except ImportError:
        print("❌ VectorBT not available. Install with: pip install vectorbt")
        return None

    # Initialize strategy
    config = SPYMultiTimeframeConfig(
        polygon_api_key=None,  # Use simulated data for testing
        risk_per_trade=0.01,
        max_portfolio_heat=0.20,
        deviation_std=1.5
    )

    strategy = SPYMultiTimeframeStrategy(config)

    # Generate extended test data
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=252)).strftime('%Y-%m-%d')  # 1 year

    print(f"📊 Generating data from {start_date} to {end_date}...")

    # Get data for all timeframes
    daily_data = strategy.get_polygon_data("SPY", "day", start_date, end_date)
    hourly_data = strategy.get_polygon_data("SPY", "hour", start_date, end_date)
    four_hour_data = strategy._resample_to_4hour(hourly_data.copy())

    print(f"✅ Daily bars: {len(daily_data)}")
    print(f"✅ 4-Hour bars: {len(four_hour_data)}")
    print(f"✅ Hourly bars: {len(hourly_data)}")

    if len(daily_data) < 50:
        print("❌ Insufficient daily data for backtesting")
        return None

    # Generate signals based on strategy rules
    print("\n📊 Generating strategy signals...")

    # Calculate indicators
    ema_9 = strategy.calculate_ema(daily_data['close'], 9)
    ema_20 = strategy.calculate_ema(daily_data['close'], 20)
    ema_72 = strategy.calculate_ema(daily_data['close'], 72)
    ema_89 = strategy.calculate_ema(daily_data['close'], 89)

    # Deviation bands for setup identification
    upper_dev_9, lower_dev_9 = strategy.calculate_deviation_bands(daily_data['close'], 9, 1.5)
    upper_dev_72, lower_dev_72 = strategy.calculate_deviation_bands(daily_data['close'], 72, 1.5)

    # Generate entry signals (simplified for VectorBT)
    # Entry when: 9>20 AND price touches lower deviation band
    bullish_regime = ema_9 > ema_20
    price_at_lower_band = daily_data['close'] <= lower_dev_9

    # Combine conditions for entries
    entries = bullish_regime & price_at_lower_band

    # Generate exit signals
    # Exit when: 9<20 OR price reaches upper 72/89 deviation band
    bearish_regime = ema_9 < ema_20
    price_at_upper_band = daily_data['close'] >= upper_dev_72

    exits = bearish_regime | price_at_upper_band

    # Apply some additional filters for realistic trading
    # Don't enter on consecutive days (avoid overtrading)
    entries = entries & (~entries.shift(1).fillna(False))

    # Don't exit too quickly (minimum hold period)
    exits = exits & (~entries.shift(5).fillna(False))  # Don't exit within 5 days of entry

    print(f"✅ Entry signals generated: {entries.sum()}")
    print(f"✅ Exit signals generated: {exits.sum()}")

    # Run VectorBT backtest with different configurations
    print("\n📈 Running VectorBT backtests...")

    backtests = {}

    # 1. Basic Strategy
    pf_basic = vbt.Portfolio.from_signals(
        close=daily_data['close'],
        entries=entries,
        exits=exits,
        init_cash=100_000,
        fees=0.001,
        slippage=0.001
    )

    backtests['Basic Strategy'] = pf_basic

    # 2. With Stop Loss
    atr = strategy.calculate_atr(daily_data, 14)
    stop_loss_distance = atr * 2.0  # 2x ATR stop loss

    pf_with_stop = vbt.Portfolio.from_signals(
        close=daily_data['close'],
        entries=entries,
        exits=exits,
        init_cash=100_000,
        fees=0.001,
        slippage=0.001,
        sl_stop=stop_loss_distance
    )

    backtests['With Stop Loss'] = pf_with_stop

    # 3. With Take Profit
    take_profit_distance = atr * 3.0  # 3x ATR take profit

    pf_with_tp = vbt.Portfolio.from_signals(
        close=daily_data['close'],
        entries=entries,
        exits=exits,
        init_cash=100_000,
        fees=0.001,
        slippage=0.001,
        tp_stop=take_profit_distance
    )

    backtests['With Take Profit'] = pf_with_tp

    # 4. Complete Strategy (Stop Loss + Take Profit)
    pf_complete = vbt.Portfolio.from_signals(
        close=daily_data['close'],
        entries=entries,
        exits=exits,
        init_cash=100_000,
        fees=0.001,
        slippage=0.001,
        sl_stop=stop_loss_distance,
        tp_stop=take_profit_distance
    )

    backtests['Complete Strategy'] = pf_complete

    # Display results
    print("\n📊 VectorBT Backtest Results:")
    print("=" * 80)
    print(f"{'Strategy':<20} {'Return':<10} {'Sharpe':<8} {'Max DD':<10} {'Trades':<8} {'Win Rate':<10}")
    print("-" * 80)

    for strategy_name, pf in backtests.items():
        try:
            total_return = pf.total_return()
            sharpe_ratio = pf.sharpe_ratio()
            max_drawdown = pf.max_drawdown()
            total_trades = pf.trades.count()

            # Handle cases where there might be no trades
            if total_trades > 0:
                win_rate = pf.trades.win_rate()
            else:
                win_rate = 0.0

            print(f"{strategy_name:<20} "
                  f"{total_return:<10.2%} "
                  f"{sharpe_ratio:<8.2f} "
                  f"{max_drawdown:<10.2%} "
                  f"{total_trades:<8} "
                  f"{win_rate:<10.1%}")

        except Exception as e:
            print(f"{strategy_name:<20} Error: {str(e)}")

    # Find best strategy
    try:
        best_strategy = max(backtests.items(), key=lambda x: x[1].sharpe_ratio())
        print(f"\n🏆 Best Strategy: {best_strategy[0]} (Sharpe: {best_strategy[1].sharpe_ratio():.2f})")
    except:
        print("\n⚠️ Could not determine best strategy due to calculation errors")

    # Detailed analysis of best strategy
    print("\n📈 Detailed Analysis:")
    print("=" * 50)

    try:
        best_pf = backtests['Complete Strategy']

        print(f"Total Return: {best_pf.total_return():.2%}")
        print(f"Annualized Return: {best_pf.annualized_return():.2%}")
        print(f"Sharpe Ratio: {best_pf.sharpe_ratio():.2f}")
        print(f"Sortino Ratio: {best_pf.sortino_ratio():.2f}")
        print(f"Max Drawdown: {best_pf.max_drawdown():.2%}")
        print(f"Calmar Ratio: {best_pf.calmar_ratio():.2f}")
        print(f"Total Trades: {best_pf.trades.count()}")

        if best_pf.trades.count() > 0:
            print(f"Win Rate: {best_pf.trades.win_rate():.1%}")
            print(f"Profit Factor: {best_pf.trades.profit_factor():.2f}")
            print(f"Average Win: ${best_pf.trades.wins().mean():.2f}")
            print(f"Average Loss: ${best_pf.trades.losses().mean():.2f}")

    except Exception as e:
        print(f"Error in detailed analysis: {e}")

    # Trade log
    print("\n📋 Recent Trades:")
    print("=" * 50)

    try:
        best_pf = backtests['Complete Strategy']
        trades = best_pf.trades.records

        if len(trades) > 0:
            # Convert to DataFrame for better display
            trades_df = pd.DataFrame(trades)

            # Show last 10 trades
            recent_trades = trades_df.tail(10)

            for i, (_, trade) in enumerate(recent_trades.iterrows()):
                entry_idx = trade['entry_idx']
                exit_idx = trade['exit_idx']
                entry_price = trade['entry_price']
                exit_price = trade['exit_price']
                pnl = trade['pnl']

                entry_date = daily_data.index[entry_idx].strftime('%Y-%m-%d')
                exit_date = daily_data.index[exit_idx].strftime('%Y-%m-%d')

                pnl_str = f"${pnl:+.2f}"
                if pnl > 0:
                    pnl_str = f"📈 {pnl_str}"
                else:
                    pnl_str = f"📉 {pnl_str}"

                print(f"{i+1:2d}. {entry_date} → {exit_date} "
                      f"Entry: ${entry_price:.2f} Exit: ${exit_price:.2f} {pnl_str}")

        else:
            print("No trades generated in test period")

    except Exception as e:
        print(f"Error generating trade log: {e}")

    # Equity curve
    print("\n📊 Equity Curve Analysis:")
    print("=" * 50)

    try:
        best_pf = backtests['Complete Strategy']
        equity_curve = best_pf.value()

        print(f"Starting Equity: ${equity_curve.iloc[0]:.2f}")
        print(f"Ending Equity: ${equity_curve.iloc[-1]:.2f}")
        print(f"Peak Equity: ${equity_curve.max():.2f}")
        print(f"Lowest Equity: ${equity_curve.min():.2f}")

        # Calculate drawdown periods
        drawdown = best_pf.drawdown()
        max_dd_period = drawdown.idxmin()
        max_dd_date = daily_data.index[max_dd_period] if max_dd_period < len(daily_data) else None

        if max_dd_date:
            print(f"Max Drawdown Date: {max_dd_date.strftime('%Y-%m-%d')}")

    except Exception as e:
        print(f"Error in equity curve analysis: {e}")

    return backtests

def compare_with_benchmark():
    """Compare strategy performance with SPY buy-and-hold."""
    print("\n🎯 Benchmark Comparison")
    print("=" * 50)

    try:
        import vectorbt as vbt

        # Generate SPY data for the same period
        strategy = SPYMultiTimeframeStrategy()
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=252)).strftime('%Y-%m-%d')

        spy_data = strategy.get_polygon_data("SPY", "day", start_date, end_date)

        if len(spy_data) == 0:
            print("❌ Could not generate SPY benchmark data")
            return None

        # SPY buy-and-hold benchmark
        pf_spy = vbt.Portfolio.from_holding(
            close=spy_data['close'],
            init_cash=100_000
        )

        # Strategy performance (from previous test)
        ema_9 = strategy.calculate_ema(spy_data['close'], 9)
        ema_20 = strategy.calculate_ema(spy_data['close'], 20)
        upper_dev_9, lower_dev_9 = strategy.calculate_deviation_bands(spy_data['close'], 9, 1.5)

        bullish_regime = ema_9 > ema_20
        price_at_lower_band = spy_data['close'] <= lower_dev_9
        entries = bullish_regime & price_at_lower_band & (~entries.shift(1).fillna(False))

        bearish_regime = ema_9 < ema_20
        upper_dev_72, lower_dev_72 = strategy.calculate_deviation_bands(spy_data['close'], 72, 1.5)
        price_at_upper_band = spy_data['close'] >= upper_dev_72
        exits = bearish_regime | price_at_upper_band
        exits = exits & (~entries.shift(5).fillna(False))

        pf_strategy = vbt.Portfolio.from_signals(
            close=spy_data['close'],
            entries=entries,
            exits=exits,
            init_cash=100_000,
            fees=0.001,
            slippage=0.001
        )

        # Comparison
        print(f"{'Metric':<20} {'SPY Buy & Hold':<15} {'Strategy':<15} {'Outperformance':<15}")
        print("-" * 65)

        spy_return = pf_spy.total_return()
        strategy_return = pf_strategy.total_return()
        outperformance = strategy_return - spy_return

        print(f"{'Total Return':<20} {spy_return:<15.2%} {strategy_return:<15.2%} {outperformance:<15.2%}")

        spy_sharpe = pf_spy.sharpe_ratio()
        strategy_sharpe = pf_strategy.sharpe_ratio()
        sharpe_outperformance = strategy_sharpe - spy_sharpe

        print(f"{'Sharpe Ratio':<20} {spy_sharpe:<15.2f} {strategy_sharpe:<15.2f} {sharpe_outperformance:<15.2f}")

        spy_dd = pf_spy.max_drawdown()
        strategy_dd = pf_strategy.max_drawdown()
        dd_improvement = spy_dd - strategy_dd  # Lower drawdown is better

        print(f"{'Max Drawdown':<20} {spy_dd:<15.2%} {strategy_dd:<15.2%} {dd_improvement:<15.2%}")

        spy_trades = pf_spy.trades.count()
        strategy_trades = pf_strategy.trades.count()

        print(f"{'Total Trades':<20} {spy_trades:<15} {strategy_trades:<15} {'N/A':<15}")

        return {
            'spy_benchmark': pf_spy,
            'strategy': pf_strategy,
            'outperformance': outperformance
        }

    except Exception as e:
        print(f"❌ Benchmark comparison failed: {e}")
        return None

def main():
    """Main function to run all backtesting analyses."""
    print("🧪 SPY Strategy VectorBT Backtesting Suite")
    print("=" * 60)

    # Run main backtest
    backtests = run_vectorbt_backtest()

    if backtests:
        # Compare with benchmark
        benchmark_results = compare_with_benchmark()

        print(f"\n📊 Final Summary")
        print("=" * 50)

        if benchmark_results:
            outperformance = benchmark_results['outperformance']
            if outperformance > 0:
                print(f"🎉 Strategy outperformed SPY buy-and-hold by {outperformance:.2%}")
            else:
                print(f"⚠️ Strategy underperformed SPY buy-and-hold by {abs(outperformance):.2%}")

        print(f"\n🔧 Recommendations:")
        print("1. Add real Polygon API key for live data")
        print("2. Optimize entry/exit parameters")
        print("3. Consider market regime filters")
        print("4. Add position sizing rules")
        print("5. Implement walk-forward analysis")

        return backtests
    else:
        print("❌ Backtesting failed to complete")
        return None

if __name__ == "__main__":
    results = main()