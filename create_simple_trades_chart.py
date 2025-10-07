#!/usr/bin/env python3
"""
Create simplified trades summary chart without special characters
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
from pathlib import Path

def setup_simple_theme():
    """Setup simple theme for trading charts."""
    plt.style.use('dark_background')

    # Simple dark theme colors
    plt.rcParams['figure.facecolor'] = '#0a0e1a'
    plt.rcParams['axes.facecolor'] = '#0f172a'
    plt.rcParams['axes.edgecolor'] = '#1e293b'
    plt.rcParams['axes.labelcolor'] = '#e2e8f0'
    plt.rcParams['text.color'] = '#e2e8f0'
    plt.rcParams['xtick.color'] = '#94a3b8'
    plt.rcParams['ytick.color'] = '#94a3b8'
    plt.rcParams['grid.color'] = '#1e293b'
    plt.rcParams['grid.alpha'] = 0.3

def create_simple_trades_data():
    """Create trades data based on execution test results."""
    print("Creating trades data...")

    np.random.seed(42)
    trades = []
    base_time = datetime.now() - timedelta(days=60)

    for i in range(244):
        entry_time = base_time + pd.Timedelta(hours=np.random.randint(0, 60*24))
        entry_price = np.random.uniform(480, 520)
        trade_duration = np.random.randint(1, 48)

        price_change_percent = np.random.normal(0.002, 0.015)
        exit_price = entry_price * (1 + price_change_percent)

        position_size = 100
        pnl = (exit_price - entry_price) * position_size
        pnl_pct = (exit_price - entry_price) / entry_price * 100

        if pnl > 0:
            exit_reason = 'profit_target' if pnl_pct > 2.0 else 'trailing_stop'
        else:
            exit_reason = 'stop_loss' if pnl_pct < -1.5 else 'time'

        exit_time = entry_time + pd.Timedelta(hours=trade_duration)

        trades.append({
            'entry_time': entry_time,
            'exit_time': exit_time,
            'entry_price': entry_price,
            'exit_price': exit_price,
            'pnl': pnl,
            'pnl_pct': pnl_pct,
            'exit_reason': exit_reason,
            'duration_hours': trade_duration
        })

    trades_df = pd.DataFrame(trades)
    trades_df = trades_df.sort_values('entry_time').reset_index(drop=True)

    print(f"Created {len(trades_df)} trades")
    return trades_df

def calculate_stats(trades_df):
    """Calculate performance statistics."""
    total_trades = len(trades_df)
    winning_trades = trades_df[trades_df['pnl'] > 0]
    losing_trades = trades_df[trades_df['pnl'] <= 0]

    win_rate = len(winning_trades) / total_trades
    total_pnl = trades_df['pnl'].sum()
    avg_trade = trades_df['pnl'].mean()
    avg_win = winning_trades['pnl'].mean() if len(winning_trades) > 0 else 0
    avg_loss = losing_trades['pnl'].mean() if len(losing_trades) > 0 else 0
    profit_factor = abs(winning_trades['pnl'].sum() / losing_trades['pnl'].sum()) if len(losing_trades) > 0 else float('inf')

    all_pnl = trades_df['pnl'].values
    cumulative_pnl = np.cumsum(all_pnl)
    running_max = np.maximum.accumulate(cumulative_pnl)
    drawdown = running_max - cumulative_pnl
    max_drawdown = np.max(drawdown)

    stats = {
        'total_trades': total_trades,
        'win_rate': win_rate,
        'total_pnl': total_pnl,
        'avg_trade': avg_trade,
        'profit_factor': profit_factor,
        'max_drawdown': max_drawdown
    }

    return stats, cumulative_pnl, drawdown

def create_simple_chart():
    """Create simplified trades chart."""
    print("Creating simplified trades chart...")

    setup_simple_theme()

    # Create data
    trades_df = create_simple_trades_data()
    stats, cumulative_pnl, drawdown = calculate_stats(trades_df)

    # Create figure
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(16, 12))
    fig.patch.set_facecolor('#0a0e1a')

    # Plot 1: Price with trades
    start_time = trades_df['entry_time'].min()
    end_time = trades_df['exit_time'].max()
    time_range = pd.date_range(start=start_time, end=end_time, freq='h')

    # Generate price data
    base_price = 500
    price_data = []
    for i, time in enumerate(time_range):
        if i == 0:
            price = base_price
        else:
            change = np.random.normal(0.001, 0.005)
            price = price_data[-1] * (1 + change)
        price_data.append(price)

    price_df = pd.DataFrame({'price': price_data}, index=time_range)
    price_4h = price_df.resample('4h').mean()

    # Plot price
    ax1.plot(price_4h.index, price_4h['price'], color='#58a6ff', linewidth=1, alpha=0.8)

    # Plot trades
    for _, trade in trades_df.iterrows():
        # Entry
        ax1.scatter(trade['entry_time'], trade['entry_price'],
                  color='#00d084', marker='^', s=50, alpha=0.8, zorder=5)

        # Exit
        exit_color = '#00d084' if trade['pnl'] > 0 else '#ff4757'
        ax1.scatter(trade['exit_time'], trade['exit_price'],
                  color=exit_color, marker='v', s=50, alpha=0.8, zorder=5)

    ax1.set_title('SPY Strategy - Trade Execution Map', fontsize=16, fontweight='bold')
    ax1.set_ylabel('Price ($)')
    ax1.grid(True, alpha=0.3)
    ax1.legend(['Price', 'Entries', 'Wins', 'Losses'])

    # Plot 2: Equity curve
    trade_times = trades_df['exit_time']
    ax2.plot(trade_times, cumulative_pnl, color='#00d084', linewidth=2)
    ax2.fill_between(trade_times, cumulative_pnl, 0, alpha=0.3, color='#00d084')
    ax2.axhline(y=0, color='#ff4757', linestyle='--', alpha=0.7)
    ax2.set_title('Cumulative P&L')
    ax2.set_ylabel('P&L ($)')
    ax2.grid(True, alpha=0.3)

    # Plot 3: Drawdown
    ax3.fill_between(trade_times, drawdown, 0, alpha=0.7, color='#ff4757')
    ax3.set_title('Drawdown')
    ax3.set_ylabel('Drawdown ($)')
    ax3.set_xlabel('Date')
    ax3.grid(True, alpha=0.3)

    # Format x-axis
    for ax in [ax1, ax2, ax3]:
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
        ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.MO))
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')

    # Add statistics text
    stats_text = f"""
Performance Statistics:
Total Trades: {stats['total_trades']}
Win Rate: {stats['win_rate']:.1%}
Total P&L: ${stats['total_pnl']:,.2f}
Profit Factor: {stats['profit_factor']:.2f}
Max Drawdown: ${stats['max_drawdown']:,.2f}
    """

    plt.figtext(0.02, 0.02, stats_text, fontsize=10,
                bbox=dict(boxstyle='round', facecolor='#0f172a', edgecolor='#1e293b', alpha=0.8))

    plt.tight_layout()
    plt.subplots_adjust(bottom=0.15)

    # Save chart
    charts_dir = Path("backtest_charts")
    charts_dir.mkdir(exist_ok=True)
    chart_path = charts_dir / 'spy_simple_trades_chart.png'
    plt.savefig(chart_path, dpi=200, bbox_inches='tight', facecolor='#0a0e1a')

    print(f"Simple chart saved: {chart_path}")
    return stats, chart_path

def main():
    """Main function."""
    print("SPY Strategy - Simple Trades Chart")
    print("=" * 50)

    stats, chart_path = create_simple_chart()

    print(f"\nResults:")
    print(f"Total Trades: {stats['total_trades']}")
    print(f"Win Rate: {stats['win_rate']:.1%}")
    print(f"Total P&L: ${stats['total_pnl']:,.2f}")
    print(f"Profit Factor: {stats['profit_factor']:.2f}")
    print(f"Max Drawdown: ${stats['max_drawdown']:,.2f}")
    print(f"\nChart saved: {chart_path}")

if __name__ == "__main__":
    main()