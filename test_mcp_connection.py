#!/usr/bin/env python3
"""
Test script to verify Claude MCP (Model Context Protocol) connection
"""

import os
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent))

def test_mcp_connection():
    """Test Claude MCP connection"""
    
    print("🧪 Testing Claude MCP Connection")
    print("=" * 40)
    
    # Check environment variables
    mcp_vars = {
        "ANTHROPIC_BASE_URL": os.getenv("ANTHROPIC_BASE_URL"),
        "ANTHROPIC_AUTH_TOKEN": os.getenv("ANTHROPIC_AUTH_TOKEN"),
        "GLM_URL": os.getenv("GLM_URL"),
        "GLM_API_TOKEN": os.getenv("GLM_API_TOKEN")
    }
    
    found_vars = {k: v for k, v in mcp_vars.items() if v}
    
    if not found_vars:
        print("❌ No MCP environment variables found")
        print("\nTo fix this:")
        print("1. Make sure Claude Desktop is running")
        print("2. Run: python setup_mcp_connection.py")
        print("3. Or set manually:")
        print("   export ANTHROPIC_BASE_URL=http://localhost:3000")
        print("   export ANTHROPIC_AUTH_TOKEN=your_mcp_token")
        return False
    
    print("✅ Found MCP environment variables:")
    for var, value in found_vars.items():
        preview = f"{value[:20]}..." if len(value) > 20 else value
        print(f"   {var}: {preview}")
    
    # Test the connection
    try:
        from claude_mcp_client import ClaudeMCPClient
        
        print("\n🔌 Connecting to Claude via MCP...")
        client = ClaudeMCPClient()
        
        # Show connection info
        info = client.get_connection_info()
        print(f"📋 Connection Info:")
        for key, value in info.items():
            print(f"   {key}: {value}")
        
        # Simple test message
        print("\n💬 Testing message exchange...")
        response = client.send_message(
            "Hello! Please respond with exactly: 'MCP connection successful!'",
            max_tokens=50,
            temperature=0.1
        )
        
        response_text = response['content'][0]['text']
        print(f"✅ Connection successful!")
        print(f"Claude response: {response_text}")
        
        return True
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure Claude Desktop is running")
        print("2. Check your MCP connection details")
        print("3. Verify the MCP server is accessible")
        print("4. Run: python setup_mcp_connection.py check")
        return False

def test_trading_functionality():
    """Test trading-specific functionality via MCP"""
    
    print("\n🏦 Testing Trading Functionality via MCP")
    print("=" * 42)
    
    try:
        from claude_mcp_client import ClaudeMCPClient
        
        client = ClaudeMCPClient()
        
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

def check_claude_desktop():
    """Check if Claude Desktop is running"""
    
    print("🔍 Checking Claude Desktop Status")
    print("=" * 35)
    
    try:
        import subprocess
        result = subprocess.run(['pgrep', '-f', 'Claude'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Claude Desktop appears to be running")
            pids = result.stdout.strip().split('\n')
            print(f"   Process IDs: {', '.join(pids)}")
            return True
        else:
            print("❌ Claude Desktop doesn't appear to be running")
            print("   Please start Claude Desktop and try again")
            return False
    except Exception as e:
        print(f"⚠️  Could not check Claude Desktop status: {e}")
        return None

if __name__ == "__main__":
    print("🚀 Claude MCP Connection Test Suite")
    print("=" * 50)
    
    # Check Claude Desktop first
    desktop_running = check_claude_desktop()
    
    if desktop_running is False:
        print("\n❌ Please start Claude Desktop first, then run this test again.")
        sys.exit(1)
    
    # Test MCP connection
    success = test_mcp_connection()
    
    if success:
        test_trading_functionality()
        print("\n🎉 All MCP tests passed! Your system is ready.")
        print("\nYou can now run:")
        print("• python demo_enhanced_strategy_architect.py")
        print("• python test_enhanced_strategy_architect.py")
        print("• Any other trading scripts in the project")
    else:
        print("\n❌ MCP setup incomplete. Please fix the issues above.")
        print("Run: python setup_mcp_connection.py")
        sys.exit(1)
