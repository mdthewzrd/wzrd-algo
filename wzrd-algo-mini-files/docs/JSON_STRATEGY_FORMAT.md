# 📋 JSON Strategy Format Specification

## 🏗️ Complete Strategy Schema

```json
{
  "strategy_name": "string",              // Required: Unique strategy identifier
  "description": "string",                // Required: Human-readable description
  "timeframe": "string",                  // Required: "1min", "5min", "15min", "1hr", "1d"
  "symbol": "string",                     // Required: Trading symbol (e.g., "QQQ", "SPY")
  "signals": [],                          // Required: Array of trading signals
  "entry_conditions": [],                 // Required: Entry rule definitions
  "exit_conditions": [],                  // Required: Exit rule definitions
  "risk_management": {},                  // Optional: Risk parameters
  "indicators": {},                       // Optional: Technical indicator definitions
  "market_conditions": {},                // Optional: Time filters and market rules
  "performance_metrics": {},              // Optional: Backtest results
  "backtest_settings": {}                 // Optional: Backtest configuration
}
```

## 🎯 Core Required Fields

### Strategy Identification
```json
{
  "strategy_name": "Enhanced_EMA_9_20_Crossover",
  "description": "EMA 9/20 crossover with time filtering (8am-1pm) and 1hr direction confirmation",
  "timeframe": "5min",
  "symbol": "QQQ"
}
```

### Signals Array (Critical for Chart Display)
```json
{
  "signals": [
    {
      "type": "entry_signal",              // Required: "entry_signal" or "exit_signal"
      "timestamp": "2024-10-01 08:15:00",  // Required: ISO format "YYYY-MM-DD HH:MM:SS"
      "price": 449.25,                     // Required: Entry/exit price
      "shares": 100,                       // Required: Position size
      "reason": "EMA 9 crossed above EMA 20 (5min) + 1hr EMA trend up", // Required
      "direction": "long",                 // Required: "long", "short", "close_long", "close_short"
      "hour_ema_direction": "bullish",     // Optional: 1hr trend confirmation
      "pnl": 255.0                         // Required for exit_signal: profit/loss
    }
  ]
}
```

## 🚨 Critical Time Filtering Rules

### Entry Signal Requirements
- **Time Range**: 8:00am - 1:00pm EST ONLY
- **Timezone**: All timestamps in EST/EDT
- **Format**: "YYYY-MM-DD HH:MM:SS" (24-hour format)
- **Validation**: Entry signals outside 8am-1pm will be filtered out

### Exit Signal Requirements
- **Time Range**: Any time during market hours
- **Required Field**: "pnl" (profit/loss calculation)
- **Market Hours**: 9:30am - 4:00pm EST, weekdays

## 📈 Entry Conditions Schema

```json
{
  "entry_conditions": [
    {
      "type": "ema_crossover_with_time_filter",
      "description": "EMA 9 crosses above EMA 20 between 8am-1pm EST",
      "direction": "long",
      "indicators": ["ema9_5min", "ema20_5min", "ema9_1hr", "ema20_1hr"],
      "condition": "EMA9_5min > EMA20_5min AND previous_EMA9_5min <= previous_EMA20_5min AND EMA9_1hr > EMA20_1hr",
      "time_filter": {
        "start": "08:00",
        "end": "13:00",
        "timezone": "US/Eastern"
      }
    }
  ]
}
```

## 🚪 Exit Conditions Schema

```json
{
  "exit_conditions": [
    {
      "type": "ema_crossover_exit",
      "description": "EMA 9 crosses below EMA 20 (no time restriction)",
      "direction": "close_long",
      "condition": "EMA9_5min < EMA20_5min"
    }
  ]
}
```

## 📊 Performance Metrics Schema

```json
{
  "performance_metrics": {
    "total_trades": 3,              // Integer: Number of complete trades
    "win_rate": 1.0,               // Float: Percentage as decimal (0.0-1.0)
    "total_pnl": 630.0,            // Float: Total profit/loss in dollars
    "profit_factor": 3.2,          // Float: Gross profit / gross loss
    "entry_time_range": "08:00-13:00 EST",     // String: Time filter description
    "directional_filter": "1hr EMA trend confirmation"  // String: Direction rule
  }
}
```

## 🔧 Optional Advanced Fields

### Risk Management
```json
{
  "risk_management": {
    "stop_loss": {
      "type": "percentage",
      "value": 2.0
    },
    "take_profit": {
      "type": "percentage",
      "value": 4.0
    },
    "position_size": {
      "type": "fixed_dollar",
      "value": 1000
    },
    "pyramiding": {
      "enabled": false
    }
  }
}
```

### Technical Indicators
```json
{
  "indicators": {
    "ema9": {
      "type": "exponential_moving_average",
      "period": 9,
      "timeframe": "5min"
    },
    "ema20": {
      "type": "exponential_moving_average",
      "period": 20,
      "timeframe": "5min"
    },
    "ema9_1hr": {
      "type": "exponential_moving_average",
      "period": 9,
      "timeframe": "1hr"
    }
  }
}
```

### Market Conditions
```json
{
  "market_conditions": {
    "time_filters": {
      "start_time": "08:00",
      "end_time": "13:00",
      "timezone": "US/Eastern"
    },
    "market_hours": {
      "start": "09:30",
      "end": "16:00",
      "timezone": "US/Eastern"
    }
  }
}
```

## 🎯 Minimal Valid Strategy Template

```json
{
  "strategy_name": "Your_Strategy_Name",
  "description": "Brief strategy description",
  "timeframe": "5min",
  "symbol": "QQQ",
  "signals": [
    {
      "type": "entry_signal",
      "timestamp": "2024-10-01 09:30:00",
      "price": 450.00,
      "shares": 100,
      "reason": "Your entry reason",
      "direction": "long"
    },
    {
      "type": "exit_signal",
      "timestamp": "2024-10-01 15:00:00",
      "price": 455.00,
      "shares": 100,
      "reason": "Your exit reason",
      "direction": "close_long",
      "pnl": 500.0
    }
  ],
  "entry_conditions": [
    {
      "type": "your_entry_logic",
      "description": "Entry condition description",
      "direction": "long"
    }
  ],
  "exit_conditions": [
    {
      "type": "your_exit_logic",
      "description": "Exit condition description",
      "direction": "close_long"
    }
  ]
}
```

## ✅ Validation Checklist

### Required Fields Check
- [ ] strategy_name (unique identifier)
- [ ] description (human readable)
- [ ] timeframe (valid timeframe string)
- [ ] symbol (trading symbol)
- [ ] signals (array with at least one signal)
- [ ] entry_conditions (array with rules)
- [ ] exit_conditions (array with rules)

### Signal Validation
- [ ] All entry signals between 8:00am-1:00pm EST
- [ ] All timestamps in "YYYY-MM-DD HH:MM:SS" format
- [ ] All signals have required fields: type, timestamp, price, shares, reason, direction
- [ ] Exit signals include "pnl" field
- [ ] Signal types are "entry_signal" or "exit_signal"
- [ ] Directions are valid: "long", "short", "close_long", "close_short"

### Chart Compatibility
- [ ] At least one signal for chart display
- [ ] Timestamps within reasonable date range (last 30 days recommended)
- [ ] Price values are realistic for chosen symbol
- [ ] Signals are chronologically ordered

## 🚨 Common Validation Errors

### Invalid Timestamps
```json
// ❌ Wrong: Missing seconds
"timestamp": "2024-10-01 09:30"

// ❌ Wrong: Invalid format
"timestamp": "10/01/2024 9:30 AM"

// ✅ Correct: Full ISO format
"timestamp": "2024-10-01 09:30:00"
```

### Invalid Entry Times
```json
// ❌ Wrong: Entry outside allowed hours
{
  "type": "entry_signal",
  "timestamp": "2024-10-01 14:30:00"  // 2:30 PM - too late!
}

// ✅ Correct: Entry within 8am-1pm window
{
  "type": "entry_signal",
  "timestamp": "2024-10-01 10:30:00"  // 10:30 AM - valid!
}
```

### Missing Required Fields
```json
// ❌ Wrong: Missing pnl on exit signal
{
  "type": "exit_signal",
  "timestamp": "2024-10-01 15:00:00",
  "price": 455.00
  // Missing: pnl field required for exits
}

// ✅ Correct: Complete exit signal
{
  "type": "exit_signal",
  "timestamp": "2024-10-01 15:00:00",
  "price": 455.00,
  "shares": 100,
  "reason": "Exit reason",
  "direction": "close_long",
  "pnl": 500.0
}
```

## 📚 Example Strategy Files

### Working Examples
- `strategies/corrected_ema_strategy.json` - Complete EMA crossover strategy
- `strategies/test_strategy_with_signals.json` - Simple test strategy
- `strategies/enhanced_ema_9_20_crossover_codified.json` - Full featured example

### Template Files
- Use minimal template above for new strategies
- Follow time filtering rules strictly
- Include performance_metrics for better visualization