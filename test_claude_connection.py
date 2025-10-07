#!/usr/bin/env python3
"""
Simple test script to verify Claude Anthropic API connection
"""

import os
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent))

def test_claude_connection():
    """Test Claude API connection"""
    
    print("🧪 Testing Claude Anthropic API Connection")
    print("=" * 45)
    
    # Check environment variables
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌ ANTHROPIC_API_KEY environment variable not set")
        print("\nTo fix this:")
        print("1. Get your API key from https://console.anthropic.com/")
        print("2. Run: python setup_claude_env.py")
        print("3. Or set manually: export ANTHROPIC_API_KEY=your_key_here")
        return False
    
    print(f"✅ API key found (starts with: {api_key[:10]}...)")
    
    # Test the connection
    try:
        from claude_anthropic_client import ClaudeAnthropicClient
        
        print("\n🔌 Connecting to Claude API...")
        client = ClaudeAnthropicClient()
        
        # Simple test message
        response = client.send_message(
            "Hello! Please respond with exactly: 'Claude API connection successful!'",
            max_tokens=50,
            temperature=0.1
        )
        
        response_text = response['content'][0]['text']
        print(f"✅ Connection successful!")
        print(f"Claude response: {response_text}")
        
        # Test model info
        model_info = client.get_model_info()
        print(f"\n📋 Model Info:")
        for key, value in model_info.items():
            print(f"   {key}: {value}")
        
        return True
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

def test_trading_functionality():
    """Test trading-specific functionality"""
    
    print("\n🏦 Testing Trading Functionality")
    print("=" * 35)
    
    try:
        from claude_anthropic_client import ClaudeAnthropicClient
        
        client = ClaudeAnthropicClient()
        
        # Test market analysis
        sample_data = {
            "symbol": "SPY",
            "price": 450.25,
            "volume": 1000000,
            "rsi": 65.5,
            "macd": 2.1
        }
        
        print("📊 Testing market analysis...")
        analysis = client.get_trading_analysis(sample_data)
        print(f"✅ Analysis generated ({len(analysis)} characters)")
        print(f"Preview: {analysis[:100]}...")
        
        # Test strategy generation
        print("\n🎯 Testing strategy generation...")
        strategy_desc = "Simple RSI mean reversion strategy for SPY"
        code = client.generate_strategy_code(strategy_desc)
        print(f"✅ Strategy code generated ({len(code)} characters)")
        print(f"Preview: {code[:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Trading functionality test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_claude_connection()
    
    if success:
        test_trading_functionality()
        print("\n🎉 All tests passed! Claude is ready to use.")
        print("\nYou can now run:")
        print("• python demo_enhanced_strategy_architect.py")
        print("• python test_enhanced_strategy_architect.py")
        print("• Any other trading scripts in the project")
    else:
        print("\n❌ Setup incomplete. Please fix the issues above.")
        sys.exit(1)
