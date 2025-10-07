#!/usr/bin/env python3
"""
Optimized SPY Strategy with Better Parameters
Tuned version with enhanced signal generation and risk management
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

def run_optimized_backtest():
    """Run optimized SPY strategy backtest."""
    print("🚀 Optimized SPY Strategy Backtest")
    print("=" * 50)

    # Enhanced configuration with better parameters
    config = SPYMultiTimeframeConfig(
        polygon_api_key=None,  # Use simulated data for now
        risk_per_trade=0.015,  # 1.5% risk per trade
        max_portfolio_heat=0.30,  # 30% max portfolio heat
        deviation_std=1.2  # Tighter deviation bands for more signals
    )

    strategy = SPYMultiTimeframeStrategy(config)

    # Generate test data - longer period for better results
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=730)).strftime('%Y-%m-%d')  # 2 years

    print(f"📊 Generating data from {start_date} to {end_date}...")

    daily_data = strategy.get_polygon_data("SPY", "day", start_date, end_date)
    hourly_data = strategy.get_polygon_data("SPY", "hour", start_date, end_date)
    four_hour_data = strategy._resample_to_4hour(hourly_data.copy())

    print(f"✅ Daily bars: {len(daily_data)}")
    print(f"✅ 4-Hour bars: {len(four_hour_data)}")
    print(f"✅ Hourly bars: {len(hourly_data)}")

    if len(daily_data) < 100:
        print("❌ Insufficient data")
        return None

    # Calculate indicators
    print("\n📊 Calculating optimized indicators...")
    ema_9 = strategy.calculate_ema(daily_data['close'], 9)
    ema_20 = strategy.calculate_ema(daily_data['close'], 20)
    ema_50 = strategy.calculate_ema(daily_data['close'], 50)  # Additional EMA for trend strength
    ema_72 = strategy.calculate_ema(daily_data['close'], 72)
    ema_89 = strategy.calculate_ema(daily_data['close'], 89)

    # Enhanced deviation bands with tighter parameters
    upper_dev_9, lower_dev_9 = strategy.calculate_deviation_bands(daily_data['close'], 9, config.deviation_std)
    upper_dev_20, lower_dev_20 = strategy.calculate_deviation_bands(daily_data['close'], 20, config.deviation_std)
    upper_dev_72, lower_dev_72 = strategy.calculate_deviation_bands(daily_data['close'], 72, config.deviation_std)

    # Enhanced entry signals - multiple confirmation layers
    print("📊 Generating enhanced signals...")

    # Primary trend filter
    bullish_trend = (ema_9 > ema_20) & (ema_20 > ema_50) & (ema_50 > ema_72)
    strong_bullish = bullish_trend & (daily_data['close'] > ema_89)

    # Price action filters
    price_at_lower_deviation = daily_data['close'] <= lower_dev_9 * 1.01  # Near lower band
    price_momentum = daily_data['close'].pct_change(3) > -0.03  # 3-day momentum not too negative
    volume_confirmation = daily_data.get('volume', pd.Series(1, index=daily_data.index)) > 0  # Volume exists

    # Enhanced entries with multiple confirmations
    entries = strong_bullish & price_at_lower_deviation & price_momentum & volume_confirmation
    entries = entries & (~entries.shift(1).fillna(False))  # No consecutive entries
    entries = entries & (~entries.shift(2).fillna(False))  # No entries 2 days prior

    # Enhanced exit signals
    bearish_regime = ema_9 < ema_20
    price_at_upper_deviation = daily_data['close'] >= upper_dev_72 * 0.98  # Near upper band
    trend_weakness = ema_20 < ema_50  # Medium-term trend weakening

    exits = bearish_regime | price_at_upper_deviation | trend_weakness
    exits = exits & (~exits.shift(1).fillna(False))  # No consecutive exits

    print(f"✅ Entry signals: {entries.sum()}")
    print(f"✅ Exit signals: {exits.sum()}")

    # Enhanced backtest with position sizing
    print("\n📈 Running optimized backtest...")
    initial_cash = 100000
    cash = initial_cash
    position = 0
    equity = []
    trades = []
    entry_price = 0
    entry_date = None
    stop_loss_price = 0
    trailing_stop_price = 0

    # Risk management parameters
    atr = strategy.calculate_atr(daily_data, 14)

    for i, (date, row) in enumerate(daily_data.iterrows()):
        price = row['close']
        equity_value = cash + position * price
        equity.append(equity_value)

        # Update trailing stop if in position
        if position > 0:
            # Daily trailing stop - update daily
            current_atr = atr.iloc[i] if i < len(atr) else atr.iloc[-1]
            trail_distance = current_atr * 2.0  # 2x ATR trailing stop

            # Update trailing stop if price moves up
            if price > trailing_stop_price:
                trailing_stop_price = price - trail_distance

            # Check for stop loss hit
            if price <= trailing_stop_price:
                exit_price = price
                pnl = (exit_price - entry_price) * position
                commission = position * price * 0.001
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
                    'hold_days': (date - entry_date).days,
                    'exit_reason': 'trailing_stop'
                })

                print(f"🛑 Trailing Stop on {date.strftime('%Y-%m-%d')}: {position:.0f} shares @ ${price:.2f}, P&L: ${pnl:+.2f}")

                position = 0
                entry_price = 0
                entry_date = None
                trailing_stop_price = 0
                continue

        # Entry logic
        if entries.iloc[i] and position == 0:
            # Enhanced position sizing
            current_atr = atr.iloc[i] if i < len(atr) else atr.iloc[-1]
            risk_amount = cash * config.risk_per_trade
            stop_distance = current_atr * 2.0  # 2x ATR stop loss
            position_size = risk_amount / stop_distance
            position_size = min(position_size, cash * config.max_portfolio_heat / price)

            entry_price = price
            entry_date = date
            position = position_size
            trailing_stop_price = entry_price - stop_distance  # Initial stop loss

            cash -= position * price
            print(f"📈 Entry on {date.strftime('%Y-%m-%d')}: {position:.0f} shares @ ${price:.2f}, Stop: ${trailing_stop_price:.2f}")

        # Regular exit logic (non-trailing stop)
        elif exits.iloc[i] and position > 0:
            exit_price = price
            pnl = (exit_price - entry_price) * position
            commission = position * price * 0.001
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
                'hold_days': (date - entry_date).days,
                'exit_reason': 'signal'
            })

            print(f"📉 Signal Exit on {date.strftime('%Y-%m-%d')}: {position:.0f} shares @ ${price:.2f}, P&L: ${pnl:+.2f}")

            position = 0
            entry_price = 0
            entry_date = None
            trailing_stop_price = 0

    # Create equity series
    equity_series = pd.Series(equity, index=daily_data.index)

    # Enhanced performance metrics
    total_return = (equity_series.iloc[-1] - initial_cash) / initial_cash
    daily_returns = equity_series.pct_change().dropna()
    sharpe_ratio = daily_returns.mean() / daily_returns.std() * np.sqrt(252) if len(daily_returns) > 1 else 0

    # Calculate drawdown
    running_max = equity_series.expanding().max()
    drawdown = (equity_series - running_max) / running_max
    max_drawdown = drawdown.min()

    # Win rate and other metrics
    if len(trades) > 0:
        winning_trades = [t for t in trades if t['pnl'] > 0]
        losing_trades = [t for t in trades if t['pnl'] < 0]
        win_rate = len(winning_trades) / len(trades)

        avg_win = np.mean([t['pnl'] for t in winning_trades]) if winning_trades else 0
        avg_loss = np.mean([t['pnl'] for t in losing_trades]) if losing_trades else 0

        total_gains = sum([t['pnl'] for t in winning_trades])
        total_losses = abs(sum([t['pnl'] for t in losing_trades]))
        profit_factor = total_gains / total_losses if total_losses > 0 else float('inf')

        avg_hold_time = np.mean([t['hold_days'] for t in trades])
    else:
        win_rate = 0
        avg_win = 0
        avg_loss = 0
        profit_factor = 0
        avg_hold_time = 0

    # Display results
    print(f"\n📊 Optimized Strategy Results:")
    print("-" * 50)
    print(f"Initial Capital: ${initial_cash:,.2f}")
    print(f"Final Equity: ${equity_series.iloc[-1]:,.2f}")
    print(f"Total Return: {total_return:.2%}")
    print(f"Annualized Return: {(1 + total_return) ** (365 / len(daily_data)) - 1:.2%}")
    print(f"Sharpe Ratio: {sharpe_ratio:.2f}")
    print(f"Max Drawdown: {max_drawdown:.2%}")
    print(f"Total Trades: {len(trades)}")
    print(f"Win Rate: {win_rate:.1%}")
    print(f"Profit Factor: {profit_factor:.2f}")
    print(f"Average Hold Time: {avg_hold_time:.1f} days")

    # Create enhanced visualizations
    print(f"\n📈 Creating enhanced charts...")
    charts_dir = Path("backtest_charts")
    charts_dir.mkdir(exist_ok=True)

    # 1. Comprehensive Strategy Overview
    fig = plt.figure(figsize=(16, 12))

    # Equity curve and drawdown
    ax1 = plt.subplot(3, 2, 1)
    ax1.plot(equity_series.index, equity_series.values, label='Strategy Equity', color='blue', linewidth=2)
    ax1.axhline(y=initial_cash, color='gray', linestyle='--', label='Initial Capital', alpha=0.7)
    ax1.set_title('Equity Curve', fontweight='bold')
    ax1.set_ylabel('Equity ($)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Drawdown
    ax2 = plt.subplot(3, 2, 2)
    ax2.fill_between(drawdown.index, drawdown.values * 100, 0, color='red', alpha=0.3)
    ax2.set_title('Drawdown (%)', fontweight='bold')
    ax2.set_ylabel('Drawdown (%)')
    ax2.grid(True, alpha=0.3)

    # Price with all indicators
    ax3 = plt.subplot(3, 2, 3)
    ax3.plot(daily_data.index, daily_data['close'], label='SPY Price', color='black', linewidth=2)
    ax3.plot(daily_data.index, ema_9, label='EMA 9', color='blue', alpha=0.8, linewidth=1.5)
    ax3.plot(daily_data.index, ema_20, label='EMA 20', color='orange', alpha=0.8, linewidth=1.5)
    ax3.plot(daily_data.index, ema_72, label='EMA 72', color='purple', alpha=0.8, linewidth=1.5)
    ax3.plot(daily_data.index, ema_89, label='EMA 89', color='brown', alpha=0.8, linewidth=1.5)
    ax3.plot(daily_data.index, lower_dev_9, label='Lower Dev 9', color='lightblue', alpha=0.5, linestyle='--')
    ax3.scatter(daily_data.index[entries], daily_data.loc[entries, 'close'],
               color='green', marker='^', s=100, label='Entries', zorder=5)
    ax3.scatter(daily_data.index[exits], daily_data.loc[exits, 'close'],
               color='red', marker='v', s=100, label='Exits', zorder=5)
    ax3.set_title('Price with Indicators', fontweight='bold')
    ax3.set_ylabel('Price ($)')
    ax3.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    ax3.grid(True, alpha=0.3)

    # Trade P&L distribution
    if len(trades) > 0:
        ax4 = plt.subplot(3, 2, 4)
        colors = ['green' if t['pnl'] > 0 else 'red' for t in trades]
        ax4.bar(range(len(trades)), [t['pnl'] for t in trades], color=colors, alpha=0.7)
        ax4.axhline(y=0, color='black', linestyle='-', linewidth=1)
        ax4.set_title('Trade P&L', fontweight='bold')
        ax4.set_xlabel('Trade #')
        ax4.set_ylabel('P&L ($)')
        ax4.grid(True, alpha=0.3)

    # Monthly returns heatmap
    if len(equity_series) > 30:
        ax5 = plt.subplot(3, 2, 5)
        monthly_returns = equity_series.resample('M').last().pct_change().dropna()
        monthly_returns = monthly_returns * 100

        # Create simple monthly bar chart
        months = [d.strftime('%Y-%m') for d in monthly_returns.index]
        colors = ['green' if r > 0 else 'red' for r in monthly_returns.values]
        ax5.bar(range(len(monthly_returns)), monthly_returns.values, color=colors, alpha=0.7)
        ax5.axhline(y=0, color='black', linestyle='-', linewidth=1)
        ax5.set_title('Monthly Returns (%)', fontweight='bold')
        ax5.set_xlabel('Month')
        ax5.set_ylabel('Return (%)')
        ax5.set_xticks(range(len(months)))
        ax5.set_xticklabels(months, rotation=45, ha='right')
        ax5.grid(True, alpha=0.3)

    # Performance metrics radar chart (simplified)
    ax6 = plt.subplot(3, 2, 6)
    metrics = ['Win Rate', 'Profit Factor', 'Sharpe', 'Return/Drawdown']
    values = [
        win_rate * 100,  # Convert to percentage
        min(profit_factor, 3),  # Cap at 3
        max(sharpe_ratio, -2),  # Show negative values
        abs(total_return / max_drawdown) if max_drawdown != 0 else 0
    ]
    ax6.bar(metrics, values, color=['blue', 'green', 'orange', 'purple'], alpha=0.7)
    ax6.set_title('Performance Metrics', fontweight='bold')
    ax6.set_ylabel('Value')
    ax6.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(charts_dir / 'optimized_strategy_overview.png', dpi=300, bbox_inches='tight')
    print(f"✅ Saved optimized overview: {charts_dir / 'optimized_strategy_overview.png'}")

    # 2. Detailed trade analysis
    if len(trades) > 0:
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))

        # Cumulative P&L
        cumulative_pnl = np.cumsum([t['pnl'] for t in trades])
        ax1.plot(range(len(cumulative_pnl)), cumulative_pnl, color='blue', linewidth=2, marker='o')
        ax1.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
        ax1.set_title('Cumulative P&L', fontweight='bold')
        ax1.set_xlabel('Trade #')
        ax1.set_ylabel('Cumulative P&L ($)')
        ax1.grid(True, alpha=0.3)

        # P&L histogram
        pnl_values = [t['pnl'] for t in trades]
        ax2.hist(pnl_values, bins=min(10, len(trades)), alpha=0.7, color='blue', edgecolor='black')
        ax2.axvline(x=0, color='red', linestyle='--', label='Breakeven')
        ax2.set_title('P&L Distribution', fontweight='bold')
        ax2.set_xlabel('P&L ($)')
        ax2.set_ylabel('Frequency')
        ax2.legend()
        ax2.grid(True, alpha=0.3)

        # Hold time vs P&L
        hold_times = [t['hold_days'] for t in trades]
        colors = ['green' if t['pnl'] > 0 else 'red' for t in trades]
        ax3.scatter(hold_times, pnl_values, color=colors, alpha=0.7, s=50)
        ax3.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
        ax3.set_title('Hold Time vs P&L', fontweight='bold')
        ax3.set_xlabel('Hold Days')
        ax3.set_ylabel('P&L ($)')
        ax3.grid(True, alpha=0.3)

        # Exit reasons
        exit_reasons = [t['exit_reason'] for t in trades]
        unique_reasons = list(set(exit_reasons))
        reason_counts = [exit_reasons.count(reason) for reason in unique_reasons]
        ax4.pie(reason_counts, labels=unique_reasons, autopct='%1.1f%%', startangle=90)
        ax4.set_title('Exit Reasons', fontweight='bold')

        plt.tight_layout()
        plt.savefig(charts_dir / 'optimized_trade_analysis.png', dpi=300, bbox_inches='tight')
        print(f"✅ Saved trade analysis: {charts_dir / 'optimized_trade_analysis.png'}")

    # Detailed trade log
    print(f"\n📋 Detailed Trade Log")
    print("-" * 100)
    print(f"{'#':<3} {'Entry':<12} {'Exit':<12} {'Entry $':<8} {'Exit $':<8} {'P&L $':<10} {'P&L %':<8} {'Days':<5} {'Reason':<10}")
    print("-" * 100)

    for i, trade in enumerate(trades):
        entry_str = trade['entry_date'].strftime('%m/%d/%Y')
        exit_str = trade['exit_date'].strftime('%m/%d/%Y')
        pnl_str = f"{trade['pnl']:+.2f}"
        pct_str = f"{trade['pnl_pct']:+.1f}%"
        reason = trade['exit_reason'][:8] if trade['exit_reason'] else 'signal'

        print(f"{i+1:<3} {entry_str:<12} {exit_str:<12} "
              f"{trade['entry_price']:<8.2f} {trade['exit_price']:<8.2f} "
              f"{pnl_str:<10} {pct_str:<8} {trade['hold_days']:<5} {reason:<10}")

    return {
        'equity_curve': equity_series,
        'trades': trades,
        'performance': {
            'total_return': total_return,
            'sharpe_ratio': sharpe_ratio,
            'max_drawdown': max_drawdown,
            'total_trades': len(trades),
            'win_rate': win_rate,
            'profit_factor': profit_factor,
            'avg_hold_time': avg_hold_time
        }
    }

def main():
    """Main function."""
    print("🚀 Optimized SPY Strategy Test")
    print("=" * 50)

    results = run_optimized_backtest()

    if results:
        perf = results['performance']

        print(f"\n🎯 Strategy Assessment:")
        print("-" * 40)

        # Performance evaluation
        if perf['total_return'] > 0.05:  # >5% return
            print(f"✅ Strong performance: {perf['total_return']:.2%} return")
        elif perf['total_return'] > 0:
            print(f"⚠️ Modest positive performance: {perf['total_return']:.2%} return")
        else:
            print(f"❌ Negative performance: {perf['total_return']:.2%} return")

        if perf['sharpe_ratio'] > 1.0:
            print(f"✅ Excellent risk-adjusted returns (Sharpe: {perf['sharpe_ratio']:.2f})")
        elif perf['sharpe_ratio'] > 0.5:
            print(f"⚠️ Moderate risk-adjusted returns (Sharpe: {perf['sharpe_ratio']:.2f})")
        else:
            print(f"❌ Poor risk-adjusted returns (Sharpe: {perf['sharpe_ratio']:.2f})")

        if perf['max_drawdown'] > -0.15:  # <15% drawdown
            print(f"✅ Excellent drawdown control: {perf['max_drawdown']:.1%}")
        elif perf['max_drawdown'] > -0.25:
            print(f"⚠️ Moderate drawdown: {perf['max_drawdown']:.1%}")
        else:
            print(f"❌ High drawdown: {perf['max_drawdown']:.1%}")

        if perf['win_rate'] > 0.6:
            print(f"✅ High win rate: {perf['win_rate']:.1%}")
        elif perf['win_rate'] > 0.45:
            print(f"⚠️ Moderate win rate: {perf['win_rate']:.1%}")
        else:
            print(f"❌ Low win rate: {perf['win_rate']:.1%}")

        print(f"\n📁 Enhanced charts saved to: backtest_charts/")
        print(f"\n🔧 Next steps for optimization:")
        print(f"1. Add real Polygon API data")
        print(f"2. Test different deviation band parameters")
        print(f"3. Implement market regime detection")
        print(f"4. Add position scaling based on volatility")
        print(f"5. Consider sector rotation filters")

        return results
    else:
        print("❌ Optimized backtest failed")
        return None

if __name__ == "__main__":
    results = main()