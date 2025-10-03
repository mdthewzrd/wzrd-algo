# WZRD Strategy Skeleton V2 - Daily Uptrend Pyracycle Swing

## Strategy Basics
- **Strategy Name:** Daily Uptrend Pyracycle Swing
- **Asset:** SPY
- **Strategy Type:** Swing + Pyramiding + Recycling
- **Core Idea:** Higher timeframe trend following - wait for dips in daily uptrends, then aggressively pyramid into winners from extreme lower deviations back to extreme highs

## Timeframes & Setup
- **HTF (Signal):** Daily chart - Daily uptrend with 9 EMA above 20 EMA, not at extremes (use 72/89 6-9 dev bands as extreme guide)
- **MTF (Trigger):** Hourly - Route start/end system using 72/89 6 dev bands (lower hit = start, upper hit = end)
- **LTF (Execution):** 15min - Market structure breaks, 9/20 EMA crosses, pyramid on dips to dev bands

## Entry Rules
- **Main Signal:** Daily 9 EMA crosses and confirms above 20 EMA in uptrend, not above upper 72/89 6 dev band
- **Entry Trigger:** Hourly 72/89 6 dev band lower hit (route start) + 15min bar break vs wide ATR stop
- **Confirmation:** 15min 9/20 EMA cross to bullish after initial entry
- **Entry Style:** Limit orders on mini pullbacks, wait for break of prior bar highs to confirm

## Position Management
- **Initial Size:** 1R out the gate with full size wide stop (0.5 ATR below low)
- **Pyramiding:** Add aggressively on 9/20 cross, then pyramid on dips to 15min dev bands until 15min extreme
- **Max Size:** 1R total position (multiple entries but risk stays at 1R)

## Exit Rules
- **Profit Target:** Hourly 72/89 6 dev band upper hit OR hourly 9/20 cross bearish
- **Stop Loss:** Initial = wide ATR stop, then below swing lows when pyramiding
- **Trailing Stop:** Swing points, then 9/20 hourly when getting tight near highs
- **Time Exit:** None specified

## Risk Management
- **Risk per Trade:** 1% of account
- **Position Sizing:** R-based sizing targeting 3:1 R average winner
- **Daily Risk Limit:** 3R maximum

## Invalidation Rules
- **Skip If:** Not in daily uptrend, 9 below 20 EMA, price in daily extremes, outside RTH (4pm-8am need 9/20 cross confirmation)
- **Exit Early If:** HTF trendbreak, MTF trendbreak, hourly 9/20 cross bearish, momentum shift

## Key Indicators
- **Primary:** 72/89 EMA deviation bands (6-9 multiplier), 9/20 EMA cloud, previous day close
- **Secondary:** ATR for stop calculations, volume for confirmation
- **Settings:** Dev bands 72/89 6-9 upper/lower, 9/20 jlines, 15min dev bands 9/20 upper 2.5-3 lower 1-1.5

## Quality Filters
- **A+ Setups:** Route start during RTH (8am-12pm), clear daily uptrend, extreme deviation touch
- **B+ Setups:** Outside RTH signals need 9/20 cross confirmation, less extreme touches
- **Size Adjustments:** Full 1R for A+ setups, reduce size for B+ setups

## Execution Notes
- **Best Times:** Route starts during RTH 8am-12pm ideal, signals beyond need extra confirmation
- **Avoid Times:** When in daily extremes, when trend is failing
- **Special Rules:** Stop pyramiding at 15min extremes, recycle 30% at extremes and re-enter on hourly 9/20 lower 1

## Target Performance
- **Win Rate:** 50%
- **Risk:Reward:** 3:1 R average winner, 2+ profit factor
- **Trade Frequency:** 1-2 route starts per month

## Detailed Execution Flow

### Route Start Process
1. **Daily Check:** 9 above 20 EMA, not in extremes
2. **Hourly Trigger:** 72/89 6 dev band lower hit
3. **15min Entry:** Bar break with 0.5 ATR stop below low
4. **First Add:** 9/20 cross on 15min vs 1c below lowest low

### Pyramiding Process
1. **Continue Adding:** On dips to 9/20 lower 1 vs previous swing lows
2. **Stop Management:** Risk swing low points on hourly
3. **Extreme Recognition:** Stop pyramiding when getting 15min extreme

### Recycling Process
1. **15min Extreme:** Cover 30%, trail rest
2. **Re-entry:** Look to add back on dip to hourly 9/20 dev band lower 1
3. **Hourly Extreme:** Cover 50% at hourly 72/89, trail rest for 9/20 flip

### Exit Hierarchy
1. **Immediate:** Hourly 9/20 cross bearish = flat
2. **Partial:** 15min extremes = 30% recycle, hourly extremes = 50% cover
3. **Trail:** Use swing lows and hourly 9/20 context for remaining position

---

## Quick Check Questions:
1. **HTF Setup Clear?** [X] Yes [ ] No - Daily uptrend 9>20, not extreme
2. **Entry Rules Specific?** [X] Yes [ ] No - Hourly dev band + 15min execution
3. **Exit Rules Defined?** [X] Yes [ ] No - Multiple exit levels with recycling
4. **Risk Management Complete?** [X] Yes [ ] No - 1R position, 3R daily max
5. **Ready for GPT?** [X] Yes [ ] No - Complete pyramiding swing system

---

## Strike Management Rules
- **Maximum Attempts:** 2 wide stop attempts, then 1 more on 15min 9/20 cross
- **Strikeout Rule:** After 3 attempts, wait until next day
- **Re-entry:** Can attempt new route start next trading day

## Market Regime Filters
- **Bull Market:** Strategy crushes in strong uptrends - primary conditions
- **Neutral Market:** Reduce size, require stronger confirmation
- **Bear Market:** Avoid or use much smaller size with tight stops

---

*Document Status: Ready for GPT - Complete pyramiding strategy with route start/end system*