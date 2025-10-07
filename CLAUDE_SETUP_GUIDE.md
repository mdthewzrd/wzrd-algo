# Claude Anthropic API Setup Guide

This guide will help you switch from GLM 4.5 to Claude Anthropic API for your wzrd-algo project.

## What Changed

✅ **Completed Changes:**
- Created new `claude_anthropic_client.py` with direct Anthropic API integration
- Updated all import statements to use the new Claude client
- Maintained backward compatibility (existing code will work without changes)
- Created setup and test scripts for easy configuration

## Quick Setup

### Step 1: Get Your Anthropic API Key

1. Go to [Anthropic Console](https://console.anthropic.com/)
2. Sign up or log in
3. Create an API key
4. Copy the key (starts with `sk-ant-`)

### Step 2: Run the Setup Script

```bash
cd /Users/michaeldurante/wzrd-algo
python setup_claude_env.py
```

This will:
- Prompt you for your API key
- Create a `.env` file with your credentials
- Test the connection
- Confirm everything is working

### Step 3: Test the Connection

```bash
python test_claude_connection.py
```

This will verify:
- API key is properly set
- Connection to Claude works
- Trading functionality is operational

## Manual Setup (Alternative)

If you prefer to set up manually:

### 1. Set Environment Variable

**Option A: Using .env file**
```bash
echo "ANTHROPIC_API_KEY=your_api_key_here" > .env
```

**Option B: Export in shell**
```bash
export ANTHROPIC_API_KEY=your_api_key_here
```

**Option C: Add to ~/.zshrc (permanent)**
```bash
echo "export ANTHROPIC_API_KEY=your_api_key_here" >> ~/.zshrc
source ~/.zshrc
```

### 2. Test the Setup
```bash
python test_claude_connection.py
```

## What Models Are Available

The new client uses **Claude 3.5 Sonnet** by default, which is:
- More capable than GLM 4.5
- Better at code generation
- More reliable for trading analysis
- Faster response times

You can also use other Claude models by specifying the `model` parameter:
- `claude-3-5-sonnet-20241022` (default, recommended)
- `claude-3-opus-20240229` (most capable, slower)
- `claude-3-haiku-20240307` (fastest, less capable)

## Using the New Client

### Basic Usage

```python
from claude_anthropic_client import ClaudeAnthropicClient

client = ClaudeAnthropicClient()
response = client.send_message("Analyze this trading setup...")
print(response['content'][0]['text'])
```

### Trading Analysis

```python
market_data = {
    "symbol": "SPY",
    "price": 450.25,
    "rsi": 65.5
}

analysis = client.get_trading_analysis(market_data)
print(analysis)
```

### Strategy Generation

```python
strategy_desc = "RSI mean reversion strategy"
code = client.generate_strategy_code(strategy_desc)
print(code)
```

## Backward Compatibility

✅ **All existing code will work without changes!**

The new client includes a backward compatibility alias:
```python
# This still works:
from claude_glm_client import ClaudeGLMClient

# It now uses Claude Anthropic API instead of GLM 4.5
```

## Files That Were Updated

- `agents/strategy_architect_enhanced.py`
- `strategy_architect_standalone.py`
- `demo_enhanced_strategy_architect.py`
- `test_enhanced_strategy_architect.py`
- `test_pyramiding_backtest.py`
- `examples/claude_usage_examples.py`

## Running Your Trading Scripts

After setup, you can run any of these:

```bash
# Test the enhanced strategy architect
python test_enhanced_strategy_architect.py

# Run a demo
python demo_enhanced_strategy_architect.py

# Test pyramiding strategies
python test_pyramiding_backtest.py

# Run examples
python examples/claude_usage_examples.py
```

## Troubleshooting

### "API key is required" Error

Make sure your environment variable is set:
```bash
echo $ANTHROPIC_API_KEY
```

If empty, run the setup script again:
```bash
python setup_claude_env.py
```

### "Error calling Claude API" Error

1. Check your API key is valid
2. Ensure you have credits in your Anthropic account
3. Check your internet connection
4. Try the test script: `python test_claude_connection.py`

### Import Errors

If you get import errors, make sure you're in the project directory:
```bash
cd /Users/michaeldurante/wzrd-algo
python your_script.py
```

## Benefits of the Switch

🚀 **Performance:**
- Faster response times
- More reliable API
- Better uptime

🧠 **Intelligence:**
- Better code generation
- More accurate trading analysis
- Better understanding of complex strategies

💰 **Cost:**
- Competitive pricing
- Pay-per-use model
- No monthly subscriptions

🔧 **Features:**
- Latest AI capabilities
- Regular model updates
- Better tool integration

## Support

If you run into issues:

1. Run the test script: `python test_claude_connection.py`
2. Check the setup script: `python setup_claude_env.py check`
3. Verify your API key at [Anthropic Console](https://console.anthropic.com/)

---

**You're all set!** Your wzrd-algo project now uses Claude instead of GLM 4.5. 🎉
