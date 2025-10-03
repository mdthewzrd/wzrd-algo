# 🚀 WZRD-Algo-Mini: Complete Trading Strategy System

[![Strategy Generation](https://img.shields.io/badge/Strategy-Generation-blue)](apps/signal_codifier.py)
[![Chart Visualization](https://img.shields.io/badge/Chart-Visualization-green)](apps/strategy_viewer_enhanced.py)
[![GPT Integration](https://img.shields.io/badge/GPT-Integration-purple)](docs/GPT_COMPLETE_INSTRUCTIONS.md)

> **Complete trading strategy development workflow**: Natural Language → JSON Strategy → Interactive Charts

## 🎯 What This System Does

**WZRD-Algo-Mini** converts natural language trading strategy descriptions into structured JSON artifacts that generate interactive charts with backtested signals.

### Core Workflow
```
Natural Language → Signal Codifier → JSON Strategy → Strategy Viewer → Interactive Charts
```

## 📁 Project Structure

```
wzrd-algo-mini/
├── 🖥️  apps/                    # Main Applications
│   ├── signal_codifier.py       # Strategy → JSON converter
│   ├── strategy_viewer_enhanced.py # Advanced charting
│   └── strategy_viewer_simple.py   # Basic charts
├── 📚 docs/                     # Complete Documentation
├── 📊 strategies/               # Strategy JSON Files
├── 🧪 tests/                    # Test Files & Examples
├── 🔧 utils/                    # Core Engine
└── 🔄 workflows/               # Automation Scripts
```

## ⚡ Quick Start (2 Minutes)

### 1. Start Services
```bash
# Signal Codifier (Port 8502)
streamlit run apps/signal_codifier.py --server.port 8502

# Strategy Viewer (Port 8510)
streamlit run apps/strategy_viewer_enhanced.py --server.port 8510
```

### 2. Test System
1. **Strategy Viewer**: http://localhost:8510
2. Load: `strategies/corrected_ema_strategy.json`
3. See interactive chart with zoom controls! 🎉

## 🎨 Key Features

### 📊 Advanced Charting
- **Multi-Panel Layout**: Price + Volume + RSI
- **Professional Zoom**: Horizontal & vertical scaling
- **Time Controls**: 1-30 days, multiple frequencies
- **Signal Markers**: Clear entry/exit visualization

### 🕐 Smart Time Filtering
- **Entry Signals**: Only 8:00am - 1:00pm EST
- **Direction Confirmation**: 1hr EMA trend required
- **Market Hours**: Automatic 9:30am-4:00pm filtering

### 🤖 GPT Integration Ready
- **Complete Documentation**: Training materials included
- **JSON Schema**: Validated strategy format
- **Example Strategies**: Working templates provided

## 🔧 Configuration

### Required Environment Variables
```bash
# .env file
POLYGON_API_KEY=Fm7brz4s23eSocDErnL68cE7wspz2K1I
```

### Service Ports
| Service | Port | Purpose |
|---------|------|---------|
| Signal Codifier | 8502 | Strategy → JSON conversion |
| Strategy Viewer Enhanced | 8510 | Advanced charts & zoom |
| Strategy Viewer Simple | 8509 | Basic chart display |

## 📋 Strategy Rules

### Time Filtering
- ✅ **Entry signals**: 8:00am - 1:00pm EST only
- ✅ **Exit signals**: Any market hours
- ✅ **Validation**: Automatic time compliance checking

### JSON Format
```json
{
  "strategy_name": "Strategy_Name",
  "description": "Strategy description",
  "timeframe": "5min",
  "symbol": "QQQ",
  "signals": [
    {
      "type": "entry_signal",
      "timestamp": "2024-10-01 09:30:00",
      "price": 450.00,
      "shares": 100,
      "reason": "Entry reason",
      "direction": "long"
    }
  ],
  "entry_conditions": [...],
  "exit_conditions": [...]
}
```

## 🎯 Working Examples

### Test Strategies (Ready to Use)
- `strategies/corrected_ema_strategy.json` - EMA 9/20 crossover ✅
- `strategies/test_strategy_with_signals.json` - Simple test case ✅
- `strategies/enhanced_ema_9_20_crossover_codified.json` - Full example ✅

### GPT Prompt Examples
```
"Create a QQQ strategy that buys when the 9 EMA crosses above the 20 EMA on 5-minute charts. Only enter trades between 8am and 1pm EST. Exit when the EMAs cross back down."

"I want a momentum strategy for SPY that buys when price breaks above the 20-period high with volume confirmation. Only morning entries."
```

## 📚 Documentation

### Core Guides
- 📖 [**Quick Start Guide**](docs/QUICK_START_GUIDE.md) - 5-minute setup
- 🏗️ [**Complete System Guide**](docs/WZRD_COMPLETE_SYSTEM_GUIDE.md) - Full architecture
- 📋 [**JSON Strategy Format**](docs/JSON_STRATEGY_FORMAT.md) - Schema specification
- 🤖 [**GPT Instructions**](docs/GPT_COMPLETE_INSTRUCTIONS.md) - Training materials

### Development
- 🧪 [Test Files](tests/) - Examples and validation
- 🔧 [Utilities](utils/) - Core engines and tools
- 📊 [Strategy Examples](strategies/) - Working strategy files

## 🚀 Advanced Features

### Chart Controls
- **Drag to Zoom**: Select time/price ranges
- **Double-click Reset**: Return to full view
- **Hover Crosshairs**: Precise value display
- **Time Range**: Adjustable 1-30 days
- **Frequency**: 1min, 5min, 15min, 1hr

### Signal Analysis
- **Entry Validation**: 8am-1pm EST compliance
- **P&L Tracking**: Automatic profit/loss calculation
- **Performance Metrics**: Win rate, profit factor
- **Direction Filtering**: 1hr trend confirmation

## 🛠️ Development

### Project Dependencies
```bash
pip install streamlit pandas plotly numpy python-dotenv pytz
```

### Service Management
```bash
# Check running services
lsof -i :8502 -i :8510

# Kill all services
pkill -f streamlit

# Restart with fresh environment
streamlit run apps/signal_codifier.py --server.port 8502
```

## 🎓 GPT Integration

### Training Your Custom GPT
1. Use `docs/GPT_COMPLETE_INSTRUCTIONS.md` as knowledge base
2. Include `docs/JSON_STRATEGY_FORMAT.md` for schema reference
3. Add example strategies from `strategies/` folder
4. Test with provided example prompts

### Validation Checklist
- [ ] Entry signals only 8am-1pm EST
- [ ] Valid JSON structure
- [ ] Realistic prices for symbol
- [ ] Complete entry/exit pairs
- [ ] Proper timestamp format: "YYYY-MM-DD HH:MM:SS"

## 🐛 Troubleshooting

### Common Issues
- **Blank Charts**: Check JSON format and signal timestamps
- **Service Errors**: Verify ports 8502/8510 are available
- **Missing Files**: Run from wzrd-algo-mini root directory
- **API Issues**: Check POLYGON_API_KEY in .env file

### Quick Fixes
```bash
# Reset services
pkill -f streamlit
streamlit run apps/strategy_viewer_enhanced.py --server.port 8510

# Validate JSON
python -m json.tool strategies/your_strategy.json

# Check file organization
ls apps/ docs/ strategies/ utils/
```

## 🎉 Success Indicators

Your system works when:
- ✅ Services start on ports 8502 and 8510
- ✅ Example strategies load and display charts
- ✅ Zoom controls work smoothly
- ✅ Entry signals only show 8am-1pm
- ✅ GPT generates compliant JSON strategies

## 📞 Support

- 📖 **Documentation**: `/docs/` folder has complete guides
- 🧪 **Examples**: `/strategies/` folder has working examples
- 🔧 **Issues**: Check troubleshooting section above

---

**Ready to create professional trading strategies with AI assistance!** 🚀

Start with the [Quick Start Guide](docs/QUICK_START_GUIDE.md) for a 5-minute setup.