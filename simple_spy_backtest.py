#!/usr/bin/env python3
"""
Simple SPY Strategy Backtest with Manual Visualization
Bypasses VectorBT display issues to show strategy performance
"""

import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent))

from spy_multi_timeframe_strategy import SPYMultiTimeframeStrategy, SPYMultiTimeframeConfig

def run_simple_backtest():
    """Run simplified backtest with manual calculations."""
    print("📊 Simple SPY Strategy Backtest")
    print("=" * 50)

    # Initialize strategy
    config = SPYMultiTimeframeConfig(
        polygon_api_key=None,  # Use simulated data
        risk_per_trade=0.01,
        max_portfolio_heat=0.20,
        deviation_std=1.5
    )

    strategy = SPYMultiTimeframeStrategy(config)

    # Generate test data
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')  # 1 year

    print(f"📊 Generating data from {start_date} to {end_date}...")

    daily_data = strategy.get_polygon_data("SPY", "day", start_date, end_date)
    hourly_data = strategy.get_polygon_data("SPY", "hour", start_date, end_date)

    print(f"✅ Daily bars: {len(daily_data)}")
    print(f"✅ Hourly bars: {len(hourly_data)}")

    if len(daily_data) < 50:
        print("❌ Insufficient data")
        return None

    # Calculate indicators
    print("\n📊 Calculating indicators...")
    ema_9 = strategy.calculate_ema(daily_data['close'], 9)
    ema_20 = strategy.calculate_ema(daily_data['close'], 20)
    ema_72 = strategy.calculate_ema(daily_data['close'], 72)
    ema_89 = strategy.calculate_ema(daily_data['close'], 89)

    # Deviation bands
    upper_dev_9, lower_dev_9 = strategy.calculate_deviation_bands(daily_data['close'], 9, 1.5)
    upper_dev_72, lower_dev_72 = strategy.calculate_deviation_bands(daily_data['close'], 72, 1.5)

    # Generate entry/exit signals
    print("📊 Generating signals...")
    bullish_regime = ema_9 > ema_20
    price_at_lower_band = daily_data['close'] <= lower_dev_9

    entries = bullish_regime & price_at_lower_band
    entries = entries & (~entries.shift(1).fillna(False))  # No consecutive entries

    bearish_regime = ema_9 < ema_20
    price_at_upper_band = daily_data['close'] >= upper_dev_72

    exits = bearish_regime | price_at_upper_band
    exits = exits & (~entries.shift(5).fillna(False))  # Don't exit too quickly

    print(f"✅ Entry signals: {entries.sum()}")
    print(f"✅ Exit signals: {exits.sum()}")

    # Manual backtest simulation
    print("\n📈 Running manual backtest...")
    initial_cash = 100000
    cash = initial_cash
    position = 0
    equity = []
    trades = []
    entry_price = 0
    entry_date = None

    for i, (date, row) in enumerate(daily_data.iterrows()):
        price = row['close']
        equity_value = cash + position * price
        equity.append(equity_value)

        # Entry logic
        if entries.iloc[i] and position == 0:
            # Risk-based position sizing
            risk_amount = cash * config.risk_per_trade
            stop_distance = price * 0.02  # 2% stop loss
            position_size = risk_amount / stop_distance
            position_size = min(position_size, cash * config.max_portfolio_heat / price)

            entry_price = price
            entry_date = date
            position = position_size
            cash -= position * price
            print(f"📈 Entry on {date.strftime('%Y-%m-%d')}: {position:.0f} shares @ ${price:.2f}")

        # Exit logic
        elif exits.iloc[i] and position > 0:
            exit_price = price
            pnl = (exit_price - entry_price) * position
            commission = position * price * 0.001  # 0.1% fees
            pnl -= commission

            cash += position * price
            trades.append({
                'entry_date': entry_date,
                'exit_date': date,
                'entry_price': entry_price,
                'exit_price': exit_price,
                'position': position,
                'pnl': pnl,
                'pnl_pct': (exit_price - entry_price) / entry_price * 100,
                'hold_days': (date - entry_date).days
            })

            print(f"📉 Exit on {date.strftime('%Y-%m-%d')}: {position:.0f} shares @ ${price:.2f}, P&L: ${pnl:+.2f}")

            position = 0
            entry_price = 0
            entry_date = None

    # Create equity series
    equity_series = pd.Series(equity, index=daily_data.index)

    # Calculate performance metrics
    total_return = (equity_series.iloc[-1] - initial_cash) / initial_cash
    daily_returns = equity_series.pct_change().dropna()
    sharpe_ratio = daily_returns.mean() / daily_returns.std() * np.sqrt(252) if len(daily_returns) > 0 else 0

    # Calculate drawdown
    running_max = equity_series.expanding().max()
    drawdown = (equity_series - running_max) / running_max
    max_drawdown = drawdown.min()

    # Display results
    print(f"\n📊 Performance Results:")
    print("-" * 40)
    print(f"Initial Capital: ${initial_cash:,.2f}")
    print(f"Final Equity: ${equity_series.iloc[-1]:,.2f}")
    print(f"Total Return: {total_return:.2%}")
    print(f"Sharpe Ratio: {sharpe_ratio:.2f}")
    print(f"Max Drawdown: {max_drawdown:.2%}")
    print(f"Total Trades: {len(trades)}")

    if len(trades) > 0:
        winning_trades = [t for t in trades if t['pnl'] > 0]
        losing_trades = [t for t in trades if t['pnl'] < 0]
        win_rate = len(winning_trades) / len(trades)

        avg_win = np.mean([t['pnl'] for t in winning_trades]) if winning_trades else 0
        avg_loss = np.mean([t['pnl'] for t in losing_trades]) if losing_trades else 0

        print(f"Win Rate: {win_rate:.1%}")
        print(f"Average Win: ${avg_win:.2f}")
        print(f"Average Loss: ${avg_loss:.2f}")

        if avg_loss != 0:
            profit_factor = abs(avg_win / avg_loss) * (len(winning_trades) / len(losing_trades)) if losing_trades else float('inf')
            print(f"Profit Factor: {profit_factor:.2f}")

    # Create visualizations
    print(f"\n📈 Creating charts...")
    charts_dir = Path("backtest_charts")
    charts_dir.mkdir(exist_ok=True)

    # 1. Equity Curve and Drawdown
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

    # Equity curve
    ax1.plot(equity_series.index, equity_series.values, label='Strategy Equity', color='blue', linewidth=2)
    ax1.axhline(y=initial_cash, color='gray', linestyle='--', label='Initial Capital', alpha=0.7)
    ax1.set_title('SPY Strategy - Equity Curve', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Equity ($)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Drawdown
    ax2.fill_between(drawdown.index, drawdown.values * 100, 0, color='red', alpha=0.3)
    ax2.set_title('Drawdown (%)', fontsize=14, fontweight='bold')
    ax2.set_ylabel('Drawdown (%)')
    ax2.set_xlabel('Date')
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(charts_dir / 'spy_equity_curve.png', dpi=300, bbox_inches='tight')
    print(f"✅ Saved equity curve: {charts_dir / 'spy_equity_curve.png'}")

    # 2. Price Chart with Signals
    fig, ax = plt.subplots(figsize=(14, 8))

    # Price
    ax.plot(daily_data.index, daily_data['close'], label='SPY Price', color='black', linewidth=2)

    # EMAs
    ax.plot(daily_data.index, ema_9, label='EMA 9', color='blue', alpha=0.8, linewidth=1.5)
    ax.plot(daily_data.index, ema_20, label='EMA 20', color='orange', alpha=0.8, linewidth=1.5)
    ax.plot(daily_data.index, ema_72, label='EMA 72', color='purple', alpha=0.8, linewidth=1.5)
    ax.plot(daily_data.index, ema_89, label='EMA 89', color='brown', alpha=0.8, linewidth=1.5)

    # Deviation bands
    ax.plot(daily_data.index, upper_dev_9, label='Upper Dev (9)', color='lightblue', alpha=0.5, linestyle='--')
    ax.plot(daily_data.index, lower_dev_9, label='Lower Dev (9)', color='lightblue', alpha=0.5, linestyle='--')
    ax.plot(daily_data.index, upper_dev_72, label='Upper Dev (72)', color='lightcoral', alpha=0.5, linestyle='--')
    ax.plot(daily_data.index, lower_dev_72, label='Lower Dev (72)', color='lightcoral', alpha=0.5, linestyle='--')

    # Entry/Exit signals
    entry_dates = daily_data.index[entries]
    entry_prices = daily_data.loc[entries, 'close']
    ax.scatter(entry_dates, entry_prices, color='green', marker='^', s=100, label='Entries', zorder=5)

    exit_dates = daily_data.index[exits]
    exit_prices = daily_data.loc[exits, 'close']
    ax.scatter(exit_dates, exit_prices, color='red', marker='v', s=100, label='Exits', zorder=5)

    ax.set_title('SPY Strategy - Price Chart with Indicators and Signals', fontsize=16, fontweight='bold')
    ax.set_xlabel('Date')
    ax.set_ylabel('Price ($)')
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    ax.grid(True, alpha=0.3)

    # Format x-axis
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.savefig(charts_dir / 'spy_price_chart.png', dpi=300, bbox_inches='tight')
    print(f"✅ Saved price chart: {charts_dir / 'spy_price_chart.png'}")

    # 3. Trade Analysis
    if len(trades) > 0:
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))

        # Trade P&L
        colors = ['green' if t['pnl'] > 0 else 'red' for t in trades]
        ax1.bar(range(len(trades)), [t['pnl'] for t in trades], color=colors, alpha=0.7)
        ax1.axhline(y=0, color='black', linestyle='-', linewidth=1)
        ax1.set_title('Individual Trade P&L', fontweight='bold')
        ax1.set_xlabel('Trade #')
        ax1.set_ylabel('P&L ($)')
        ax1.grid(True, alpha=0.3)

        # Cumulative P&L
        cumulative_pnl = np.cumsum([t['pnl'] for t in trades])
        ax2.plot(range(len(cumulative_pnl)), cumulative_pnl, color='blue', linewidth=2, marker='o')
        ax2.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
        ax2.set_title('Cumulative P&L', fontweight='bold')
        ax2.set_xlabel('Trade #')
        ax2.set_ylabel('Cumulative P&L ($)')
        ax2.grid(True, alpha=0.3)

        # Trade Distribution
        pnl_values = [t['pnl'] for t in trades]
        ax3.hist(pnl_values, bins=min(10, len(trades)), alpha=0.7, color='blue', edgecolor='black')
        ax3.axvline(x=0, color='red', linestyle='--', label='Breakeven')
        ax3.set_title('Trade P&L Distribution', fontweight='bold')
        ax3.set_xlabel('P&L ($)')
        ax3.set_ylabel('Frequency')
        ax3.legend()
        ax3.grid(True, alpha=0.3)

        # Hold Time vs P&L
        hold_times = [t['hold_days'] for t in trades]
        colors = ['green' if t['pnl'] > 0 else 'red' for t in trades]
        ax4.scatter(hold_times, pnl_values, color=colors, alpha=0.7, s=50)
        ax4.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
        ax4.set_title('Hold Time vs P&L', fontweight='bold')
        ax4.set_xlabel('Hold Days')
        ax4.set_ylabel('P&L ($)')
        ax4.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig(charts_dir / 'spy_trade_analysis.png', dpi=300, bbox_inches='tight')
        print(f"✅ Saved trade analysis: {charts_dir / 'spy_trade_analysis.png'}")

    # 4. Trade Log Summary
    print(f"\n📋 Trade Log")
    print("-" * 80)

    if len(trades) > 0:
        print(f"{'#':<3} {'Entry':<12} {'Exit':<12} {'Entry $':<8} {'Exit $':<8} {'P&L $':<10} {'P&L %':<8} {'Days':<5}")
        print("-" * 80)

        for i, trade in enumerate(trades[-10:]):  # Show last 10 trades
            entry_str = trade['entry_date'].strftime('%m/%d/%Y')
            exit_str = trade['exit_date'].strftime('%m/%d/%Y')
            pnl_str = f"{trade['pnl']:+.2f}"
            pct_str = f"{trade['pnl_pct']:+.1f}%"

            print(f"{i+1-len(trades):<3} {entry_str:<12} {exit_str:<12} "
                  f"{trade['entry_price']:<8.2f} {trade['exit_price']:<8.2f} "
                  f"{pnl_str:<10} {pct_str:<8} {trade['hold_days']:<5}")

        if len(trades) > 10:
            print(f"\n... and {len(trades) - 10} more trades")

    else:
        print("No trades executed in the backtest period")

    print(f"\n📊 Summary")
    print("-" * 40)
    print(f"Strategy generated {len(trades)} trades over {len(daily_data)} days")
    print(f"Final equity: ${equity_series.iloc[-1]:,.2f}")
    print(f"Total return: {total_return:.2%}")
    print(f"Sharpe ratio: {sharpe_ratio:.2f}")
    print(f"Maximum drawdown: {max_drawdown:.2%}")

    print(f"\n📁 Charts saved to: {charts_dir}/")

    return {
        'equity_curve': equity_series,
        'trades': trades,
        'performance': {
            'total_return': total_return,
            'sharpe_ratio': sharpe_ratio,
            'max_drawdown': max_drawdown,
            'total_trades': len(trades)
        }
    }

def main():
    """Main function."""
    print("🚀 SPY Strategy - Simple Backtest with Visualization")
    print("=" * 60)

    results = run_simple_backtest()

    if results:
        print(f"\n🎉 Backtest completed successfully!")
        print(f"📈 Check the backtest_charts/ directory for detailed visualizations")

        # Additional recommendations
        print(f"\n💡 Strategy Analysis:")
        perf = results['performance']

        if perf['total_return'] > 0:
            print(f"✅ Strategy is profitable with {perf['total_return']:.2%} return")
        else:
            print(f"⚠️ Strategy shows negative performance")

        if perf['sharpe_ratio'] > 1.0:
            print(f"✅ Good risk-adjusted returns (Sharpe: {perf['sharpe_ratio']:.2f})")
        elif perf['sharpe_ratio'] > 0:
            print(f"⚠️ Moderate risk-adjusted returns (Sharpe: {perf['sharpe_ratio']:.2f})")
        else:
            print(f"❌ Poor risk-adjusted returns")

        if perf['max_drawdown'] > -0.20:
            print(f"✅ Drawdown controlled at {perf['max_drawdown']:.1%}")
        else:
            print(f"⚠️ High drawdown of {perf['max_drawdown']:.1%}")

        print(f"\n🔧 Optimization suggestions:")
        print(f"1. Add Polygon API key for real market data")
        print(f"2. Test different entry/exit parameters")
        print(f"3. Add market regime filters")
        print(f"4. Optimize position sizing")

        return results
    else:
        print("❌ Backtest failed")
        return None

if __name__ == "__main__":
    results = main()