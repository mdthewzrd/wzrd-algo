#!/usr/bin/env python3
"""
Demo script for the Enhanced Strategy Architect
Run this to see the improved system in action!
"""

import asyncio
import logging
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent))

from agents.strategy_architect_enhanced import EnhancedStrategyArchitect
from claude_mcp_client import ClaudeMCPClient as ClaudeGLMClient

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def demo_basic_strategy():
    """Demo basic strategy generation."""
    print("🎯 Demo 1: Basic Momentum Strategy")
    print("=" * 50)

    architect = EnhancedStrategyArchitect()

    # Simple momentum strategy
    simple_strategy = """
    # Momentum Breakout Strategy

    This strategy captures momentum breakouts in large-cap stocks.

    ## Entry Conditions
    - Price breaks above 20-day high
    - Volume > 1.5x average volume
    - RSI > 50

    ## Exit Conditions
    - Take profit at 2R
    - Stop loss at 1R
    - Time exit after 5 days

    ## Risk Management
    - 1% risk per trade
    - Maximum 20% portfolio heat
    """

    try:
        result = architect.process_strategy_document(simple_strategy, "Momentum Breakout")

        print(f"✅ Strategy Generated: {result['strategy_name']}")
        print(f"📊 Complexity Score: {result['metadata']['complexity_score']}/100")
        print(f"⏱️ Estimated Time: {result['metadata']['estimated_development_time']}")
        print(f"📁 Files Generated: {list(result['generated_files'].keys())}")
        print(f"🔧 Technical Indicators: {', '.join(result['components']['indicators'])}")

        # Show sample code
        if 'strategy.py' in result['generated_files']:
            code = result['generated_files']['strategy.py']
            lines = code.split('\n')
            print(f"\n📝 Sample Code (first 20 lines):")
            print("-" * 40)
            for i, line in enumerate(lines[:20]):
                print(f"{i+1:2d}: {line}")

        return result

    except Exception as e:
        print(f"❌ Demo failed: {e}")
        return None


async def demo_complex_strategy():
    """Demo complex strategy generation."""
    print("\n🎯 Demo 2: Complex Mean Reversion Strategy")
    print("=" * 50)

    architect = EnhancedStrategyArchitect()

    # Complex strategy with advanced features
    complex_strategy = """
    # Advanced Mean Reversion Strategy

    ## Overview
    Multi-timeframe mean reversion strategy targeting overextended conditions in large-cap equities.

    ## Market Context
    - Large-cap US equities ($2B+ market cap)
    - 15-minute timeframe (context) + 5-minute (execution)
    - Intraday trading only
    - Avoid high volatility periods (VIX > 30)

    ## Entry Logic
    - Price extension > 2% above EMA72/89 confluence
    - Volume declining from 5-day peak (showing exhaustion)
    - RSI > 70 (overbought condition)
    - Gap threshold: 0.75× ATR minimum

    ## Entry Filters
    - Minimum 8M daily volume
    - Minimum $300M daily dollar volume
    - Price range $10-$500
    - 2.5% minimum daily range
    - Market cap > $2B
    - Avoid earnings announcement days

    ## Exit Conditions
    - Primary: Mean reversion to EMA confluence
    - Secondary: RSI drops below 50
    - Time exit: 75 minutes maximum
    - Stop loss: 1.5× ATR below entry
    - Trailing stop at breakeven after 1R profit

    ## Risk Management
    - Position sizing: 1% account risk per trade
    - Maximum portfolio heat: 20%
    - Maximum 6 concurrent positions
    - ATR-based position sizing
    - Sector correlation limits

    ## Pyramiding Rules
    - Maximum 2 additions per position
    - 50% size reduction on additions
    - Only add if original position is profitable
    - Minimum 30 minutes between additions

    ## Technical Indicators
    - Primary: EMA72/89 confluence
    - Secondary: RSI(14), Volume analysis, ATR(14)
    - Confirmation: Money Flow Index, Stochastic
    - Multi-timeframe: 15m context, 5m execution

    ## Performance Targets
    - Win rate: 65%+
    - Profit factor: 1.8+
    - Maximum drawdown: <12%
    - Average holding period: 8-24 hours

    ## Special Conditions
    - No trades during FOMC announcements
    - Reduced position size during high VIX
    - Sector rotation awareness
    - News sentiment filtering
    """

    try:
        result = architect.process_strategy_document(complex_strategy, "Advanced Mean Reversion")

        print(f"✅ Complex Strategy Generated: {result['strategy_name']}")
        print(f"📊 Complexity Score: {result['metadata']['complexity_score']}/100")
        print(f"⏱️ Estimated Time: {result['metadata']['estimated_development_time']}")
        print(f"📁 Files Generated: {list(result['generated_files'].keys())}")

        # Show key components
        components = result['components']
        print(f"\n🔍 Strategy Components:")
        print(f"   Type: {components['strategy_type']}")
        print(f"   Market: {components['market_focus']}")
        print(f"   Timeframe: {components['timeframe']}")
        print(f"   Risk Level: {components['risk_level']}")
        print(f"   Entry Conditions: {len(components['entry_conditions'])}")
        print(f"   Exit Conditions: {len(components['exit_conditions'])}")
        print(f"   Indicators: {', '.join(components['indicators'])}")

        return result

    except Exception as e:
        print(f"❌ Complex demo failed: {e}")
        return None


async def demo_claude_integration():
    """Demo Claude API integration for enhanced understanding."""
    print("\n🎯 Demo 3: Claude-Enhanced Strategy Analysis")
    print("=" * 50)

    try:
        # Test Claude connection
        claude_client = ClaudeGLMClient()

        # Create a strategy description that needs AI understanding
        strategy_description = """
        I want to build a pairs trading strategy for ETFs that:

        1. Finds correlated ETF pairs using cointegration analysis
        2. Trades when the spread deviates by 2 standard deviations
        3. Uses dynamic hedging with options
        4. Implements machine learning for regime detection
        5. Manages risk through portfolio-level optimization

        The strategy should work on daily data and handle market regime changes
        automatically. I need professional-grade code with proper backtesting.
        """

        # Use Claude to analyze the strategy
        analysis_response = claude_client.send_message(
            message=f"""
            Analyze this trading strategy request and provide structured requirements:

            {strategy_description}

            Return a structured analysis covering:
            1. Strategy type and approach
            2. Technical requirements
            3. Risk management needs
            4. Implementation complexity
            5. Key components needed
            """,
            max_tokens=1500,
            temperature=0.3
        )

        analysis = analysis_response['choices'][0]['message']['content']
        print("🤖 Claude Strategy Analysis:")
        print("-" * 40)
        print(analysis)

        # Now use the enhanced architect
        architect = EnhancedStrategyArchitect()
        result = architect.process_strategy_document(strategy_description, "AI-Enhanced Pairs Trading")

        print(f"\n✅ AI-Enhanced Strategy Generated")
        print(f"📊 Complexity Score: {result['metadata']['complexity_score']}/100")
        print(f"📁 Generated Files: {list(result['generated_files'].keys())}")

        return result

    except Exception as e:
        print(f"❌ Claude integration demo failed: {e}")
        return None


async def demo_error_handling():
    """Demo error handling and fallback mechanisms."""
    print("\n🎯 Demo 4: Error Handling & Fallbacks")
    print("=" * 50)

    architect = EnhancedStrategyArchitect()

    # Test with problematic documents
    test_cases = [
        {
            'name': 'Empty Document',
            'content': ''
        },
        {
            'name': 'Non-Strategy Text',
            'content': 'This is just regular text about trading, not a real strategy.'
        },
        {
            'name': 'Very Simple Strategy',
            'content': 'Buy low, sell high. Use stop loss.'
        }
    ]

    for test_case in test_cases:
        try:
            print(f"\n📋 Testing: {test_case['name']}")
            result = architect.process_strategy_document(test_case['content'], test_case['name'])

            if result and 'generated_files' in result:
                print(f"✅ Handled gracefully - Generated {len(result['generated_files'])} files")
                print(f"   Strategy: {result['strategy_name']}")
                print(f"   Complexity: {result['metadata']['complexity_score']}")
            else:
                print("❌ Failed to generate strategy")

        except Exception as e:
            print(f"⚠️ Error (expected): {e}")


async def main():
    """Run all demos."""
    print("🚀 Enhanced Strategy Architect Demo Suite")
    print("=" * 60)
    print("This demo shows the improvements made to the Strategy Architect:")
    print("✅ Better document parsing")
    print("✅ Professional code generation")
    print("✅ Claude AI integration")
    print("✅ Error handling & fallbacks")
    print("✅ Comprehensive testing framework")

    # Run demos
    demos = [
        demo_basic_strategy,
        demo_complex_strategy,
        demo_claude_integration,
        demo_error_handling
    ]

    results = []
    for demo in demos:
        try:
            result = await demo()
            results.append(result)
        except Exception as e:
            print(f"❌ Demo failed with error: {e}")
            results.append(None)

    # Summary
    print(f"\n📊 Demo Summary")
    print("=" * 50)
    successful_demos = sum(1 for r in results if r is not None)
    print(f"Successful demos: {successful_demos}/{len(demos)}")

    if successful_demos == len(demos):
        print("🎉 All demos completed successfully!")
        print("✅ The Enhanced Strategy Architect is working properly")
    else:
        print("⚠️ Some demos failed - check the error messages above")

    print(f"\n🔧 Next Steps:")
    print("1. Try the test suite: python test_enhanced_strategy_architect.py")
    print("2. Integrate with your Conversation Orchestrator")
    print("3. Add real-time market data feeds")
    print("4. Connect to backtesting frameworks")

    return results


if __name__ == "__main__":
    results = asyncio.run(main())