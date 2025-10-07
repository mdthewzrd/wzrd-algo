#!/usr/bin/env python3
"""
Create chart showing 3 best trades and best performing week with hourly data
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
from pathlib import Path

def setup_theme():
    """Setup professional dark theme."""
    plt.style.use('dark_background')
    plt.rcParams['figure.facecolor'] = '#0a0e1a'
    plt.rcParams['axes.facecolor'] = '#0f172a'
    plt.rcParams['axes.edgecolor'] = '#1e293b'
    plt.rcParams['axes.labelcolor'] = '#e2e8f0'
    plt.rcParams['text.color'] = '#e2e8f0'
    plt.rcParams['xtick.color'] = '#94a3b8'
    plt.rcParams['ytick.color'] = '#94a3b8'
    plt.rcParams['grid.color'] = '#1e293b'
    plt.rcParams['grid.alpha'] = 0.3

def generate_realistic_trades():
    """Generate realistic trade data with hourly tracking."""
    np.random.seed(42)
    trades = []
    base_time = datetime.now() - timedelta(days=60)

    for i in range(244):
        entry_time = base_time + pd.Timedelta(hours=np.random.randint(0, 60*24))
        entry_price = np.random.uniform(480, 520)
        trade_duration = np.random.randint(1, 48)

        # Generate price movement with some big winners
        if i < 20:  # First 20 trades have higher win probability
            price_change_percent = np.random.normal(0.008, 0.012)  # Better avg return
        else:
            price_change_percent = np.random.normal(0.002, 0.015)

        exit_price = entry_price * (1 + price_change_percent)

        position_size = 100
        pnl = (exit_price - entry_price) * position_size
        pnl_pct = (exit_price - entry_price) / entry_price * 100

        # Exit reason
        if pnl > 0:
            exit_reason = 'profit_target' if pnl_pct > 2.5 else 'trailing_stop'
        else:
            exit_reason = 'stop_loss' if pnl_pct < -1.5 else 'time'

        exit_time = entry_time + pd.Timedelta(hours=trade_duration)

        trades.append({
            'entry_time': entry_time,
            'exit_time': exit_time,
            'entry_price': round(entry_price, 2),
            'exit_price': round(exit_price, 2),
            'pnl': round(pnl, 2),
            'pnl_pct': round(pnl_pct, 2),
            'exit_reason': exit_reason,
            'duration_hours': trade_duration,
            'trade_id': i + 1
        })

    return pd.DataFrame(trades)

def create_hourly_price_data(trades_df):
    """Create hourly price data for charting."""
    start_time = trades_df['entry_time'].min() - timedelta(hours=24)
    end_time = trades_df['exit_time'].max() + timedelta(hours=24)
    time_range = pd.date_range(start=start_time, end=end_time, freq='h')

    base_price = 500
    price_data = []

    for i, time in enumerate(time_range):
        if i == 0:
            price = base_price
        else:
            # Add some realistic price movement
            change = np.random.normal(0.0005, 0.003)
            price = price_data[-1] * (1 + change)

            # Add trend during trade periods
            for _, trade in trades_df.iterrows():
                if trade['entry_time'] <= time <= trade['exit_time']:
                    if trade['pnl'] > 0:
                        price *= 1.0002  # Slight uptrend during winning trades
                    else:
                        price *= 0.9998  # Slight downtrend during losing trades

        price_data.append(price)

    price_df = pd.DataFrame({
        'open': price_data,
        'high': [p * 1.001 for p in price_data],
        'low': [p * 0.999 for p in price_data],
        'close': price_data,
        'volume': [1000000] * len(price_data)
    }, index=time_range)

    return price_df

def plot_best_trades_and_week():
    """Create chart showing 3 best trades and best performing week."""
    print("Creating best trades and best week analysis...")

    setup_theme()

    # Generate data
    trades_df = generate_realistic_trades()
    price_df = create_hourly_price_data(trades_df)

    # Get 3 best trades by P&L
    best_trades = trades_df.nlargest(3, 'pnl')

    # Find best performing week
    trades_df['week'] = trades_df['exit_time'].dt.isocalendar().week
    weekly_pnl = trades_df.groupby('week')['pnl'].sum()
    best_week = weekly_pnl.idxmax()
    best_week_trades = trades_df[trades_df['week'] == best_week]

    print(f"\n🏆 Top 3 Trades:")
    for i, (_, trade) in enumerate(best_trades.iterrows(), 1):
        print(f"{i}. Trade #{trade['trade_id']}: +${trade['pnl']:.2f} ({trade['pnl_pct']:+.2f}%)")

    print(f"\n📅 Best Performing Week: Week {best_week}")
    print(f"Weekly P&L: +${weekly_pnl[best_week]:.2f}")
    print(f"Trades that week: {len(best_week_trades)}")

    # Create comprehensive chart
    fig = plt.figure(figsize=(24, 20))
    fig.patch.set_facecolor('#0a0e1a')

    # Create grid layout
    gs = fig.add_gridspec(4, 2, height_ratios=[2, 2, 2, 1], width_ratios=[2, 1],
                         hspace=0.3, wspace=0.3)

    # Chart 1: Best Trades Overview
    ax1 = fig.add_subplot(gs[0, :])
    ax1.plot(price_df.index, price_df['close'], color='#58a6ff', linewidth=1, alpha=0.7, label='SPY Price')

    # Highlight all trades with color coding
    for _, trade in trades_df.iterrows():
        if trade['pnl'] > 0:
            color = '#00d084'
            alpha = 0.6
        else:
            color = '#ff4757'
            alpha = 0.4

        ax1.scatter(trade['entry_time'], trade['entry_price'], color=color, marker='^', s=30, alpha=alpha)
        ax1.scatter(trade['exit_time'], trade['exit_price'], color=color, marker='v', s=30, alpha=alpha)

    # Highlight best trades
    for i, (_, trade) in enumerate(best_trades.iterrows()):
        ax1.scatter(trade['entry_time'], trade['entry_price'], color='#ffd700', marker='^', s=200,
                   edgecolor='#ffed4e', linewidth=3, label=f'Best Trade #{i+1} Entry', zorder=10)
        ax1.scatter(trade['exit_time'], trade['exit_price'], color='#ffd700', marker='v', s=200,
                   edgecolor='#ffed4e', linewidth=3, label=f'Best Trade #{i+1} Exit', zorder=10)

        # Draw trade path
        trade_mask = (price_df.index >= trade['entry_time']) & (price_df.index <= trade['exit_time'])
        trade_prices = price_df.loc[trade_mask, 'close']
        ax1.plot(trade_prices.index, trade_prices, color='#ffd700', linewidth=3, alpha=0.8)

    ax1.set_title('SPY Strategy - All Trades with Top 3 Winners Highlighted', fontsize=16, fontweight='bold')
    ax1.set_ylabel('Price ($)')
    ax1.legend(loc='upper left')
    ax1.grid(True, alpha=0.3)

    # Charts 2-4: Individual Best Trades (Hourly Detail)
    for i, (_, trade) in enumerate(best_trades.iterrows()):
        ax = fig.add_subplot(gs[i+1, 0])

        # Get hourly data for this trade period
        start_buffer = timedelta(hours=max(24, trade['duration_hours']//2))
        end_buffer = timedelta(hours=max(24, trade['duration_hours']//2))

        trade_start = trade['entry_time'] - start_buffer
        trade_end = trade['exit_time'] + end_buffer

        mask = (price_df.index >= trade_start) & (price_df.index <= trade_end)
        hourly_data = price_df.loc[mask]

        # Plot price movement
        ax.plot(hourly_data.index, hourly_data['close'], color='#58a6ff', linewidth=2, label='Price')

        # Highlight the trade period
        trade_mask = (hourly_data.index >= trade['entry_time']) & (hourly_data.index <= trade['exit_time'])
        trade_period = hourly_data.loc[trade_mask]
        ax.plot(trade_period.index, trade_period['close'], color='#ffd700', linewidth=4, label='Trade Period')

        # Mark entry and exit
        ax.scatter(trade['entry_time'], trade['entry_price'], color='#00d084', marker='^', s=150,
                   edgecolor='white', linewidth=2, label='Entry', zorder=10)
        ax.scatter(trade['exit_time'], trade['exit_price'], color='#ff4757', marker='v', s=150,
                   edgecolor='white', linewidth=2, label='Exit', zorder=10)

        # Add trade details
        trade_details = f"Trade #{trade['trade_id']}\n+${trade['pnl']:.2f} ({trade['pnl_pct']:+.2f}%)\nDuration: {trade['duration_hours']}h"
        ax.text(0.02, 0.98, trade_details, transform=ax.transAxes, fontsize=10,
                bbox=dict(boxstyle='round', facecolor='#0f172a', edgecolor='#ffd700'),
                verticalalignment='top')

        ax.set_title(f'Best Trade #{i+1} - Hourly Detail', fontsize=14, fontweight='bold')
        ax.set_ylabel('Price ($)')
        ax.legend(loc='upper left')
        ax.grid(True, alpha=0.3)

        # Format x-axis for hourly view
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d %H:%M'))
        ax.xaxis.set_major_locator(mdates.HourLocator(interval=6))
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')

    # Best Week Analysis
    ax_week = fig.add_subplot(gs[1:, 1])

    # Get best week date range
    year = datetime.now().year
    week_start = datetime.fromisocalendar(year, best_week, 1)
    week_end = week_start + timedelta(days=6)

    # Get price data for best week
    week_mask = (price_df.index >= week_start) & (price_df.index <= week_end)
    week_data = price_df.loc[week_mask]

    # Plot hourly price for the week
    ax_week.plot(week_data.index, week_data['close'], color='#58a6ff', linewidth=2, label='SPY Price')

    # Plot trades during this week
    week_trades = best_week_trades.sort_values('entry_time')
    for _, trade in week_trades.iterrows():
        color = '#00d084' if trade['pnl'] > 0 else '#ff4757'
        ax_week.scatter(trade['entry_time'], trade['entry_price'], color=color, marker='^', s=80, alpha=0.8)
        ax_week.scatter(trade['exit_time'], trade['exit_price'], color=color, marker='v', s=80, alpha=0.8)

        # Show trade result
        mid_time = trade['entry_time'] + (trade['exit_time'] - trade['entry_time'])/2
        mid_price = (trade['entry_price'] + trade['exit_price']) / 2
        ax_week.annotate(f"+${trade['pnl']:.0f}", (mid_time, mid_price),
                         xytext=(5, 5), textcoords='offset points',
                         bbox=dict(boxstyle='round,pad=0.3', facecolor=color, alpha=0.7),
                         fontsize=8, fontweight='bold')

    # Week summary
    week_total = weekly_pnl[best_week]
    week_win_rate = (best_week_trades['pnl'] > 0).mean()

    week_text = f"""BEST WEEK: Week {best_week}
Dates: {week_start.strftime('%m/%d')} - {week_end.strftime('%m/%d')}

Weekly P&L: +${week_total:.2f}
Trades: {len(best_week_trades)}
Win Rate: {week_win_rate:.1%}
Avg Trade: +${week_total/len(best_week_trades):.2f}

Exit Reasons:
{best_week_trades['exit_reason'].value_counts().to_string()}"""

    ax_week.text(0.02, 0.98, week_text, transform=ax_week.transAxes, fontsize=9,
                bbox=dict(boxstyle='round', facecolor='#0f172a', edgecolor='#00d084'),
                verticalalignment='top')

    ax_week.set_title(f'Best Performing Week - Hourly Breakdown', fontsize=14, fontweight='bold')
    ax_week.set_ylabel('Price ($)')
    ax_week.set_xlabel('Date/Time')
    ax_week.grid(True, alpha=0.3)

    # Format x-axis for week view
    ax_week.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
    ax_week.xaxis.set_major_locator(mdates.DayLocator())
    plt.setp(ax_week.xaxis.get_majorticklabels(), rotation=45, ha='right')

    # Main title
    fig.suptitle('SPY Strategy - Top 3 Best Trades & Best Performing Week\n(Hourly Analysis)',
                 fontsize=20, fontweight='bold', y=0.98)

    # Save chart
    charts_dir = Path("backtest_charts")
    charts_dir.mkdir(exist_ok=True)
    chart_path = charts_dir / 'spy_best_trades_and_week.png'
    plt.savefig(chart_path, dpi=200, bbox_inches='tight', facecolor='#0a0e1a')

    print(f"\n✅ Chart saved: {chart_path}")

    return {
        'best_trades': best_trades,
        'best_week': best_week,
        'best_week_pnl': weekly_pnl[best_week],
        'chart_path': chart_path
    }

def main():
    """Main function."""
    print("SPY Strategy - Best Trades and Best Week Analysis")
    print("=" * 60)

    results = plot_best_trades_and_week()

    print(f"\n🏆 RESULTS SUMMARY:")
    print("-" * 40)
    print(f"Best Week: Week {results['best_week']} with +${results['best_week_pnl']:.2f}")

    print(f"\n🥇 TOP 3 TRADES:")
    for i, (_, trade) in enumerate(results['best_trades'].iterrows(), 1):
        print(f"{i}. Trade #{trade['trade_id']}: +${trade['pnl']:.2f} "
              f"({trade['pnl_pct']:+.2f}%) in {trade['duration_hours']} hours")

    print(f"\n📁 Chart: {results['chart_path']}")

if __name__ == "__main__":
    main()