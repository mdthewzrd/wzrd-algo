"""
Examples of using Claude GLM 4.5 API for wzrd-algo trading system
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from claude_mcp_client import ClaudeMCPClient as ClaudeGLMClient
import json
import pandas as pd

def test_basic_connection():
    """Test basic API connection"""
    print("🔍 Testing basic Claude API connection...")

    client = ClaudeGLMClient()

    try:
        response = client.send_message("Hello! I'm testing the API connection.")
        print("✅ Connection successful!")
        print(f"Response: {response['content'][0]['text']}")
        return True
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

def analyze_market_data():
    """Example: Analyze market data"""
    print("\n📈 Analyzing market data...")

    client = ClaudeGLMClient()

    # Sample market data
    market_data = {
        "symbol": "TSLA",
        "current_price": 250.50,
        "daily_change": 2.5,
        "volume": 45000000,
        "technical_indicators": {
            "rsi": 65.4,
            "macd": {"signal": "bullish", "value": 1.2},
            "moving_averages": {
                "sma_20": 245.30,
                "sma_50": 240.10,
                "ema_12": 248.75
            }
        },
        "market_sentiment": "bullish",
        "volatility": "medium"
    }

    try:
        analysis = client.get_trading_analysis(market_data)
        print("📊 Market Analysis:")
        print(analysis)
        return analysis
    except Exception as e:
        print(f"❌ Analysis failed: {e}")
        return None

def generate_trading_strategy():
    """Example: Generate trading strategy code"""
    print("\n🤖 Generating trading strategy code...")

    client = ClaudeGLMClient()

    strategy_description = """
    Create a mean reversion strategy for Tesla stock that:
    1. Uses Bollinger Bands for entry/exit signals
    2. Implements stop-loss at 2% below entry
    3. Takes profit at 3% above entry
    4. Uses RSI as confirmation filter (avoid oversold conditions)
    5. Works on 15-minute timeframes
    """

    try:
        strategy_code = client.generate_strategy_code(strategy_description)
        print("📝 Generated Strategy Code:")
        print(strategy_code)

        # Save to file
        with open("generated_strategies/bollinger_bands_strategy.py", "w") as f:
            f.write(strategy_code)
        print("💾 Strategy saved to generated_strategies/bollinger_bands_strategy.py")

        return strategy_code
    except Exception as e:
        print(f"❌ Strategy generation failed: {e}")
        return None

def conversation_example():
    """Example: Multi-turn conversation"""
    print("\n💬 Multi-turn conversation example...")

    client = ClaudeGLMClient()

    # Start conversation
    conversation_history = []

    # First message
    response1 = client.send_message(
        "I'm building a trading bot for crypto. What are the key components I need?",
        conversation_history=conversation_history
    )
    print(f"Claude: {response1['content'][0]['text']}")

    # Add to conversation history
    conversation_history.append({
        "role": "user",
        "content": "I'm building a trading bot for crypto. What are the key components I need?"
    })
    conversation_history.append({
        "role": "assistant",
        "content": response1['content'][0]['text']
    })

    # Follow-up message
    response2 = client.send_message(
        "Can you elaborate on the risk management component?",
        conversation_history=conversation_history
    )
    print(f"Claude: {response2['content'][0]['text']}")

def main():
    """Run all examples"""
    print("🚀 Claude GLM 4.5 API Examples for wzrd-algo")
    print("=" * 50)

    # Test connection first
    if not test_basic_connection():
        print("❌ Cannot proceed - API connection failed")
        return

    # Run examples
    analyze_market_data()
    generate_trading_strategy()
    conversation_example()

    print("\n✅ All examples completed!")

if __name__ == "__main__":
    main()