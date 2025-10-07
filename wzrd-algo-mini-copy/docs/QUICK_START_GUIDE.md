# 🚀 WZRD-Algo-Mini Quick Start Guide

## ⚡ 5-Minute Setup

### 1. Start the Services
```bash
# Terminal 1: Signal Codifier (Strategy → JSON)
streamlit run apps/signal_codifier.py --server.port 8502

# Terminal 2: Enhanced Strategy Viewer (JSON → Charts)
streamlit run apps/strategy_viewer_enhanced.py --server.port 8510
```

### 2. Open Browser
- **Signal Codifier**: http://localhost:8502
- **Strategy Viewer**: http://localhost:8510

### 3. Test with Example Strategy
- Go to Strategy Viewer (8510)
- Choose "Load Existing File"
- Select `corrected_ema_strategy.json`
- Click "Load File"
- View the interactive chart!

## 🎯 Complete Workflow Test

### Step 1: Create Strategy (Signal Codifier - Port 8502)
1. Enter strategy description:
   ```
   Create a QQQ strategy that buys when the 9 EMA crosses above the 20 EMA on 5-minute charts. Only enter trades between 8am and 1pm EST. Exit when the EMAs cross back down. Include 1-hour EMA trend confirmation.
   ```
2. Click "Generate Strategy JSON"
3. Copy the generated JSON

### Step 2: Visualize Strategy (Strategy Viewer - Port 8510)
1. Switch to Strategy Viewer
2. Choose "Paste JSON"
3. Paste the JSON from Step 1
4. Adjust chart settings:
   - **Days to Display**: 7 days
   - **Data Frequency**: 5min
   - **Chart Layout**: Detailed (Price + Volume + RSI)
5. View interactive chart with zoom controls

## 📊 Chart Features Test

### Zoom Controls
- **Drag**: Select area to zoom
- **Double-click**: Reset to full view
- **Hover**: See crosshair with values

### Time Controls
- **Days Slider**: 1-30 days of data
- **Frequency**: 1min, 5min, 15min, 1H

### Signal Display
- **Green Triangles**: Entry signals (8am-1pm only)
- **Red Triangles**: Exit signals (any time)
- **Hover Info**: Time, price, reason, P&L

## 🔧 Configuration Check

### Environment Variables
```bash
# Check if API key is set
echo $POLYGON_API_KEY

# Should show: Fm7brz4s23eSocDErnL68cE7wspz2K1I
```

### Service Status
```bash
# Check running services
lsof -i :8502 -i :8510

# Should show Python processes on both ports
```

## 📋 Working Example Strategies

### Available Test Files
- `strategies/corrected_ema_strategy.json` - ✅ Working EMA crossover
- `strategies/test_strategy_with_signals.json` - ✅ Simple test strategy
- `strategies/enhanced_ema_9_20_crossover_codified.json` - ✅ Full example

### Key Features Demonstrated
- ✅ Entry signals only 8am-1pm EST
- ✅ 1hr EMA direction confirmation
- ✅ Proper P&L calculations
- ✅ Interactive chart display
- ✅ Zoom and time controls

## 🚨 Troubleshooting

### Chart Not Displaying
1. Check JSON format - paste into JSONLint.com
2. Verify signal timestamps are recent (last 30 days)
3. Ensure entry signals are 8am-1pm EST

### Services Not Starting
```bash
# Kill existing processes
pkill -f streamlit

# Restart services
streamlit run apps/signal_codifier.py --server.port 8502
streamlit run apps/strategy_viewer_enhanced.py --server.port 8510
```

### Missing Files
If strategy files are missing:
```bash
# Check if files were moved correctly
ls strategies/
ls apps/
ls utils/

# Should show organized structure
```

## 🎯 GPT Integration Test

### Test Custom GPT
1. Go to your Custom GPT
2. Ask: "Create a momentum breakout strategy for SPY that buys when price breaks above the 20-period high with volume confirmation. Only enter trades between 8am and 1pm."
3. Copy the JSON response
4. Paste into Strategy Viewer (port 8510)
5. Verify chart displays correctly

### Validation Checklist
- [ ] Entry signals only 8am-1pm EST
- [ ] Valid JSON structure
- [ ] Realistic prices for symbol
- [ ] Complete entry/exit pairs
- [ ] Proper timestamp format
- [ ] Chart displays signals correctly

## 📚 Next Steps

### System Documentation
- `docs/WZRD_COMPLETE_SYSTEM_GUIDE.md` - Complete system overview
- `docs/JSON_STRATEGY_FORMAT.md` - JSON schema specification
- `docs/GPT_COMPLETE_INSTRUCTIONS.md` - GPT training materials

### Advanced Features
- Custom indicators and timeframes
- Multi-symbol strategies
- Risk management integration
- Real-time signal generation

## 🎉 Success Indicators

Your system is working correctly when:
- ✅ Both services start without errors
- ✅ Example strategies load and display charts
- ✅ Zoom controls work smoothly
- ✅ Signals show only during 8am-1pm for entries
- ✅ GPT generates valid JSON strategies
- ✅ All timestamps and P&L calculations are correct

Ready to create and test trading strategies! 🚀