# WZRD Strategy Skeleton Document

## Strategy Overview
- **Strategy Name:** [Clear, descriptive name]
- **Initial Idea:** [Brief concept description]
- **Target Market/Asset:** [SPY, QQQ, specific stocks, etc.]
- **Strategy Type:** [Swing, intraday, scalping, position]

---

## Timeframe Analysis

### Higher Timeframe (HTF) Context
- **Primary HTF:** [Daily, Hourly, etc.]
- **HTF Setup:** [Daily chart pattern, trend, market structure]
- **HTF Entry Trigger:** [What signals opportunity on HTF?]
- **HTF Important Metrics:** [Key indicators, levels, conditions]
- **HTF Confirmation Rules:** [What must be true to proceed?]

### Medium Timeframe (MTF) Context
- **Primary MTF:** [15min, Hourly, etc.]
- **MTF Setup:** [Chart pattern, trend alignment]
- **MTF Entry Trigger:** [What signals execution timing?]
- **MTF Important Metrics:** [Key indicators, levels]
- **MTF Confirmation Rules:** [What validates the setup?]

### Lower Timeframe (LTF) Execution
- **Primary LTF:** [5min, 2min, 1min]
- **LTF Setup:** [Micro-structure, entry timing]
- **LTF Entry Triggers:** [Precise entry points]
- **LTF Exit Management:** [Scaling, stops, targets]
- **LTF Important Metrics:** [Momentum, volume patterns]

---

## Trading Edge & Opportunity

### Edge Type
- **Primary Edge:** [Mean reversion, trend following, breakout, etc.]
- **Secondary Edges:** [Additional opportunities within the setup]
- **Market Conditions:** [Bullish, bearish, sideways, volatility]
- **Time of Day:** [Specific trading sessions or times]

### Alternative Approaches
- **Scalping Add-ons:** [Can we add intraday trades to swing setups?]
- **Multiple Entry Points:** [Different ways to enter the same setup]
- **Hedging Opportunities:** [Ways to reduce risk or add positions]

---

## Technical Indicators & Code

### Required Indicators
- **Primary Indicators:** [EMA 9/20, VWAP, RSI, MACD, etc.]
- **Secondary Indicators:** [Confirmation tools]
- **Custom Code:** [Any specific Pine Script, Python code]

### Indicator Parameters
- **EMA Periods:** [9, 20, 50, etc.]
- **VWAP Settings:** [Standard, anchor points]
- **RSI Levels:** [Overbought/oversold thresholds]
- **Bollinger Bands:** [Periods, deviations]

---

## Execution Strategy

### Entry Style
- **Initial Entry:** [Full size, partial, scaling in]
- **Entry Timing:** [Market orders, limit orders, specific conditions]
- **Entry Logic:** [Why enter at this specific point?]

### Position Building (Pyramiding)
- **Scaling Method:** [Add to winners, average down]
- **Add Triggers:** [What confirms to add more?]
- **Size Progression:** [0.25R → 0.5R → 1R, etc.]
- **Max Position Size:** [Total R exposure per trade]

### Position Management
- **Recycling Strategy:** [Cover partial, re-enter at better prices]
- **Partial Exits:** [Take profits at levels, reduce exposure]
- **Stop Management:** [Trail stops, break-even, time-based]

### Trade Management & Trailing
- **Stop Trailing Method:** [How stops trail - ATR-based, swing points, percentage]
- **Stop Tightening Rules:** [When to tighten stops aggressively]
- **Break-even Rules:** [When to move stop to entry price]
- **Dynamic Stop Adjustment:** [How stops adjust based on volatility/trend]
- **Partial Profit Taking:** [When and how much to take off]
- **Re-entry Rules:** [When to re-enter after partial exit]
- **Position Sizing Adjustments:** [How to adjust size based on performance]

---

## Risk Management

### R-Based Position Sizing
- **Account Risk per Trade:** [1-2% of account]
- **R-Multiple Strategy:** [Initial R, target R multiples]
- **Dynamic Sizing:** [Adjust size based on stop distance]
- **Max Daily Risk:** [Total R exposure per day]

### Stop Loss Logic
- **Initial Stop:** [Where and why?]
- **Stop Trailing:** [How does stop move?]
- **Stop Tightening:** [When to reduce risk?]
- **Time Stops:** [Max holding period]

---

## Trade Invalidators

### Pre-Trade Invalidators
- **Market Regime Filter:** [What market conditions invalidate setups?]
- **Time of Day Filter:** [What times invalidate entries?]
- **Volatility Filter:** [What volatility levels invalidate entries?]
- **Volume Filter:** [What volume conditions invalidate entries?]
- **News Event Filter:** [What news/events invalidate entries?]
- **Technical Filter:** [What technical conditions invalidate entries?]
- **Correlation Filter:** [What market correlations invalidate entries?]
- **Liquidity Filter:** [What liquidity conditions invalidate entries?]

### In-Trade Invalidators
- **Momentum Shift:** [What momentum changes invalidate the trade?]
- **Volume Divergence:** [What volume patterns invalidate the trade?]
- **Time Decay:** [What time-based factors invalidate the trade?]
- **Technical Failure:** [What technical failures invalidate the trade?]
- **Market Structure Break:** [What structure breaks invalidate the trade?]
- **Volatility Explosion:** [What volatility changes invalidate the trade?]
- **Correlation Breakdown:** [What correlation changes invalidate the trade?]
- **Liquidity Dry-up:** [What liquidity changes invalidate the trade?]

### Invalidation Actions
- **Immediate Exit:** [When to exit immediately on invalidation]
- **Partial Exit:** [When to reduce size on invalidation]
- **Stop Adjustment:** [When to adjust stops on invalidation]
- **Position Freeze:** [When to stop adding on invalidation]
- **Reverse Position:** [When to reverse on invalidation]

---

## Covering & Trade Termination

### Covering Strategy
- **Full Cover Conditions:** [When to cover entire position]
- **Partial Cover Rules:** [When to cover partial positions]
- **Scale-out Logic:** [How much to cover at each level]
- **Cover Timing:** [When during the trade to cover]
- **Cover Method:** [Market vs limit orders for covering]

### Strike Management
- **Strike Definition:** [What constitutes a "strike" or attempt]
- **Maximum Strikes:** [How many attempts per setup]
- **Strike Spacing:** [Time/price distance between strikes]
- **Strike Sizing:** [How size changes with each strike]
- **Strike Reset:** [When to reset strike counter]

### Trade End Conditions
- **Profit Target Hit:** [What ends the trade on profit]
- **Stop Loss Hit:** [What ends the trade on loss]
- **Time Limit Reached:** [What time conditions end the trade]
- **Invalidation Triggered:** [What invalidation ends the trade]
- **Manual Override:** [What manual intervention ends the trade]
- **Market Condition Change:** [What market changes end the trade]

### Re-entry Rules
- **Re-entry Waiting Period:** [How long to wait before re-entry]
- **Re-entry Conditions:** [What allows re-entry after exit]
- **Re-entry Size Limits:** [Size restrictions for re-entries]
- **Re-entry Direction:** [Can you reverse or only same direction?]
- **Maximum Re-entries:** [How many re-entries per setup]

---

## Time & Quality Variables

### Time of Day Rules
- **Entry Time Windows:** [When entries are allowed]
- **Exit Time Windows:** [When exits are required]
- **Avoidance Times:** [Times to avoid trading]
- **Session Specific Rules:** [Different rules for different sessions]
- **News Time Rules:** [Rules around news/event times]
- **Lunch Hour Rules:** [Rules for low-volume periods]
- **Close Period Rules:** [Rules near market open/close]

### A+ Variables (Quality Filters)
- **A+ Setup Definition:** [What makes an A+ quality setup]
- **Size Scaling for Quality:** [How size changes with quality]
- **Risk Adjustment for Quality:** [How risk changes with quality]
- **Entry Aggressiveness:** [How aggressiveness changes with quality]
- **Hold Time Adjustments:** [How hold time changes with quality]
- **Special Management Rules:** [Special rules for A+ setups]

### Market Regime Variables
- **Bull Market Adjustments:** [How strategy changes in bull markets]
- **Bear Market Adjustments:** [How strategy changes in bear markets]
- **Sideways Market Adjustments:** [How strategy changes in sideways markets]
- **High Volatility Adjustments:** [How strategy changes in high volatility]
- **Low Volatility Adjustments:** [How strategy changes in low volatility]
- **Trend Strength Adjustments:** [How strategy changes with trend strength]
- **Liquidity Adjustments:** [How strategy changes with liquidity]

### Special Conditions
- **Economic Event Rules:** [Rules around economic data releases]
- **Earnings Season Rules:** [Rules during earnings season]
- **Fed Meeting Rules:** [Rules around Fed announcements]
- **Options Expiration Rules:** [Rules around options expiration]
- **Month/Quarter End Rules:** [Rules around period ends]
- **Holiday Schedule Rules:** [Rules around holidays]
- **Special Event Rules:** [Rules for special market events]

---

## Trade Examples & Annotated Charts

### Ideal Setup Examples
- **Chart 1:** [HTF setup screenshot with annotations]
- **Chart 2:** [MTF trigger screenshot with annotations]
- **Chart 3:** [LTF execution screenshot with annotations]

### Execution Scenarios
- **Scenario 1:** [Perfect setup execution]
- **Scenario 2:** [Early entry management]
- **Scenario 3:** [Adverse movement handling]

---

## Performance Expectations

### Target Metrics
- **Win Rate:** [Expected percentage]
- **Profit Factor:** [Gross profit / gross loss]
- **Expectancy:** [Expected $ per R risked]
- **Sharpe Ratio:** [Risk-adjusted returns]
- **Max Drawdown:** [Acceptable drawdown %]
- **Trade Frequency:** [Trades per day/week/month]

### Compounding Strategy
- **Growth Rate:** [Expected monthly/annual growth]
- **Position Scaling:** [How size grows with account]
- **Reinvestment:** [How profits are compounded]

---

## Trading Psychology & Style

### Trading Personality
- **Risk Tolerance:** [Conservative, moderate, aggressive]
- **Patience Level:** [Wait for perfect setups vs. more frequent]
- **Conviction Level:** [High conviction vs. smaller positions]
- **Emotional Control:** [How do you handle drawdowns?]

### Style Preferences
- **Trend Following:** [With trend, against trend]
- **Mean Reversion:** [Fade extremes, buy dips, sell rallies]
- **Position Building:** [Pyramid into winners, add on pullbacks]
- **Entry Style:** [Pullbacks, breakouts, reversals]

---

## Additional Notes

### Special Considerations
- [Any unique aspects of this strategy]
- [Market regime dependencies]
- [Correlation to other strategies]
- [Unique risk factors]

### Questions for GPT
- [What do you need clarification on?]
- [What parameters need definition?]
- [What scenarios need examples?]

---

## Manual Checkpoints

### ✅ HTF/Daily Setup Validation
- [ ] HTF pattern识别正确
- [ ] Entry trigger conditions clear
- [ ] Market context appropriate

### ✅ Trade Start/Trigger Validation
- [ ] Entry logic matches trading style
- [ ] Position sizing approach correct
- [ ] Risk management rules applied

### ✅ Execution Accuracy Validation
- [ ] Entry timing matches style
- [ ] Position building logic sound
- [ **Exit management comprehensive

---

*Document Status: [Draft/Ready for GPT/Confirmed/Ready for Final PRD]*