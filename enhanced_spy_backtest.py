#!/usr/bin/env python3
"""
Enhanced SPY Strategy Backtest with Visualization
Creates comprehensive backtest results with charts and trade analysis
"""

import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent))

from spy_multi_timeframe_strategy import SPYMultiTimeframeStrategy, SPYMultiTimeframeConfig

def create_enhanced_backtest():
    """Create enhanced backtest with visualization."""
    print("📊 Enhanced SPY Strategy Backtest with Visualization")
    print("=" * 60)

    try:
        import vectorbt as vbt
        print("✅ VectorBT imported successfully")
    except ImportError:
        print("❌ VectorBT not available. Install with: pip install vectorbt")
        return None

    # Initialize strategy with optimized parameters
    config = SPYMultiTimeframeConfig(
        polygon_api_key=None,  # Use simulated data for testing
        risk_per_trade=0.01,
        max_portfolio_heat=0.20,
        deviation_std=1.5
    )

    strategy = SPYMultiTimeframeStrategy(config)

    # Generate longer test data for better results
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=500)).strftime('%Y-%m-%d')  # ~16 months

    print(f"📊 Generating data from {start_date} to {end_date}...")

    # Get data for all timeframes
    daily_data = strategy.get_polygon_data("SPY", "day", start_date, end_date)
    hourly_data = strategy.get_polygon_data("SPY", "hour", start_date, end_date)
    four_hour_data = strategy._resample_to_4hour(hourly_data.copy())

    print(f"✅ Daily bars: {len(daily_data)}")
    print(f"✅ 4-Hour bars: {len(four_hour_data)}")
    print(f"✅ Hourly bars: {len(hourly_data)}")

    if len(daily_data) < 100:
        print("❌ Insufficient daily data for backtesting")
        return None

    # Generate strategy signals with adjusted parameters for more trades
    print("\n📊 Generating enhanced strategy signals...")

    # Calculate indicators
    ema_9 = strategy.calculate_ema(daily_data['close'], 9)
    ema_20 = strategy.calculate_ema(daily_data['close'], 20)
    ema_72 = strategy.calculate_ema(daily_data['close'], 72)
    ema_89 = strategy.calculate_ema(daily_data['close'], 89)

    # Deviation bands
    upper_dev_9, lower_dev_9 = strategy.calculate_deviation_bands(daily_data['close'], 9, 1.5)
    upper_dev_72, lower_dev_72 = strategy.calculate_deviation_bands(daily_data['close'], 72, 1.5)

    # Enhanced entry signals - more aggressive for testing
    bullish_regime = ema_9 > ema_20
    price_near_lower_band = daily_data['close'] <= lower_dev_9 * 1.02  # Slightly more generous
    price_momentum = daily_data['close'].pct_change(5) > -0.02  # Not too bearish

    entries = bullish_regime & price_near_lower_band & price_momentum

    # Enhanced exit signals
    bearish_regime = ema_9 < ema_20
    price_at_upper_band = daily_data['close'] >= upper_dev_72 * 0.98  # Slightly more conservative

    exits = bearish_regime | price_at_upper_band

    # Apply filters to avoid overtrading
    entries = entries & (~entries.shift(2).fillna(False))  # Don't enter every other day
    exits = exits & (~exits.shift(1).fillna(False))  # Allow exits next day

    print(f"✅ Entry signals generated: {entries.sum()}")
    print(f"✅ Exit signals generated: {exits.sum()}")

    # Create comprehensive backtest
    print("\n📈 Running comprehensive backtest...")

    # Calculate ATR for position sizing
    atr = strategy.calculate_atr(daily_data, 14)
    stop_loss_distance = atr * 1.5  # 1.5x ATR stop loss
    take_profit_distance = atr * 3.0  # 3x ATR take profit

    # Enhanced portfolio with proper risk management
    pf = vbt.Portfolio.from_signals(
        close=daily_data['close'],
        entries=entries,
        exits=exits,
        init_cash=100_000,
        fees=0.001,
        slippage=0.001,
        sl_stop=stop_loss_distance,
        tp_stop=take_profit_distance,
        size=np.full(len(daily_data), 0.10),  # 10% position size
        size_type='percent'
    )

    # Display comprehensive results
    print("\n📊 Enhanced Strategy Results:")
    print("=" * 50)

    try:
        total_return = pf.total_return()
        sharpe_ratio = pf.sharpe_ratio()
        max_drawdown = pf.max_drawdown()
        total_trades = pf.trades.count()
        calmar_ratio = pf.calmar_ratio()
        sortino_ratio = pf.sortino_ratio()

        print(f"Total Return: {total_return:.2%}")
        print(f"Annualized Return: {pf.annualized_return():.2%}")
        print(f"Sharpe Ratio: {sharpe_ratio:.2f}")
        print(f"Sortino Ratio: {sortino_ratio:.2f}")
        print(f"Max Drawdown: {max_drawdown:.2%}")
        print(f"Calmar Ratio: {calmar_ratio:.2f}")
        print(f"Total Trades: {total_trades}")

        if total_trades > 0:
            win_rate = pf.trades.win_rate()
            profit_factor = pf.trades.profit_factor()
            avg_win = pf.trades.wins().mean()
            avg_loss = pf.trades.losses().mean()
            avg_hold_time = pf.trades.holding_period.mean()

            print(f"Win Rate: {win_rate:.1%}")
            print(f"Profit Factor: {profit_factor:.2f}")
            print(f"Average Win: ${avg_win:.2f}")
            print(f"Average Loss: ${avg_loss:.2f}")
            print(f"Average Hold Time: {avg_hold_time:.1f} days")

    except Exception as e:
        print(f"Error in performance calculation: {e}")

    # Create visualization
    print("\n📈 Creating charts and visualizations...")

    # Create charts directory if it doesn't exist
    charts_dir = Path("backtest_charts")
    charts_dir.mkdir(exist_ok=True)

    try:
        # 1. Equity Curve
        plt.figure(figsize=(12, 8))
        equity_curve = pf.value()

        plt.subplot(2, 2, 1)
        plt.plot(equity_curve.index, equity_curve.values, label='Strategy Equity', color='blue', linewidth=2)
        plt.axhline(y=100000, color='gray', linestyle='--', label='Initial Capital')
        plt.title('Strategy Equity Curve')
        plt.xlabel('Date')
        plt.ylabel('Equity ($)')
        plt.legend()
        plt.grid(True, alpha=0.3)

        # 2. Drawdown
        plt.subplot(2, 2, 2)
        drawdown = pf.drawdown()
        plt.fill_between(drawdown.index, drawdown.values * 100, 0, color='red', alpha=0.3)
        plt.title('Drawdown (%)')
        plt.xlabel('Date')
        plt.ylabel('Drawdown (%)')
        plt.grid(True, alpha=0.3)

        # 3. Price with Entry/Exit Signals
        plt.subplot(2, 2, 3)
        plt.plot(daily_data.index, daily_data['close'], label='SPY Price', color='black', linewidth=1)

        # Plot entry signals
        entry_dates = daily_data.index[entries]
        entry_prices = daily_data.loc[entries, 'close']
        plt.scatter(entry_dates, entry_prices, color='green', marker='^', s=50, label='Entries', zorder=5)

        # Plot exit signals
        exit_dates = daily_data.index[exits]
        exit_prices = daily_data.loc[exits, 'close']
        plt.scatter(exit_dates, exit_prices, color='red', marker='v', s=50, label='Exits', zorder=5)

        # Plot EMAs
        plt.plot(daily_data.index, ema_9, label='EMA 9', color='blue', alpha=0.7, linewidth=1)
        plt.plot(daily_data.index, ema_20, label='EMA 20', color='orange', alpha=0.7, linewidth=1)
        plt.plot(daily_data.index, ema_72, label='EMA 72', color='purple', alpha=0.7, linewidth=1)
        plt.plot(daily_data.index, ema_89, label='EMA 89', color='brown', alpha=0.7, linewidth=1)

        plt.title('SPY Price with Strategy Signals')
        plt.xlabel('Date')
        plt.ylabel('Price ($)')
        plt.legend()
        plt.grid(True, alpha=0.3)

        # 4. Trade Distribution
        plt.subplot(2, 2, 4)
        if total_trades > 0:
            trade_pnl = pf.trades.pnl()
            plt.hist(trade_pnl, bins=20, alpha=0.7, color='blue', edgecolor='black')
            plt.axvline(x=0, color='red', linestyle='--', label='Breakeven')
            plt.title('Trade P&L Distribution')
            plt.xlabel('P&L ($)')
            plt.ylabel('Frequency')
            plt.legend()
            plt.grid(True, alpha=0.3)
        else:
            plt.text(0.5, 0.5, 'No trades to display', ha='center', va='center', transform=plt.gca().transAxes)
            plt.title('Trade P&L Distribution')

        plt.tight_layout()
        plt.savefig(charts_dir / 'spy_strategy_overview.png', dpi=300, bbox_inches='tight')
        print(f"✅ Saved overview chart: {charts_dir / 'spy_strategy_overview.png'}")

        # 5. Detailed Trade Analysis
        if total_trades > 0:
            plt.figure(figsize=(12, 6))

            # Individual trade P&L
            trades_df = pd.DataFrame(pf.trades.records)
            if len(trades_df) > 0:
                plt.subplot(1, 2, 1)
                colors = ['green' if pnl > 0 else 'red' for pnl in trades_df['pnl']]
                plt.bar(range(len(trades_df)), trades_df['pnl'], color=colors, alpha=0.7)
                plt.axhline(y=0, color='black', linestyle='-', linewidth=1)
                plt.title('Individual Trade P&L')
                plt.xlabel('Trade Number')
                plt.ylabel('P&L ($)')
                plt.grid(True, alpha=0.3)

                # Cumulative P&L
                plt.subplot(1, 2, 2)
                cumulative_pnl = trades_df['pnl'].cumsum()
                plt.plot(range(len(cumulative_pnl)), cumulative_pnl, color='blue', linewidth=2)
                plt.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
                plt.title('Cumulative P&L')
                plt.xlabel('Trade Number')
                plt.ylabel('Cumulative P&L ($)')
                plt.grid(True, alpha=0.3)

            plt.tight_layout()
            plt.savefig(charts_dir / 'spy_trade_analysis.png', dpi=300, bbox_inches='tight')
            print(f"✅ Saved trade analysis chart: {charts_dir / 'spy_trade_analysis.png'}")

        # 6. Monthly Performance Heatmap
        if len(equity_curve) > 30:
            plt.figure(figsize=(12, 8))
            monthly_returns = equity_curve.resample('M').last().pct_change().dropna()

            # Create calendar heatmap
            years = monthly_returns.index.year.unique()
            months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                     'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

            returns_matrix = []
            for year in years:
                year_returns = []
                for month in range(1, 13):
                    month_data = monthly_returns[(monthly_returns.index.year == year) &
                                               (monthly_returns.index.month == month)]
                    if len(month_data) > 0:
                        year_returns.append(month_data.iloc[0])
                    else:
                        year_returns.append(0)
                returns_matrix.append(year_returns)

            returns_matrix = np.array(returns_matrix).T * 100  # Convert to percentage

            plt.imshow(returns_matrix, cmap='RdYlGn', aspect='auto')
            plt.colorbar(label='Monthly Return (%)')
            plt.title('Monthly Performance Heatmap')
            plt.xlabel('Year')
            plt.ylabel('Month')
            plt.xticks(range(len(years)), years)
            plt.yticks(range(12), months)

            # Add text annotations
            for i in range(12):
                for j in range(len(years)):
                    color = 'white' if abs(returns_matrix[i, j]) > 5 else 'black'
                    plt.text(j, i, f'{returns_matrix[i, j]:.1f}%',
                            ha='center', va='center', color=color, fontsize=8)

            plt.tight_layout()
            plt.savefig(charts_dir / 'spy_monthly_heatmap.png', dpi=300, bbox_inches='tight')
            print(f"✅ Saved monthly heatmap: {charts_dir / 'spy_monthly_heatmap.png'}")

        print(f"\n📊 All charts saved to: {charts_dir}/")

    except Exception as e:
        print(f"❌ Error creating charts: {e}")

    # Trade Log Summary
    print("\n📋 Trade Summary")
    print("=" * 50)

    try:
        if total_trades > 0:
            trades = pf.trades.records
            trades_df = pd.DataFrame(trades)

            if len(trades_df) > 0:
                print(f"Total Trades: {len(trades_df)}")
                print(f"Winning Trades: {len(trades_df[trades_df['pnl'] > 0])}")
                print(f"Losing Trades: {len(trades_df[trades_df['pnl'] < 0])}")

                print(f"\nBest Trade: ${trades_df['pnl'].max():.2f}")
                print(f"Worst Trade: ${trades_df['pnl'].min():.2f}")
                print(f"Average Trade: ${trades_df['pnl'].mean():.2f}")

                print(f"\nAverage Hold Time: {trades_df['holding_period'].mean():.1f} days")
                print(f"Longest Hold Time: {trades_df['holding_period'].max():.1f} days")

                # Show recent trades
                print(f"\nRecent Trades:")
                print("-" * 80)
                recent_trades = trades_df.tail(10)

                for i, (_, trade) in enumerate(recent_trades.iterrows()):
                    entry_idx = int(trade['entry_idx'])
                    exit_idx = int(trade['exit_idx'])
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
                print("No trades executed in backtest period")
        else:
            print("No trades executed in backtest period")

    except Exception as e:
        print(f"Error generating trade summary: {e}")

    return {
        'portfolio': pf,
        'data': daily_data,
        'charts_dir': charts_dir,
        'performance': {
            'total_return': total_return,
            'sharpe_ratio': sharpe_ratio,
            'max_drawdown': max_drawdown,
            'total_trades': total_trades
        }
    }

def main():
    """Main function to run enhanced backtest."""
    print("🚀 Enhanced SPY Strategy Backtest Suite")
    print("=" * 60)

    results = create_enhanced_backtest()

    if results:
        print(f"\n📊 Final Summary")
        print("=" * 50)

        perf = results['performance']
        print(f"Strategy Performance:")
        print(f"  • Total Return: {perf['total_return']:.2%}")
        print(f"  • Sharpe Ratio: {perf['sharpe_ratio']:.2f}")
        print(f"  • Max Drawdown: {perf['max_drawdown']:.2%}")
        print(f"  • Total Trades: {perf['total_trades']}")

        print(f"\n📈 Charts Generated:")
        print(f"  • Strategy Overview (4-panel chart)")
        print(f"  • Trade Analysis")
        print(f"  • Monthly Performance Heatmap")

        print(f"\n🔧 Next Steps:")
        print(f"1. Add Polygon API key for real market data")
        print(f"2. Optimize strategy parameters based on results")
        print(f"3. Test different market regimes")
        print(f"4. Implement risk management improvements")

        print(f"\n📁 Charts saved to: {results['charts_dir']}/")

        return results
    else:
        print("❌ Enhanced backtest failed to complete")
        return None

if __name__ == "__main__":
    results = main()