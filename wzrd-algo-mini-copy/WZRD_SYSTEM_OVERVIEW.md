# WZRD-Algo-Mini System Overview

## 🎯 Complete Trading Strategy Ecosystem

The WZRD-Algo-Mini system provides a complete workflow for creating, validating, and visualizing trading strategies with professional-grade chart integration.

## 🔄 Complete Workflow

### 1. **Strategy Creation**
- **Custom GPT** generates strategy JSON with MTF analysis
- **Current timestamps** (2024-10-02+) in EST timezone
- **Realistic prices**: SPY $570-580, QQQ $485-495, IWM $220-240

### 2. **Signal Validation**
- **Signal Codifier** (port 8502) validates JSON format
- Ensures proper MTF tokens and conditions
- Verifies time filters and PnL calculations

### 3. **Chart Visualization**
- **WZRD Strategy Signals Viewer** (port 8520) displays signals
- Exact WZRD chart styling from professional viewer (port 8505)
- Smart signal matching to live market data timestamps

### 4. **Professional Charts**
- **WZRD Mini Chart Viewer** (port 8505) - Reference standard
- Real Polygon API data with indicators
- After-hours shading, EMA clouds, deviation bands

## 📊 Signal Visualization

### Signal Colors & Symbols
- **Long Entry**: 🟢 Green triangle up
- **Long Exit**: 🔴 Red triangle down
- **Short Entry**: 🔴 Red triangle down
- **Short Exit**: 🟢 Green triangle up

### Visual Specifications
- **Size**: 16px triangles
- **Outline**: Thin black border (1px)
- **Colors**: Bright green (#00FF00), bright red (#FF3333)
- **Positioning**: Exact timestamp matching with market data

## 🎛️ System Ports

| Port | Application | Purpose |
|------|-------------|---------|
| 8502 | Signal Codifier | Validate strategy JSON |
| 8505 | WZRD Mini Chart Viewer | Professional chart reference |
| 8520 | WZRD Strategy Signals | Visualize signals on charts |

## 📋 Strategy JSON Requirements

### Mandatory Fields
```json
{
  "strategy_name": "Strategy_Name",
  "timeframe": "5min",
  "symbol": "SPY",
  "signals": [
    {
      "type": "entry_signal",
      "timestamp": "2024-10-02 09:30:00",
      "price": 572.00,
      "shares": 100,
      "reason": "EMA crossover with 1hr confirmation",
      "direction": "long"
    },
    {
      "type": "exit_signal",
      "timestamp": "2024-10-02 14:30:00",
      "price": 575.00,
      "shares": 100,
      "reason": "EMA crossunder",
      "direction": "close_long",
      "pnl": 300.0
    }
  ],
  "entry_conditions": [...],
  "exit_conditions": [...]
}
```

### Critical Rules
- ✅ **Entry signals**: 8:00am-1:00pm EST only
- ✅ **Timestamps**: Current dates (2024-10-02+) in EST
- ✅ **1hr EMA confirmation**: Required for ALL entries
- ✅ **PnL field**: Required for ALL exit signals
- ✅ **MTF tokens**: Use proper multi-timeframe syntax

## 🔧 MTF Token System

### EMAs
- `EMA9_5min`, `EMA20_5min` - Base timeframe
- `EMA9_1h`, `EMA20_1h` - 1hr confirmation
- `EMA9_1D`, `EMA20_1D` - Daily gate
- `previous_EMA9_5min`, `previous_EMA20_5min` - Crossover detection

### Price Data
- `Close_1h`, `High_1h`, `Low_1h` - 1hr price levels
- `previous_Close_1h` - Previous hour close

### Deviation Bands
- `DevBand72_1h_Lower_6`, `DevBand72_1h_Upper_6` - Route start/end
- `DevBand89_1h_Lower_6`, `DevBand89_1h_Upper_6` - Alternative levels

## 📈 Example Conditions

### Basic MTF Entry
```
EMA9_5min > EMA20_5min AND previous_EMA9_5min <= previous_EMA20_5min AND EMA9_1h > EMA20_1h
```

### Route Start Entry
```
EMA9_5min > EMA20_5min AND previous_EMA9_5min <= previous_EMA20_5min AND EMA9_1h > EMA20_1h AND Low_1h <= DevBand72_1h_Lower_6
```

### Daily Gate Entry
```
EMA9_5min > EMA20_5min AND previous_EMA9_5min <= previous_EMA20_5min AND EMA9_1h > EMA20_1h AND EMA9_1D > EMA20_1D
```

### Route End Exit
```
High_1h >= DevBand72_1h_Upper_6
```

## 🚀 Quick Start Guide

1. **Generate Strategy** using Custom GPT with current timestamps
2. **Validate JSON** in Signal Codifier (port 8502)
3. **Copy validated JSON** to Strategy Signals Viewer (port 8520)
4. **View signals** on professional WZRD charts
5. **Verify positioning** and signal accuracy

## ✅ Quality Checklist

### Before Submission
- [ ] Entry signals within 8:00am-1:00pm EST window
- [ ] Current timestamps (2024-10-02 or later)
- [ ] 1hr EMA confirmation in all entry conditions
- [ ] PnL calculated for all exit signals
- [ ] Realistic current market prices
- [ ] Complete time_filter objects
- [ ] Proper MTF token usage

### After Visualization
- [ ] Signals appear on chart at correct timestamps
- [ ] Green/red triangles match trade direction
- [ ] Signal tooltips show correct information
- [ ] No timezone errors or matching warnings
- [ ] Professional chart styling maintained

## 🎨 Visual Integration

The WZRD Strategy Signals Viewer seamlessly integrates with the professional WZRD chart ecosystem:

- **Identical chart engine** as port 8505 reference viewer
- **Real market data** from Polygon API
- **Professional indicators** - VWAP, EMA clouds, deviation bands
- **After-hours shading** for proper time context
- **Responsive controls** for timeframe and indicator toggles
- **Signal overlay system** with smart timestamp matching

This creates a complete professional trading strategy development and visualization environment.