# 🎯 Streamlined Workflow Examples

Complete usage examples for the WZRD Streamlined Workflow: **Web Chat → Signal Codifier → Strategy Viewer → VectorBT**

## 🚀 Quick Start Example

### Step 1: Create Strategy with Web Chat
```
You: I want to create a mean reversion strategy for QQQ on 5min charts that:
- Shorts when QQQ gaps up more than 1% in the morning
- Covers when price returns to VWAP
- Uses 300 share position size
- Has 1.5% stop loss
- Allows pyramiding into losing positions

GPT: [Generates complete strategy JSON]
```

### Step 2: Generate Code-True Signals
1. Go to **http://localhost:8502** (Signal Codifier)
2. Paste the GPT-generated JSON
3. Configure options:
   - Timeframe: 5min
   - Symbol: QQQ
   - Use real data (Polygon API) or mock data
4. Click "Generate Code-True Signals"
5. Copy the output codified artifact

### Step 3: Visual Verification
1. Go to **http://localhost:8501** (Strategy Viewer)
2. Paste the codified artifact
3. Verify signals on real charts
4. Check performance metrics
5. Review execution details

---

## 📊 Complete Workflow Examples

### Example 1: QQQ Morning Gap Fade

#### Strategy Specification (from Web Chat)
```json
{
  "strategy_name": "QQQ_Morning_Gap_Fade",
  "description": "Fade morning gaps in QQQ using VWAP and mean reversion",
  "timeframe": "5min",
  "symbol": "QQQ",
  "entry_conditions": [
    {
      "type": "gap_fade",
      "description": "Short when QQQ gaps up > 1% from previous close",
      "direction": "short",
      "indicators": ["vwap", "ema20", "rsi"],
      "gap_threshold": 1.0,
      "time_window": "09:30-10:30"
    }
  ],
  "exit_conditions": [
    {
      "type": "mean_reversion_target",
      "description": "Cover when price returns to VWAP",
      "direction": "cover_short"
    },
    {
      "type": "stop_loss",
      "description": "Stop loss at 1.5% below entry",
      "direction": "cover_short"
    }
  ],
  "risk_management": {
    "stop_loss": {"type": "percentage", "value": 1.5},
    "position_size": {"type": "fixed", "value": 300},
    "pyramiding": {
      "enabled": true,
      "max_legs": 3,
      "add_conditions": [
        {"level": "initial", "size": 100, "condition": "Gap > 1%"},
        {"level": "add", "size": 100, "condition": "Price extends 0.5% more"},
        {"level": "max", "size": 100, "condition": "Price extends 1% more"}
      ]
    }
  }
}
```

#### Signal Codifier Output
```json
{
  "strategy_name": "QQQ_Morning_Gap_Fade",
  "description": "Fade morning gaps in QQQ using VWAP and mean reversion",
  "timeframe": "5min",
  "symbol": "QQQ",
  "provenance": {
    "source": "signal_codifier",
    "generated_at": "2025-10-01T10:30:00Z",
    "market_data_source": "polygon",
    "computation_method": "rules_engine"
  },
  "signals": [
    {
      "timestamp": "2025-09-26 09:35:00",
      "type": "entry_short",
      "price": 594.50,
      "shares": 100,
      "reason": "Gap up 1.2% from previous close, above VWAP",
      "execution": "SOLD SHORT 100 shares @ $594.50"
    },
    {
      "timestamp": "2025-09-26 09:45:00",
      "type": "entry_short",
      "price": 595.25,
      "shares": 100,
      "reason": "Price extended 0.5% more, RSI overbought at 75",
      "execution": "SOLD SHORT 100 shares @ $595.25"
    },
    {
      "timestamp": "2025-09-26 10:15:00",
      "type": "exit_short",
      "price": 593.00,
      "shares": 200,
      "reason": "Price returned to VWAP, mean reversion complete",
      "execution": "BUY TO COVER 200 shares @ $593.00",
      "calculation": "Entry: $594.88 avg | Exit: $593.00 | Difference: $1.88 x 200 shares",
      "pnl": 376.0
    }
  ],
  "performance_metrics": {
    "total_trades": 1,
    "winning_trades": 1,
    "losing_trades": 0,
    "total_pnl": 376.0,
    "win_rate": 100.0,
    "profit_factor": null,
    "expectancy": 376.0
  }
}
```

### Example 2: Multi-Timeframe EMA Strategy

#### Strategy Specification
```json
{
  "strategy_name": "SPY_MTF_EMA_Crossover",
  "description": "Multi-timeframe EMA crossover strategy with pyramid scaling",
  "timeframe": "15min",
  "symbol": "SPY",
  "entry_conditions": [
    {
      "type": "multi_timeframe_alignment",
      "description": "HTF: Daily 50>200 EMA + MTF: 15min 9>20 EMA + LTF: 5min RSI > 50",
      "direction": "long",
      "indicators": ["ema50", "ema200", "ema9", "ema20", "rsi"],
      "htf_condition": "Daily 50EMA above 200EMA",
      "mtf_condition": "15min EMA 9 crossed above EMA 20",
      "ltf_condition": "5min RSI > 50 with momentum"
    }
  ],
  "exit_conditions": [
    {
      "type": "reversal_signal",
      "description": "Exit when EMA 9 crosses below EMA 20",
      "direction": "exit_long"
    }
  ],
  "risk_management": {
    "stop_loss": {"type": "percentage", "value": 1.0},
    "take_profit": {"type": "r_multiple", "value": 2.0},
    "position_size": {"type": "r_based", "value": 1.0},
    "pyramiding": {
      "enabled": true,
      "max_legs": 3,
      "add_conditions": [
        {"level": "initial", "size_r": 0.5, "condition": "Initial EMA crossover"},
        {"level": "confirmation", "size_r": 0.25, "condition": "Price holds above EMAs"},
        {"level": "continuation", "size_r": 0.25, "condition": "Trend continues with volume"}
      ]
    }
  }
}
```

---

## 🎯 Advanced Usage Examples

### Example 3: Complex Quality Filtering

```json
{
  "strategy_name": "QQQ_A_Plus_Setups",
  "description": "Only trade A+ quality setups with multiple confirmations",
  "timeframe": "5min",
  "symbol": "QQQ",
  "entry_conditions": [
    {
      "type": "quality_filter",
      "description": "A+ setup: RSI < 30 + Volume spike > 2x avg + Price near VWAP",
      "direction": "long",
      "indicators": ["rsi", "volume", "vwap"],
      "quality_score": "A+",
      "filters": [
        {"indicator": "rsi", "condition": "< 30"},
        {"indicator": "volume", "condition": "> 2000000"},
        {"indicator": "vwap", "condition": "within 0.3%"}
      ],
      "size_multiplier": 1.5
    }
  ],
  "exit_conditions": [
    {
      "type": "multi_target",
      "description": "Scale out at 1R and 2R targets",
      "direction": "exit_long",
      "targets": [
        {"level": "first", "r_multiple": 1.0, "size_percent": 50},
        {"level": "second", "r_multiple": 2.0, "size_percent": 50}
      ]
    }
  ],
  "risk_management": {
    "stop_loss": {"type": "atr", "value": 1.5},
    "position_size": {"type": "r_based", "value": 1.5},
    "pyramiding": {"enabled": false}
  }
}
```

---

## 🔧 Command Line Usage

### Launch the Streamlined Workflow
```bash
# Launch both apps
python launch_streamlined_workflow.py

# Manual launch
streamlit run signal_codifier.py --server.port 8502
streamlit run strategy_viewer.py --server.port 8501
```

### Test with Example Files
```bash
# Test Signal Codifier with example
# 1. Open http://localhost:8502
# 2. Load example_strategy_qqq_short_sept26.json
# 3. Generate signals
# 4. Copy output

# Test Strategy Viewer
# 1. Open http://localhost:8501
# 2. Paste the codified JSON
# 3. Verify visualization
```

---

## 🎯 Iteration Workflow

### From Strategy to Production

1. **Initial Strategy** → Web Chat development
2. **Signal Generation** → Signal Codifier processing
3. **Visual Verification** → Strategy Viewer analysis
4. **Performance Review** → Metrics and execution analysis
5. **Refinement** → Back to Web Chat with feedback
6. **Repeat** → Until performance meets expectations

### Common Iteration Patterns

#### Pattern 1: Tighten Entry Conditions
```json
// Before
"rsi_condition": "RSI < 35"

// After refinement
"rsi_condition": "RSI < 30 AND RSI diverging from price"
```

#### Pattern 2: Adjust Risk Management
```json
// Before
"stop_loss": {"type": "percentage", "value": 1.5}

// After refinement
"stop_loss": {"type": "atr", "value": 1.2, "multiplier": true}
```

#### Pattern 3: Add Quality Filters
```json
// Before
Simple entry conditions

// After refinement
Add volume confirmation, multiple timeframe alignment, market regime filter
```

---

## 📊 Performance Analysis

### Metrics to Track During Iteration

1. **Win Rate** → Should be > 55%
2. **Profit Factor** → Should be > 1.5
3. **Expectancy** → Should be positive
4. **Max Drawdown** → Should be < 10%
5. **Average Trade** → Should justify commissions

### When to Iterate

- **Win Rate < 50%** → Tighten entry conditions
- **Profit Factor < 1.3** → Adjust risk/reward ratio
- **High Drawdown** → Reduce position size or add stops
- **Low Trade Frequency** → Relax entry conditions

---

## 🚀 Next Steps After Validation

### Export to VectorBT
```python
# Use the codified JSON for backtesting
import vectorbt as vbt
import json

# Load strategy artifact
with open('codified_strategy.json', 'r') as f:
    strategy = json.load(f)

# Convert to VectorBT format
# [Implementation specific to your needs]
```

### Live Testing
1. **Paper Trading** → Test with real-time signals
2. **Position Sizing** → Adjust for account size
3. **Risk Management** → Implement real stops
4. **Performance Tracking** → Monitor live metrics

### Production Deployment
1. **Code Generation** → Convert to executable strategy
2. **Infrastructure Setup** → Deploy to trading system
3. **Monitoring** → Real-time performance tracking
4. **Optimization** → Continuous improvement

---

## 💡 Pro Tips

### Signal Codifier Tips
- Use mock data for rapid iteration
- Test different timeframes
- Validate logic with known market scenarios
- Check signal frequency and quality

### Strategy Viewer Tips
- Focus on signal timing accuracy
- Verify P&L calculations manually
- Check for overfitting in visual patterns
- Use multiple examples for robustness

### Workflow Optimization
- Keep strategies simple initially
- Add complexity incrementally
- Document iteration decisions
- Maintain performance history

---

## 🎯 Success Criteria

### Validation Checklist
- [ ] Signals appear at correct timestamps
- [ ] Arrow colors match trade direction
- [ ] P&L calculations are accurate
- [ ] Performance metrics are realistic
- [ ] Risk management rules are respected
- [ ] Multi-timeframe logic is sound
- [ ] Strategy can be implemented in VectorBT

### Production Readiness
- [ ] Consistent performance across market conditions
- [ ] Robust error handling
- [ ] Clear implementation specifications
- [ ] Comprehensive testing coverage
- [ ] Risk management is institutional-grade
- [ ] Performance meets expectations

---

*This completes the streamlined workflow examples. The system is now ready for production use with the Web Chat → Signal Codifier → Strategy Viewer → VectorBT workflow.*