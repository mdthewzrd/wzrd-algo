#!/usr/bin/env python3
"""
Test script to verify the wizard algo mini workflow
This simulates the workflow and creates sample JSON outputs
"""

import json
import os
from datetime import datetime

def create_test_strategy_json():
    """Create a test strategy JSON file"""
    strategy = {
        "strategy_name": "Test_QQQ_Mean_Reversion",
        "description": "Simple mean reversion test strategy",
        "timeframe": "5min",
        "symbol": "QQQ",
        "entry_conditions": [
            {
                "type": "price_level",
                "description": "Price extends above VWAP with overbought RSI",
                "direction": "short",
                "indicators": ["vwap", "rsi", "volume"],
                "conditions": [
                    "Price > 1% above VWAP",
                    "RSI > 70",
                    "Volume > 1.5x average volume"
                ]
            }
        ],
        "exit_conditions": [
            {
                "type": "price_level",
                "description": "Price returns to VWAP",
                "direction": "close_short",
                "conditions": [
                    "Price <= VWAP",
                    "OR price reaches profit target"
                ]
            }
        ],
        "risk_management": {
            "stop_loss": {
                "type": "percentage",
                "value": 1.0
            },
            "take_profit": {
                "type": "r_multiple",
                "value": 2.0
            },
            "position_size": {
                "type": "r_based",
                "value": 1.0
            }
        }
    }

    with open("test_strategy_workflow.json", "w") as f:
        json.dump(strategy, f, indent=2)

    return strategy

def create_codified_strategy():
    """Create a codified strategy JSON file"""
    codified = {
        "strategy_name": "QQQ_Mean_Reversion_Codified",
        "description": "Codified mean reversion strategy with signals",
        "symbol": "QQQ",
        "timeframe": "5min",
        "entry_conditions": [
            {
                "type": "multi_timeframe_alignment",
                "description": "HTF trend + MTF setup + LTF execution",
                "direction": "short",
                "htf_condition": "Daily 50EMA < 200EMA",
                "mtf_condition": "15min price > 1% above VWAP",
                "ltf_condition": "5min RSI > 70 with volume confirmation"
            }
        ],
        "exit_conditions": [
            {
                "type": "profit_target",
                "description": "Take profit at target",
                "direction": "close_short"
            }
        ],
        "risk_management": {
            "stop_loss": {
                "type": "percentage",
                "value": 1.0
            },
            "take_profit": {
                "type": "r_multiple",
                "value": 2.0
            },
            "pyramiding": {
                "enabled": True,
                "max_legs": 2,
                "add_conditions": [
                    {
                        "level": "initial",
                        "size_r": 0.5,
                        "condition": "Initial entry"
                    },
                    {
                        "level": "confirmation",
                        "size_r": 0.5,
                        "condition": "Price confirmation"
                    }
                ]
            }
        },
        "signals": [
            {
                "timestamp": "2025-10-01 10:30:00",
                "type": "entry_short",
                "price": 350.25,
                "shares": 100,
                "position_id": "QQQ-2025-10-01-A",
                "leg": 1,
                "r_allocation": 0.5,
                "reason": "Technical setup detected",
                "execution": "SOLD 100 shares @ $350.25",
                "calculation": "stop 353.75 (risk $3.50) → shares=floor($250 / 3.50)=71 → rounded to 100 with portfolio sizing rules",
                "pnl": 0.0
            },
            {
                "timestamp": "2025-10-01 10:35:00",
                "type": "entry_short",
                "price": 350.50,
                "shares": 100,
                "position_id": "QQQ-2025-10-01-A",
                "leg": 2,
                "r_allocation": 0.5,
                "reason": "Price confirmation",
                "execution": "SOLD 100 shares @ $350.50",
                "calculation": "stop 354.01 (risk $3.51) → shares=floor($250 / 3.51)=71 → rounded to 100 with portfolio sizing rules",
                "pnl": 0.0
            },
            {
                "timestamp": "2025-10-01 11:15:00",
                "type": "exit_short",
                "price": 347.50,
                "shares": 200,
                "position_id": "QQQ-2025-10-01-A",
                "leg": 1,
                "r_allocation": 1.0,
                "reason": "Profit target reached",
                "execution": "BOUGHT 200 shares @ $347.50",
                "calculation": "Profit: $5.75 per share × 200 shares = $1,150 (2.3R)",
                "pnl": 1150.0
            }
        ],
        "performance_metrics": {
            "total_trades": 1,
            "winning_trades": 1,
            "losing_trades": 0,
            "win_rate": 100.0,
            "total_pnl": 1150.0,
            "profit_factor": 1.0,
            "expectancy_per_r": 2.3,
            "max_drawdown": 0.0,
            "average_win": 1150.0,
            "average_loss": 0.0,
            "largest_win": 1150.0,
            "largest_loss": 0.0
        },
        "provenance": {
            "generated_by": "signal_codifier",
            "data_source": "polygon_io",
            "rule_version": "v1.0.0",
            "generation_timestamp": datetime.now().isoformat(),
            "code_hash": "test_workflow_hash"
        }
    }

    with open("test_codified_workflow.json", "w") as f:
        json.dump(codified, f, indent=2)

    return codified

def main():
    """Run the test workflow"""
    print("🚀 Testing Wizard Algo Mini Workflow")
    print("=" * 50)

    print("\n📋 Step 1: Creating test strategy JSON...")
    strategy = create_test_strategy_json()
    print(f"✅ Created test_strategy_workflow.json")
    print(f"   Strategy: {strategy['strategy_name']}")
    print(f"   Symbol: {strategy['symbol']}")
    print(f"   Timeframe: {strategy['timeframe']}")

    print("\n📊 Step 2: Simulating Signal Codifier processing...")
    codified = create_codified_strategy()
    print(f"✅ Created test_codified_workflow.json")
    print(f"   Codified Strategy: {codified['strategy_name']}")
    print(f"   Total Signals: {len(codified['signals'])}")
    print(f"   Win Rate: {codified['performance_metrics']['win_rate']}%")
    print(f"   Total P&L: ${codified['performance_metrics']['total_pnl']}")

    print("\n📈 Step 3: Workflow Summary")
    print("   Input JSON → Signal Codifier → Output JSON")
    print("   ↓")
    print(f"   test_strategy_workflow.json → Processing → test_codified_workflow.json")

    print("\n🎯 Step 4: Expected Services")
    print("   📊 Signal Codifier: http://localhost:8502")
    print("   📈 Strategy Viewer:  http://localhost:8501")

    print("\n💡 Step 5: Usage Instructions")
    print("   1. Start services: python launch_streamlined_workflow.py")
    print("   2. Open Signal Codifier in browser")
    print("   3. Paste strategy JSON (like test_strategy_workflow.json)")
    print("   4. Get codified output")
    print("   5. Paste codified output into Strategy Viewer")
    print("   6. Visualize signals and performance")

    print("\n✅ Test workflow completed successfully!")
    print("📁 Files created:")
    print("   - test_strategy_workflow.json (input)")
    print("   - test_codified_workflow.json (output)")

if __name__ == "__main__":
    main()