# Claude GLM 4.5 API Usage Guide

## ✅ API Setup Complete

Your Claude GLM 4.5 API key is working! Here's how to use it:

## 🚀 Quick Start

```python
from claude_glm_client import ClaudeGLMClient

# Initialize client
client = ClaudeGLMClient()

# Send a message
response = client.send_message("Hello! Help me with trading analysis.")
print(response['choices'][0]['message']['content'])
```

## 📊 Available Models

- `glm-4.5` - Standard GLM 4.5 model
- `glm-4.5-air` - GLM 4.5 Air model (potentially faster/lightweight)

## 🛠️ Key Features

### 1. Basic Chat
```python
response = client.send_message(
    "What's the best trading strategy for today?",
    temperature=0.7,
    max_tokens=1000
)
```

### 2. Market Analysis
```python
market_data = {
    "symbol": "TSLA",
    "price": 250.50,
    "volume": 45000000,
    "indicators": {"rsi": 65.4, "macd": "bullish"}
}

analysis = client.get_trading_analysis(market_data)
```

### 3. Strategy Generation
```python
strategy_code = client.generate_strategy_code("""
Create a momentum-based trading strategy using RSI and MACD
""")
```

### 4. Conversational Context
```python
history = [
    {"role": "user", "content": "I'm building a trading bot"},
    {"role": "assistant", "content": "Great! What specific features do you need?"}
]

response = client.send_message(
    "Add risk management features",
    conversation_history=history
)
```

## 📝 Integration Examples

### Trading Bot Integration
```python
# In your trading bot
from claude_glm_client import ClaudeGLMClient

class TradingBot:
    def __init__(self):
        self.claude = ClaudeGLMClient()
        self.conversation_history = []

    def get_ai_advice(self, market_data):
        analysis = self.claude.get_trading_analysis(market_data)
        return analysis

    def generate_strategy(self, requirements):
        code = self.claude.generate_strategy_code(requirements)
        # Save and implement strategy
        return code
```

### Real-time Analysis
```python
def real_time_analysis(symbol, price_data):
    client = ClaudeGLMClient()

    prompt = f"""
    Analyze this real-time data for {symbol}:
    Current Price: {price_data['price']}
    Volume: {price_data['volume']}
    Technical Indicators: {price_data['indicators']}

    Should I buy, sell, or hold?
    """

    response = client.send_message(prompt)
    return response['choices'][0]['message']['content']
```

## ⚠️ Rate Limits

The API has rate limits. Be mindful of:
- Number of requests per minute
- Token usage per request
- Concurrent request limits

## 🛡️ Best Practices

1. **Error Handling**: Always wrap API calls in try-catch blocks
2. **Rate Limiting**: Implement request queuing if making multiple calls
3. **Context Management**: Use conversation history for better context
4. **Token Management**: Monitor token usage for cost optimization

## 🔧 Troubleshooting

If you encounter errors:
1. Check your API key in `.env`
2. Verify internet connection
3. Monitor rate limits
4. Check model availability with `client.get_model_info()`

## 📚 Example Files

- `claude_glm_client.py` - Main client implementation
- `examples/claude_usage_examples.py` - Usage examples
- `generated_strategies/` - Store generated strategies here

## 🎯 Next Steps

1. Test basic functionality with simple messages
2. Integrate with your trading data pipeline
3. Build automated strategy generation
4. Add real-time market analysis capabilities

Your Claude GLM 4.5 API is ready to help with your wzrd-algo trading system! 🚀