#!/usr/bin/env python3
"""
Test script to verify API key is working properly
"""

import os
from dotenv import load_dotenv
from data_integration import MarketDataFetcher

def test_api_key():
    """Test if the API key is working"""
    print("🔑 Testing API Key Configuration")
    print("=" * 40)

    # Load environment variables
    load_dotenv()

    # Check if API key is set
    api_key = os.getenv('POLYGON_API_KEY')
    if not api_key:
        print("❌ API key not found in environment variables")
        return False

    print(f"✅ API key found: {api_key[:10]}...{api_key[-10:]}")

    # Test API connection
    try:
        fetcher = MarketDataFetcher(api_key)

        # Try to fetch some test data
        print("📊 Testing API connection...")
        df = fetcher.fetch_ohlcv_data(
            symbol='QQQ',
            timeframe='5min',
            days_back=2
        )

        if len(df) > 0:
            print(f"✅ API connection successful!")
            print(f"   Data points received: {len(df)}")
            print(f"   Date range: {df['date'].min()} to {df['date'].max()}")
            print(f"   Latest price: ${df['close'].iloc[-1]:.2f}")
            return True
        else:
            print("❌ No data received from API")
            return False

    except Exception as e:
        print(f"❌ API test failed: {e}")
        return False

def test_environment_variables():
    """Test environment variable loading"""
    print("\n🌍 Testing Environment Variable Loading")
    print("=" * 45)

    # Test direct environment access
    api_key = os.getenv('POLYGON_API_KEY')
    if api_key:
        print("✅ Environment variable loaded successfully")
        print(f"   Key length: {len(api_key)} characters")
    else:
        print("❌ Environment variable not loaded")

    # Test .env file existence
    if os.path.exists('.env'):
        print("✅ .env file exists")

        # Read .env file content
        with open('.env', 'r') as f:
            content = f.read()
            if 'POLYGON_API_KEY=' in content:
                print("✅ POLYGON_API_KEY found in .env file")
            else:
                print("❌ POLYGON_API_KEY not found in .env file")
    else:
        print("❌ .env file not found")

def main():
    """Main test function"""
    print("🚀 API Key Test Suite")
    print("=" * 50)

    # Test environment variables
    test_environment_variables()

    # Test API key functionality
    success = test_api_key()

    print("\n📋 Test Summary")
    print("=" * 30)

    if success:
        print("✅ All tests passed!")
        print("🎯 Your API key is working correctly")
        print("📊 You can now use real market data in the Signal Codifier")
    else:
        print("❌ Tests failed!")
        print("🔧 Please check your API key configuration")
        print("💡 Make sure:")
        print("   - POLYGON_API_KEY is set in .env file")
        print("   - The API key is valid and active")
        print("   - You have internet connection")

if __name__ == "__main__":
    main()