# 🚀 WZRD-Algo-Mini Complete System Guide

## 📁 Project Structure

```
wzrd-algo-mini/
├── apps/                          # Main Streamlit Applications
│   ├── signal_codifier.py         # Convert strategy descriptions → JSON
│   ├── strategy_viewer_enhanced.py # Advanced charts with zoom
│   ├── strategy_viewer_simple.py  # Basic chart viewer
│   └── strategy_viewer.py         # Original viewer
├── docs/                          # All Documentation
├── strategies/                    # Strategy JSON Files
├── tests/                        # Test Files & Examples
├── utils/                        # Core Engine Files
│   ├── signal_generator.py       # Signal generation engine (with MTF support)
│   ├── mtf_engine.py            # Multi-TimeFrame (MTF) engine
│   ├── chart_templates.py        # Chart creation utilities
│   └── data_integration.py       # Data fetching & processing
├── workflows/                    # Workflow automation
└── .env                          # API Keys & Configuration
```

## 🔄 Complete Workflow

### Phase 1: Strategy Description → JSON Conversion
**Tool:** Signal Codifier (Port 8502)
**Input:** Natural language strategy description
**Output:** Structured JSON strategy artifact

### Phase 2: JSON Validation & Visualization
**Tool:** Strategy Viewer Enhanced (Port 8510)
**Input:** Strategy JSON from Phase 1
**Output:** Interactive charts with signals

### Phase 3: Signal Generation & Backtesting
**Tool:** Signal Generator (utils/signal_generator.py)
**Input:** Strategy JSON + Market Data
**Output:** Trading signals with timestamps

## 🎯 Service Architecture

| Service | Port | Purpose | Status Check |
|---------|------|---------|--------------|
| **Signal Codifier** | 8502 | Strategy → JSON conversion | http://localhost:8502 |
| **Strategy Viewer Enhanced** | 8510 | Advanced charts & zoom | http://localhost:8510 |
| **Strategy Viewer Simple** | 8509 | Basic chart display | http://localhost:8509 |

## 🚀 Quick Start Commands

```bash
# Start Signal Codifier
streamlit run apps/signal_codifier.py --server.port 8502

# Start Enhanced Strategy Viewer
streamlit run apps/strategy_viewer_enhanced.py --server.port 8510

# Start Simple Strategy Viewer
streamlit run apps/strategy_viewer_simple.py --server.port 8509
```

## 📋 Strategy Rules Implementation

### Time Filtering Rules
- **Entry Signals**: Only between 8:00am - 1:00pm EST
- **Exit Signals**: Any time during market hours
- **Market Hours**: 9:30am - 4:00pm EST, weekdays only

### Multi-TimeFrame (MTF) Rules
- **5min Timeframe**: Primary signal generation (EMA crossovers)
- **1hr Timeframe**: Direction filter (trend confirmation) - MANDATORY
- **1D Timeframe**: Daily gate confirmation (optional)
- **Entry Logic**: 5min signal + 1hr trend alignment required
- **MTF Token Support**: `EMA9_1h`, `previous_EMA9_1h`, `DevBand72_1h_Lower_6`

### Signal Types
- **entry_signal**: Long position initiation
- **exit_signal**: Position closure with P&L calculation
- **direction**: "long", "short", "close_long", "close_short"

## 🔧 Configuration

### Required Environment Variables
```bash
POLYGON_API_KEY=your_polygon_api_key_here
```

### Default Settings
- **Base Ticker**: QQQ (Nasdaq ETF)
- **Primary Timeframe**: 5min
- **Confirmation Timeframe**: 1hr
- **Chart Days**: 7 days default, 1-30 adjustable
- **Data Frequency**: 5min default, supports 1min/5min/15min/1hr

## 📊 Chart Features

### Enhanced Viewer Capabilities
- **Multi-Panel Layout**: Price + Volume + RSI
- **Advanced Zoom**: Horizontal & vertical scaling
- **Time Controls**: Adjustable days & frequency
- **Signal Markers**: Lime entries, red exits
- **Hover Details**: Time, price, reason, P&L

### Chart Controls
- **Drag**: Zoom into time/price ranges
- **Double-click**: Reset to full view
- **Hover**: Crosshair guides with values

## 🎨 Strategy JSON Schema

Complete format specification in next section...

## 🤖 GPT Integration Points

### Primary Interaction Flow
1. **User Input** → Strategy description in natural language
2. **GPT Processing** → Convert to structured JSON format
3. **System Validation** → Check JSON against schema
4. **Chart Generation** → Visual strategy representation
5. **Signal Testing** → Backtest with historical data

### GPT Responsibilities
- Parse natural language strategy descriptions
- Generate compliant JSON strategy artifacts
- Include proper time filtering and direction rules
- Validate technical indicator parameters
- Provide clear strategy names and descriptions

## 📈 Performance Metrics

### Tracked Metrics
- **Total Trades**: Entry/exit signal pairs
- **Win Rate**: Percentage of profitable trades
- **Total P&L**: Cumulative profit/loss
- **Profit Factor**: Gross profit / gross loss
- **Entry Time Distribution**: 8am-1pm filter compliance

### Display Format
```json
"performance_metrics": {
  "total_trades": 3,
  "win_rate": 1.0,
  "total_pnl": 630.0,
  "profit_factor": 3.2
}
```

## 🔍 Testing & Validation

### Test Strategy Files
- `strategies/corrected_ema_strategy.json` - Working EMA crossover
- `strategies/test_strategy_with_signals.json` - Sample signals
- `tests/` - All test files and examples

### Validation Checklist
- ✅ Entry signals only 8am-1pm EST
- ✅ 1hr EMA direction confirmation
- ✅ Valid timestamp formats
- ✅ Proper JSON structure
- ✅ Chart display functionality

## 📚 Advanced Features

### Signal Generation Engine
- **Multi-TimeFrame Support**: 5min, 1h, 1D with proper time alignment
- **MTF Indicators**: EMAs, deviation bands with previous_ semantics
- **Real-time Calculations**: EMA calculations across timeframes
- **Timezone-aware Processing**: America/New_York with DST handling
- **Position Sizing**: Algorithms with risk management
- **Automatic MTF Detection**: Switches to MTF engine when needed

### Data Integration
- Polygon.io API connectivity
- Multiple timeframe support
- Market hours filtering
- Holiday calendar awareness

## 🐛 Common Issues & Solutions

### Chart Display Problems
- **Issue**: Blank/black charts
- **Solution**: Check JSON format, validate signals array

### Time Filtering Problems
- **Issue**: Signals outside 8am-1pm showing
- **Solution**: Verify timestamp timezone (EST/UTC)

### API Connection Issues
- **Issue**: No data loading
- **Solution**: Check POLYGON_API_KEY in .env file

## 🎯 Multi-TimeFrame (MTF) Integration

### MTF Strategy Examples

#### Golden Baseline Strategy (VALIDATED)
```json
{
  "strategy_name": "Golden_Baseline_SPY_EMA9x20_1hConfirm",
  "description": "SPY EMA 9/20 crossover with 1hr confirmation and 8am-1pm entries",
  "timeframe": "5min",
  "symbol": "SPY",
  "signals": [
    {
      "type": "entry_signal",
      "timestamp": "2024-10-01 09:30:00",
      "price": 548.50,
      "shares": 100,
      "reason": "EMA 9 crossed above EMA 20 on 5min with 1hr bullish confirmation",
      "direction": "long"
    },
    {
      "type": "exit_signal",
      "timestamp": "2024-10-01 14:30:00",
      "price": 551.00,
      "shares": 100,
      "reason": "EMA 9 crossed below EMA 20 on 5min",
      "direction": "close_long",
      "pnl": 250.0
    }
  ],
  "entry_conditions": [{
    "type": "ema_crossover_with_mtf_confirmation",
    "description": "EMA 9 crosses above EMA 20 on 5min AND 1hr EMA trend bullish",
    "direction": "long",
    "condition": "EMA9_5min > EMA20_5min AND previous_EMA9_5min <= previous_EMA20_5min AND EMA9_1h > EMA20_1h",
    "time_filter": {"start": "08:00", "end": "13:00", "timezone": "America/New_York"}
  }],
  "exit_conditions": [{
    "type": "ema_crossover_exit",
    "description": "EMA 9 crosses below EMA 20 on 5min",
    "direction": "close_long",
    "condition": "EMA9_5min < EMA20_5min"
  }]
}
```

#### Route Start/End Strategy with Deviation Bands (VALIDATED)
```json
{
  "strategy_name": "SPY_RouteStart_DevBands",
  "description": "SPY EMA crossover with deviation band route start and 1hr confirmation",
  "timeframe": "5min",
  "symbol": "SPY",
  "signals": [
    {
      "type": "entry_signal",
      "timestamp": "2024-10-01 10:15:00",
      "price": 548.75,
      "shares": 100,
      "reason": "EMA crossover with 1hr confirmation and deviation band route start",
      "direction": "long"
    },
    {
      "type": "exit_signal",
      "timestamp": "2024-10-01 12:45:00",
      "price": 555.50,
      "shares": 100,
      "reason": "Price reached upper deviation band",
      "direction": "close_long",
      "pnl": 675.0
    }
  ],
  "entry_conditions": [{
    "type": "ema_crossover_with_route_start",
    "description": "EMA crossover with 1hr confirmation and deviation band touch",
    "direction": "long",
    "condition": "EMA9_5min > EMA20_5min AND previous_EMA9_5min <= previous_EMA20_5min AND EMA9_1h > EMA20_1h AND Low_1h <= DevBand72_1h_Lower_6",
    "time_filter": {"start": "08:00", "end": "13:00", "timezone": "America/New_York"}
  }],
  "exit_conditions": [{
    "type": "deviation_band_exit",
    "description": "Price reaches upper deviation band",
    "direction": "close_long",
    "condition": "High_1h >= DevBand72_1h_Upper_6"
  }]
}
```

### MTF Token Reference
- **EMAs**: `EMA9_5min`, `EMA20_1h`, `previous_EMA9_1h`
- **Price Data**: `Close_1h`, `High_1h`, `Low_1h`, `previous_Close_1h`
- **Deviation Bands**: `DevBand72_1h_Lower_6`, `DevBand89_1h_Upper_6`
- **Timeframe Aliases**: `1h`/`1hr`/`60min`, `1D`/`1d`/`daily`

### MTF Testing Framework

Run comprehensive phased testing:
```bash
python tests/phased_testing_framework.py
```

**Test Coverage:**
- ✅ Phase 1: Basic data aggregation
- ✅ Phase 2: EMA and deviation band calculations
- ✅ Phase 3: Time filtering validation
- ✅ Phase 4: MTF condition evaluation
- ✅ Phase 5: MTF detection logic

## 🎓 Training Examples

See `docs/GPT_TRAINING_EXAMPLES.md` for complete examples...