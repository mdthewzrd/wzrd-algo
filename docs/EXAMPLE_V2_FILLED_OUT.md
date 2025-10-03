# WZRD Strategy Skeleton V2 - Simplified

## Strategy Basics
- **Strategy Name:** Daily Uptrend Pyramid Swing
- **Asset:** SPY
- **Strategy Type:** Swing + Pyramiding + Recycling
- **Core Idea:** Trade daily uptrend dips from extreme lows back to extreme highs using deviation bands

## Timeframes & Setup
- **HTF (Signal):** Daily - 9EMA above 20EMA, not at extremes (72/89 dev bands)
- **MTF (Trigger):** 1hr - Route starts at 72/89 lower dev band hit, ends at upper dev band hit
- **LTF (Execution):** 15min - Enter on bar breaks after route start, pyramid on 9/20 flips

## Entry Rules
- **Main Signal:** Daily uptrend confirmed (9>20EMA) + 1hr at lower dev band extreme
- **Entry Trigger:** 15min bar break above previous high after route start
- **Confirmation:** 15min 9/20 EMA flip to bullish
- **Entry Style:** Limit orders on pullbacks, market on breaks

## Position Management
- **Initial Size:** 1R position with wide ATR stop (0.5 ATR below low)
- **Pyramiding:** Add 0.25R at 15min 9/20 flip, another 0.25R on dips to 15m dev band
- **Max Size:** 1.5R total (stop at previous swing lows when pyramiding)

## Exit Rules
- **Profit Target:** Scale out at 1hr extremes (50% cover) + 15m extremes (30% recycle)
- **Stop Loss:** Initial wide ATR stop, then swing lows, then trail with 9/20 crosses
- **Trailing Stop:** Use hourly 9/20 cross as final exit signal
- **Time Exit:** Exit if no progress within 3 days

## Risk Management
- **Risk per Trade:** 1% of account per R
- **Position Sizing:** R-based - size = account risk % / stop distance
- **Daily Risk Limit:** 3R max per day

## Invalidation Rules
- **Skip If:** Daily at extremes, 9EMA below 20EMA (no uptrend)
- **Exit Early If:** Daily trend breaks (9/20 cross bearish), 1hr route fails

## Key Indicators
- **Primary:** 72/89 EMA deviation bands (6x ATR), 9/20 EMA cloud
- **Secondary:** Volume confirmation, previous day close
- **Settings:** 72/89 EMA with 6x ATR bands, 9/20 EMA for timing

## Quality Filters
- **A+ Setups:** Clean daily uptrend + perfect 1hr extreme hit + strong volume
- **B+ Setups:** Daily uptrend + 1hr near extremes + decent volume
- **Size Adjustments:** A+ = full 1R initial, B+ = 0.75R initial

## Execution Notes
- **Best Times:** Route starts during RTH (8am-12pm ideal), overnight needs extra confirmation
- **Avoid Times:** None specific, but overnight needs 9/20 confirmation
- **Special Rules:** 2 strike limit per setup, reset next day

## Target Performance
- **Win Rate:** 50%
- **Risk:Reward:** 3:1 average winner
- **Trade Frequency:** 1-2 route starts per month

---

## Quick Check Questions:
1. **HTF Setup Clear?** [x] Yes [ ] No
2. **Entry Rules Specific?** [x] Yes [ ] No
3. **Exit Rules Defined?** [x] Yes [ ] No
4. **Risk Management Complete?** [x] Yes [ ] No
5. **Ready for GPT?** [x] Yes [ ] No

---

*Document Status: [Ready for GPT]*