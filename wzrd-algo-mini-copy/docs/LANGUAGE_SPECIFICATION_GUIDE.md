# Language Specification Guide for WZRD Strategy Ecosystem

## Overview

This guide ensures that all strategy artifacts are written in language that is compatible with both the Streamlit Strategy Viewer and future ClaudeCode implementation in VectorBT. This creates a unified language standard across the entire WZRD ecosystem.

---

## Core Language Principles

### 1. Absolute Precision
- **No Ambiguity:** Every rule must be testable and implementable
- **No Subjectivity:** Avoid "looks like", "seems", "probably"
- **Exact Values:** Use specific numbers, not ranges when possible
- **Clear Logic:** Every condition must have a clear true/false outcome

### 2. System-Wide Consistency
- **Terminology:** Use the same terms across all components
- **Format:** Maintain consistent JSON structure and naming
- **Logic:** Ensure rules work in Streamlit and can be ported to VectorBT
- **Timing:** Use consistent time formats and timezone handling

### 3. Future-Proof Design
- **VectorBT Compatibility:** Rules must be translatable to VectorBT logic
- **Backtest Ready:** All rules must be backtestable
- **Implementation-Friendly:** Rules must be codable without interpretation
- **Scalable:** Design should work for simple and complex strategies

---

## JSON Schema Language Standards

### Required Field Naming Conventions
```json
{
  "strategy_name": "Descriptive_Name_With_Timeframe",
  "description": "Clear explanation of strategy logic",
  "timeframe": "5min|15min|hour|day",
  "symbol": "SPY|QQQ|AAPL|TSLA",
  "entry_conditions": [...],
  "exit_conditions": [...],
  "risk_management": {...},
  "signals": [...]
}
```

### Signal Type Language
```json
{
  "type": "entry_long|entry_short|exit_long|exit_short",
  "timestamp": "YYYY-MM-DD HH:MM:SS",
  "price": 594.50,
  "shares": 300,
  "reason": "Specific technical condition that triggered signal",
  "execution": "Professional trading language description",
  "calculation": "Entry: $594.50 | Exit: $593.00 | Difference: $1.50 x 300 shares",
  "pnl": 450.0
}
```

### Risk Management Language
```json
{
  "stop_loss": {
    "type": "percentage|fixed|atr|swing_points",
    "value": 0.75,
    "method": "static|dynamic|trailing"
  },
  "take_profit": {
    "type": "percentage|fixed|atr|r_multiple",
    "value": 1.5,
    "method": "static|dynamic|partial"
  },
  "position_size": {
    "type": "fixed|percentage|r_based",
    "value": 300,
    "method": "static|dynamic|volatility_adjusted"
  }
}
```

---

## Streamlit Viewer Language Standards

### Execution Log Language
- **Entry Long:** "BOUGHT {shares} shares @ ${price}"
- **Entry Short:** "SOLD SHORT {shares} shares @ ${price}"
- **Exit Long:** "SOLD {shares} shares @ ${price}"
- **Exit Short:** "BUY TO COVER {shares} shares @ ${price}"

### Signal Reason Language
- **Technical:** "EMA 9 crossed above EMA 20 at ${price}"
- **Price Action:** "Price broke above resistance at ${level}"
- **Volume:** "Volume spike confirmed breakout"
- **Momentum:** "RSI oversold at 27, reversal likely"
- **Pattern:** "Head and shoulders pattern completed"

### Calculation Language
- **Long P&L:** "Entry: ${entry} | Exit: ${exit} | Difference: ${diff} x {shares} shares"
- **Short P&L:** "Entry: ${entry} | Exit: ${exit} | Difference: ${diff} x {shares} shares"
- **R Calculation:** "Risk: ${risk_per_share} x {shares} shares = ${total_risk} R"
- **Position Size:** "Account: ${account_size} | Risk%: ${risk_pct} | Max risk: ${max_risk}"

---

## VectorBT Implementation Language Standards

### Condition Translation Rules
- **Streamlit Language:** "Price closes above EMA 20"
- **VectorBT Translation:** `data['close'] > data['ema_20']`

- **Streamlit Language:** "RSI < 30 and volume > 1M"
- **VectorBT Translation:** `(data['rsi'] < 30) & (data['volume'] > 1000000)`

- **Streamlit Language:** "VWAP bounce with MACD histogram > 0"
- **VectorBT Translation:** `(data['close'] > data['vwap']) & (data['macd_hist'] > 0)`

### Timeframe Language Standards
- **Multi-timeframe:** "HTF: Daily uptrend + MTF: 15min entry signal"
- **VectorBT:** Higher timeframe data resampled and aligned with lower timeframe

### Indicator Parameter Language
- **EMA:** "EMA(period=9)" → `ta.ema(data['close'], length=9)`
- **VWAP:** "VWAP(anchor='session_start')" → `ta.vwap(data, anchor='session_start')`
- **RSI:** "RSI(period=14, overbought=70, oversold=30)" → `ta.rsi(data['close'], length=14)`

---

## Trade Management Language Standards

### Stop Management Language
- **Static Stop:** "Stop at ${price} (fixed level)"
- **ATR Stop:** "Stop at entry - {multiplier}xATR({period})"
- **Trailing Stop:** "Stop trails at {period} swing lows"
- **Breakeven:** "Move stop to entry at {target} profit"

### Position Building Language
- **Pyramiding:** "Add 0.25R at {level}, 0.5R at {level}, 1R at {level}"
- **Scaling:** "Take 50% profit at 1R, 25% at 2R, hold 25% to 3R"
- **Recycling:** "Cover 50% at ${level}, re-enter 50% at ${better_level}"

### Invalidation Language
- **Pre-trade:** "Skip if VIX > 30 or if pre-market volume < 1M"
- **In-trade:** "Exit if momentum diverges or volume dries up"
- **Time-based:** "Exit if position held > 3 days without profit"

---

## Time and Condition Language Standards

### Time of Day Language
- **Entry Windows:** "Entries allowed 9:45-11:30 ET and 13:30-15:45 ET"
- **Exclusion Windows:** "No entries 11:30-13:30 (lunch hour)"
- **Close Rules:** "All positions must be closed by 15:55 ET"

### Market Regime Language
- **Bull Market:** "Only long entries when 50MA > 200MA"
- **Bear Market:** "Only short entries when 50MA < 200MA"
- **Sideways Market:** "Reduce size by 50% when ADX < 20"

### Quality Filter Language
- **A+ Setup:** "Full size when RSI < 20 + volume spike + trend alignment"
- **B+ Setup:** "75% size when 2/3 conditions met"
- **C+ Setup:** "50% size when 1/3 conditions met"

---

## Specialized Trading Terminology

### Strike Language
- **Strike Definition:** "Each entry attempt = 1 strike"
- **Strike Limits:** "Maximum 3 strikes per setup per session"
- **Strike Reset:** "Strike counter resets after 2 consecutive losses"

### Bar Break Language
- **Bar Break (Short):** "Price breaks below previous bar low"
- **Bar Break (Long):** "Price breaks above previous bar high"
- **Inside Bar:** "Current bar inside previous bar range"

### Risk High Day Language
- **Risk High Day:** "Max risk reduced to 0.5% on FOMC/Earnings days"
- **Risk Normal Day:** "Standard 1-2% risk on normal trading days"

---

## Implementation Guidelines

### Rule Writing Best Practices
1. **Be Specific:** "EMA 9 crosses above EMA 20" not "EMA crossover"
2. **Be Testable:** Every rule must have a clear true/false test
3. **Be Complete:** Include all conditions, not just the obvious ones
4. **Be Consistent:** Use the same terminology throughout
5. **Be Implementable:** Rules must be codable in VectorBT

### Language Validation Checklist
- [ ] All conditions have specific parameters
- [ ] No subjective terms (good, bad, better, worse)
- [ ] All time references include timezone
- [ ] All calculations show exact math
- [ ] All rules are backtestable
- [ ] Terminology is consistent across sections
- [ ] Rules work in Streamlit and VectorBT context

### Translation Examples

**Good (VectorBT Compatible):**
```json
{
  "condition": "Close above EMA 20 AND RSI > 50 AND Volume > 1M",
  "translation": "(close > ema_20) & (rsi > 50) & (volume > 1000000)"
}
```

**Bad (Too Vague):**
```json
{
  "condition": "Bullish momentum with good volume",
  "translation": "Cannot translate - subjective terms"
}
```

---

## Quality Assurance Standards

### Strategy Artifact Review
1. **JSON Validation:** All required fields present and properly formatted
2. **Logic Validation:** All rules are testable and implementable
3. **Consistency Check:** Terminology consistent across document
4. **Completeness Check:** All edge cases covered
5. **Translation Check:** Rules can be translated to VectorBT

### Streamlit Validation
1. **Signal Generation:** Arrows appear at correct times
2. **Arrow Colors:** Colors match trade direction correctly
3. **Performance Metrics:** Metrics calculate correctly
4. **Execution Logs:** Logs show professional trading language
5. **P&L Calculations:** Calculations match expected results

### VectorBT Readiness
1. **Indicator Compatibility:** All indicators have VectorBT equivalents
2. **Condition Logic:** All conditions can be expressed in pandas/vectorbt
3. **Timeframe Handling:** Multi-timeframe logic can be implemented
4. **Risk Management:** Risk rules can be coded
5. **Performance Tracking:** All metrics can be calculated

---

## Ecosystem Integration

### Knowledge Base Standards
- **Strategy Library:** All strategies use consistent language
- **Template Library:** All templates follow naming conventions
- **Indicator Library:** All indicators have standard parameters
- **Risk Library:** All risk methods have consistent implementation

### Cross-Component Communication
- **Streamlit → VectorBT:** Strategy artifacts can be directly implemented
- **GPT → Streamlit:** Generated strategies work immediately in viewer
- **GPT → VectorBT:** Generated strategies need minimal modification
- **User → System:** Users understand the language and can contribute

### Documentation Standards
- **Strategy Documents:** Use exact language from this guide
- **Technical Specifications:** Include VectorBT translation notes
- **User Guides:** Explain terminology and conventions
- **Training Materials:** Teach the language standards to new users

---

## Evolution and Maintenance

### Language Updates
- **Version Control:** Track changes to language standards
- **Backward Compatibility:** Maintain compatibility with older strategies
- **Deprecation Process:** Phase out old terminology gracefully
- **Adoption Process:** Gradually introduce new standards

### Community Contributions
- **Style Guide:** Provide examples of good and bad language usage
- **Review Process:** Have language experts review new strategies
- **Feedback Loop:** Collect user feedback on language clarity
- **Continuous Improvement:** Regularly update standards based on usage

---

*This language specification ensures that the entire WZRD ecosystem speaks the same language, making strategies compatible across Streamlit visualization, GPT generation, and VectorBT implementation.*