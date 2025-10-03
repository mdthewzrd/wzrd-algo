# 🎯 WZRD Algo Mini - Streamlined Strategy Development System

Complete workflow for developing, testing, and verifying trading strategies with GPT-generated signals.

## 🚀 Core Workflow

**Your Streamlined Development Loop:**
```
🌐 Web Chat → 🎯 Signal Codifier → 📊 Strategy Viewer → 🔄 Iterate
```

### Three Core Components

1. **Signal Codifier** (`signal_codifier.py`) - Convert strategy JSON to code-true signals
2. **Strategy Viewer** (`strategy_viewer.py`) - Visual verification of signals
3. **Launch Script** (`launch_workflow.py`) - Easy system startup

## 🎯 Features

### 🔥 Signal Codifier (localhost:8502)
- **Code-True Signal Generation** - Computed by rules engine, not manual entry
- **Perfect VectorBT Compatibility** - Ensures backtesting accuracy
- **Real Market Data Integration** - Uses Polygon API for realistic signals
- **Pyramiding Support** - Multi-leg position building
- **Performance Metrics** - Win rate, P&L, expectancy calculations
- **Provenance Tracking** - Complete audit trail for all signals

### 📊 Strategy Viewer (localhost:8501)
- **Visual Signal Verification** - See signals overlaid on real charts
- **Performance Analytics** - Trade statistics and metrics
- **Multiple Input Methods** - Paste JSON, load examples, or existing files
- **Professional Charting** - Real-time market data with technical indicators
- **Signal History Table** - Detailed execution and calculation breakdown

### 🚀 Quick Start

**Launch Both Apps:**
```bash
python launch_workflow.py
```

**Manual Launch:**
```bash
# Terminal 1 - Signal Codifier
streamlit run signal_codifier.py --server.port 8502

# Terminal 2 - Strategy Viewer
streamlit run strategy_viewer.py --server.port 8501
```

## 🛠️ Installation

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Set up API key (optional for real data):**
```bash
export POLYGON_API_KEY="your_api_key_here"
```

## 🎯 Usage Guide

### Step 1: Web Chat Strategy Development
Start with your custom GPT to develop strategy ideas and get initial JSON specifications.

### Step 2: Signal Codifier (localhost:8502)
1. Paste your strategy JSON
2. Configure options (real data vs mock, timeframe, etc.)
3. Click "Generate Code-True Signals"
4. Copy the output JSON artifact

### Step 3: Strategy Viewer (localhost:8501)
1. Paste the codified JSON artifact
2. Verify signals visually on the chart
3. Review performance metrics
4. Check signal execution details

### Step 4: Iterate
- Go back to web chat with feedback
- Refine strategy based on visual verification
- Repeat until satisfied

## 📊 Strategy Features

### Supported Strategy Types
- **Multi-timeframe Analysis** - HTF, MTF, LTF alignment
- **Pyramiding** - Multi-leg position building
- **Quality Filters** - A+, B+ setup grading
- **Advanced Risk Management** - Dynamic stops, scaling exits
- **Trade Invalidators** - Pre-trade and in-trade filters

### Technical Indicators
- **Moving Averages**: EMA 9/20/50/200
- **Volume Weighted**: VWAP, VWAP bands
- **Momentum**: RSI, Stochastic, MACD
- **Volatility**: ATR-based stops and sizing
- **Support/Resistance**: Key level detection

### Performance Metrics
- Win Rate & Profit Factor
- Expectancy per R
- Max Drawdown analysis
- Average Win/Loss ratios
- Total P&L tracking

## 🔧 Configuration

### API Key Setup
```bash
export POLYGON_API_KEY="your_api_key_here"
```

### Custom Ports
```bash
# Signal Codifier on port 8503
streamlit run signal_codifier.py --server.port 8503

# Strategy Viewer on port 8504
streamlit run strategy_viewer.py --server.port 8504
```

## 🔧 Troubleshooting

**Signal Codifier Issues:**
- "No signals generated" - Check strategy conditions are realistic
- "API error" - Use mock data option if API key unavailable
- "JSON error" - Validate JSON format before pasting

**Strategy Viewer Issues:**
- "Chart not displaying" - Check symbol and timeframe are valid
- "No data available" - Verify Polygon API key or use mock data
- "Signals not visible" - Ensure signal dates are within data range

**General Issues:**
- **Port conflicts** - Use custom ports with `--server.port`
- **Dependencies** - Run `pip install -r requirements.txt`
- **Cache issues** - Clear with `streamlit cache clear`

## 🚀 Next Steps

Once you're satisfied with your strategy:
1. **Export to VectorBT** - Use the codified JSON for backtesting
2. **Live Testing** - Paper trade with real-time signals
3. **Strategy Optimization** - Refine based on performance metrics
4. **Production Deployment** - Implement in live trading system

---

**Version**: 2.0 - Streamlined Workflow
**Last Updated**: October 1, 2025
**Status**: Production Ready ✅

## 🎯 Your Complete Workflow

```
Web Chat → Signal Codifier → Strategy Viewer → VectorBT
```

**Remember**: This system ensures **code-true signals** for perfect backtesting accuracy!