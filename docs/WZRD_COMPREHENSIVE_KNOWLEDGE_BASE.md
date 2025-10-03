# WZRD Trading Strategy Generator - Comprehensive Knowledge Base

## Table of Contents
1. [Trading Strategy Fundamentals](#trading-strategy-fundamentals)
2. [Technical Analysis & Indicators](#technical-analysis--indicators)
3. [Risk Management & Position Sizing](#risk-management--position-sizing)
4. [Multi-timeframe Analysis](#multi-timeframe-analysis)
5. [Advanced Position Management](#advanced-position-management)
6. [Market Conditions & Regimes](#market-conditions--regimes)
7. [Strategy Validation & Testing](#strategy-validation--testing)
8. [Implementation & Coding](#implementation--coding)
9. [Command Reference](#command-reference)
10. [Workflow Examples](#workflow-examples)
11. [Troubleshooting & FAQ](#troubleshooting--faq)
12. [Glossary & Terminology](#glossary--terminology)

---

## Trading Strategy Fundamentals

### Strategy Types & Classifications

#### 1. Trend Following Strategies
**Definition:** Strategies that aim to capture sustained price movements in the direction of the established trend.

**Key Characteristics:**
- Lower win rates (35-45%) but higher risk-reward ratios
- Longer holding periods (days to weeks)
- Require strong trend identification
- Use moving averages, trend lines, momentum indicators

**Common Patterns:**
- Moving average crossovers (9/20, 20/50, 50/200)
- Trend line breaks and retests
- Higher highs and higher lows
- Momentum divergences

**Entry Conditions:**
- Pullbacks to key moving averages
- Breakouts from consolidation patterns
- Trend line retests with confirmation
- Momentum indicator alignment

**Exit Conditions:**
- Trend line breaks
- Moving average crossover reversal
- Momentum divergence with price
- Key support/resistance levels

#### 2. Mean Reversion Strategies
**Definition:** Strategies that bet on price returning to its mean or average value after extending too far in one direction.

**Key Characteristics:**
- Higher win rates (55-65%) but lower risk-reward ratios
- Shorter holding periods (minutes to days)
- Work best in range-bound markets
- Use oscillators, standard deviations, VWAP

**Common Patterns:**
- Bollinger Band extremes
- RSI overbought/oversold conditions
- VWAP extensions and reversions
- Price deviations from moving averages

**Entry Conditions:**
- RSI < 30 or > 70
- Price outside 2 standard deviations
- Extensions > 1% from VWAP
- Volume spikes at extremes

**Exit Conditions:**
- Return to VWAP or moving average
- RSI crossing back through 50
- Volume drying up at target
- Time-based exits

#### 3. Breakout Strategies
**Definition:** Strategies that aim to capture significant price movements when price breaks out of consolidation patterns or key levels.

**Key Characteristics:**
- Moderate win rates (45-55%)
- Medium holding periods (hours to days)
- Require volatility expansion
- Use volume confirmation, pattern recognition

**Common Patterns:**
- Rectangle and box pattern breaks
- Triangle breakouts (ascending, descending, symmetrical)
- Key support/resistance level breaks
- High-tight flag patterns

**Entry Conditions:**
- Volume > 1.5x average volume
- Price closes outside pattern
- Momentum indicator confirmation
- Multiple timeframe alignment

**Exit Conditions:**
- Measured move targets
- Volume failure at new levels
- Return to breakout level
- Time-based stops

#### 4. Scalping Strategies
**Definition:** High-frequency strategies aiming to capture small price movements with very short holding periods.

**Key Characteristics:**
- High win rates (60-75%)
- Very short holding periods (seconds to minutes)
- Require high liquidity and tight spreads
- Use order flow, micro-structure analysis

**Common Patterns:**
- Tick-level reversals
- Micro support/resistance levels
- Order book imbalances
- Time-based patterns

**Entry Conditions:**
- Liquidity detection
- Order flow signals
- Micro-trend alignment
- Spread compression

**Exit Conditions:**
- Quick profit targets (0.1-0.5%)
- Time stops (30-120 seconds)
- Volume-based exits
- Spread expansion

### Market Structure Analysis

#### 1. Trend Identification
**Uptrend Characteristics:**
- Higher highs and higher lows
- Price above key moving averages (20, 50, 200)
- Higher momentum readings
- Volume expansion on rallies

**Downtrend Characteristics:**
- Lower highs and lower lows
- Price below key moving averages
- Lower momentum readings
- Volume expansion on declines

**Sideways Market Characteristics:**
- Price oscillating between support and resistance
- Moving averages flattening
- Mixed momentum signals
- Variable volume patterns

#### 2. Support and Resistance
**Static Levels:**
- Previous swing highs and lows
- Round numbers (psychological levels)
- Gap fill areas
- Volume profile nodes

**Dynamic Levels:**
- Moving averages (20, 50, 200 EMA/SMA)
- VWAP (Volume Weighted Average Price)
- Trend lines
- Fibonacci retracements/Extensions

#### 3. Market Phases
**Accumulation Phase:**
- Range-bound price action
- Volume picking up at lows
- Institutional buying
- Base building patterns

**Markup Phase:**
- Breaking out of accumulation
- Higher highs and higher lows
- Volume confirmation
- Trend following strategies work best

**Distribution Phase:**
- Range-bound at highs
- Volume at highs without price progress
- Institutional selling
- Reversal patterns forming

**Markdown Phase:**
- Breaking down from distribution
- Lower highs and lower lows
- Volume on declines
- Trend following (short) strategies work best

---

## Technical Analysis & Indicators

### Moving Averages

#### 1. Simple Moving Average (SMA)
**Calculation:** SMA = (Sum of closing prices over N periods) / N

**Common Periods:**
- 9-period: Short-term trend
- 20-period: Medium-term trend
- 50-period: Long-term trend
- 200-period: Major trend indicator

**Usage:**
- Trend identification (price above/below)
- Dynamic support/resistance
- Crossover signals
- Moving average envelopes

#### 2. Exponential Moving Average (EMA)
**Calculation:** EMA = (Close - EMA_previous) × (2/(N+1)) + EMA_previous

**Advantages over SMA:**
- More responsive to recent price action
- Better for short-term trading
- Reduces lag in signals
- More weight to current prices

**Common EMA Strategies:**
- 9/20 EMA crossover (short-term trend changes)
- 20/50 EMA crossover (medium-term trend changes)
- EMA ribbon (multiple EMAs for trend strength)
- Price vs EMA relationship (pullback entries)

#### 3. Volume Weighted Average Price (VWAP)
**Calculation:** VWAP = Σ(Price × Volume) / Σ(Volume)

**Key Characteristics:**
- Intraday indicator (resets daily)
- Represents average price all traders paid
- Used by institutions for execution
- Works best with high volume

**VWAP Strategies:**
- Mean reversion to VWAP
- VWAP as dynamic support/resistance
- VWAP crossovers with price
- Multiple VWAP anchors (session, week, month)

### Momentum Indicators

#### 1. Relative Strength Index (RSI)
**Calculation:** RSI = 100 - (100 / (1 + RS))
Where RS = Average Gain / Average Loss over N periods

**Standard Settings:**
- Period: 14
- Overbought: > 70
- Oversold: < 30
- Midline: 50

**RSI Strategies:**
- Divergence trading (price vs RSI)
- Overbought/oversold reversals
- RSI trend line breaks
- RSI failure swings

#### 2. MACD (Moving Average Convergence Divergence)
**Components:**
- MACD Line: 12-period EMA - 26-period EMA
- Signal Line: 9-period EMA of MACD line
- Histogram: MACD Line - Signal Line

**MACD Strategies:**
- MACD line crossing signal line
- Histogram expansion/contraction
- Zero line crossovers
- Divergence patterns

#### 3. Stochastic Oscillator
**Calculation:** %K = 100 × (Close - Lowest Low) / (Highest High - Lowest Low)
%D = 3-period SMA of %K

**Settings:**
- %K Period: 14
- %D Period: 3
- Slowing: 3
- Overbought: > 80
- Oversold: < 20

**Stochastic Strategies:**
- Overbought/oversold reversals
- Stochastic crossover signals
- Divergence trading
- Failure swings

### Volatility Indicators

#### 1. Bollinger Bands
**Calculation:**
- Middle Band: 20-period SMA
- Upper Band: 20-period SMA + (2 × Standard Deviation)
- Lower Band: 20-period SMA - (2 × Standard Deviation)

**Bollinger Band Strategies:**
- Band rides (strong trends)
- Band squeezes (volatility contraction)
- Reversion to bands (mean reversion)
- Band width expansion (breakout signals)

#### 2. Average True Range (ATR)
**Calculation:** ATR = (Previous ATR × (N-1) + Current TR) / N
Where TR = max(High-Low, |High-Previous Close|, |Low-Previous Close|)

**ATR Usage:**
- Volatility measurement
- Stop loss placement
- Position sizing
- Breakout confirmation

#### 3. Keltner Channels
**Calculation:**
- Middle Line: 20-period EMA
- Upper Channel: 20-period EMA + (2 × ATR)
- Lower Channel: 20-period EMA - (2 × ATR)

**Keltner Strategies:**
- Trend following with envelope breaks
- Mean reversion to middle line
- Volatility breakout detection
- Dynamic stop placement

### Volume Indicators

#### 1. On-Balance Volume (OBV)
**Calculation:** OBV = Previous OBV + Volume (if up) - Volume (if down)

**OBV Analysis:**
- Confirming price trends
- Divergence signals
- Breakout confirmation
- Trend strength assessment

#### 2. Volume Profile
**Components:**
- Volume at Price (VAP) levels
- Point of Control (POC)
- Value Area (VA)
- High Volume Nodes (HVN)

**Volume Profile Strategies:**
- Trading around POC
- Value Area high/low breaks
- High volume node support/resistance
- Low volume node acceleration zones

#### 3. Money Flow Index (MFI)
**Calculation:** MFI = 100 - (100 / (1 + Money Flow))
Money Flow = Typical Price × Volume
Typical Price = (High + Low + Close) / 3

**MFI Strategies:**
- Overbought/oversold conditions
- Divergence trading
- Money flow confirmation
- Volume-weighted RSI

### Pattern Recognition

#### 1. Candlestick Patterns
**Reversal Patterns:**
- Doji (indecision)
- Hammer/Hanging Man
- Engulfing Patterns
- Morning/Evening Star
- Shooting Star/Inverted Hammer

**Continuation Patterns:**
- Marubozu (strong trend)
- Spinning Tops (consolidation)
- Three White Soldiers/Black Crows
- Rising/Falling Three Methods

#### 2. Chart Patterns
**Reversal Patterns:**
- Head and Shoulders
- Double Top/Bottom
- Triple Top/Bottom
- Rounded Top/Bottom

**Continuation Patterns:**
- Flags and Pennants
- Triangles (Ascending, Descending, Symmetrical)
- Rectangles (Box Patterns)
- Cup and Handle

#### 3. Harmonic Patterns
**Primary Harmonic Patterns:**
- Gartley (222 Pattern)
- Butterfly Pattern
- Bat Pattern
- Crab Pattern
- Cypher Pattern

**Fibonacci Ratios in Harmonics:**
- 0.382, 0.500, 0.618, 0.786 (Retracements)
- 1.272, 1.414, 1.618, 2.000 (Extensions)
- 0.886 (Square root of 0.786)

---

## Risk Management & Position Sizing

### R-Based Risk Management

#### 1. Understanding R Multiples
**Definition:** R represents the initial risk per trade, measured as a percentage of account equity.

**Standard R Values:**
- Conservative: 0.5% - 1.0% per trade
- Moderate: 1.0% - 2.0% per trade
- Aggressive: 2.0% - 3.0% per trade

**Account Risk Calculation:**
- Account Size: $100,000
- Risk per Trade: 1% = $1,000
- Stop Distance: $2.00 per share
- Max Shares: $1,000 / $2.00 = 500 shares

#### 2. Position Sizing Methods
**Fixed Fractional:**
- Risk fixed percentage of account
- Adjusts position size based on volatility
- Account growth increases position size
- Account drawdown decreases position size

**Fixed Dollar:**
- Risk fixed dollar amount per trade
- Consistent risk regardless of account size
- Easier to track and manage
- Less optimal for account growth

**Volatility Adjusted:**
- Position size inversely related to volatility
- More shares in low volatility, fewer in high
- Better risk normalization
- Uses ATR for volatility measurement

#### 3. Stop Loss Placement
**Technical Stops:**
- Support/Resistance levels
- Moving averages
- Trend lines
- Pattern completion points

**Volatility Stops:**
- ATR multiples (1x, 2x, 3x ATR)
- Standard deviation bands
- Bollinger Band extremes
- Keltner Channel breaks

**Time Stops:**
- Maximum holding period
- Session end stops
- Event-based stops
- Volatility contraction stops

### Advanced Risk Management

#### 1. Pyramiding Strategies
**Progressive Building:**
- Initial entry: 0.25R
- Confirmation add: 0.25R (total 0.5R)
- Continuation add: 0.5R (total 1.0R)
- Maximum exposure: 1.0-2.0R per setup

**Pyramiding Rules:**
- Only add to winning positions
- Each add at better price than initial
- Stop moved to breakeven after first add
- Reduce size if volatility increases

#### 2. Scaling Out Strategies
**Partial Profit Taking:**
- Take 50% at 1R target
- Take 25% at 2R target
- Hold 25% to 3R target
- Stop moved to breakeven at 1R

**Scaling Logic:**
- Reduce risk as profit increases
- Let winners run partially
- Lock in profits at levels
- Manage emotional trading

#### 3. Breakeven Management
**Breakeven Rules:**
- Move stop to entry price at 1R profit
- Add small buffer (0.1R) for noise
- Only on high-confidence trades
- Consider volatility when placing

**Timing Considerations:**
- Wait for confirmation of move
- Don't move too early (whipsaw risk)
- Consider market conditions
- Account for transaction costs

### Portfolio Level Risk

#### 1. Correlation Management
**Correlation Types:**
- Positive correlation: Assets move together
- Negative correlation: Assets move opposite
- No correlation: Random movement

**Correlation Rules:**
- Limit exposure to highly correlated assets
- Use negative correlation for hedging
- Diversify across uncorrelated assets
- Monitor correlation changes over time

#### 2. Sector Exposure
**Sector Diversification:**
- Limit exposure to single sector
- Balance across market sectors
- Consider sector rotation
- Monitor sector volatility

**Sector Risk Limits:**
- Maximum 20% in single sector
- Maximum 40% in related sectors
- Rebalance quarterly or as needed
- Consider sector ETFs for exposure

#### 3. Market Regime Risk
**Regime Identification:**
- Bull markets: Trend following, buy dips
- Bear markets: Short selling, cash positions
- Sideways markets: Range trading, mean reversion
- High volatility: Reduced size, wider stops

**Regime Adjustment:**
- Reduce position size in uncertain regimes
- Change strategy type based on regime
- Increase cash in unfavorable regimes
- Use regime-specific indicators

---

## Multi-timeframe Analysis

### Timeframe Hierarchy

#### 1. Higher Timeframe (HTF) - Daily/Weekly
**Purpose:** Market structure and trend identification

**Key Components:**
- Major trend direction
- Key support/resistance levels
- Market regime (bull/bear/sideways)
- Volume patterns and accumulation/distribution

**Analysis Tools:**
- Moving averages (50, 200)
- Trend lines and channels
- Volume profile
- Market structure (higher highs/lows)

**Decision Rules:**
- Only trade with HTF trend
- Use HTF for major support/resistance
- Identify HTF reversal patterns
- Confirm HTF momentum alignment

#### 2. Medium Timeframe (MTF) - 4 Hour/Hourly
**Purpose:** Entry timing and setup confirmation

**Key Components:**
- Intermediate trend alignment
- Setup identification
- Entry timing windows
- Risk management levels

**Analysis Tools:**
- Moving averages (20, 50)
- Momentum indicators (RSI, MACD)
- Volume confirmation
- Pattern recognition

**Decision Rules:**
- Enter when MTF aligns with HTF
- Use MTF for entry timing
- Place stops at MTF levels
- Scale based on MTF signals

#### 3. Lower Timeframe (LTF) - 15min/5min
**Purpose:** Precise entry execution and position management

**Key Components:**
- Micro-structure analysis
- Precise entry points
- Position building opportunities
- Exit timing

**Analysis Tools:**
- Price action analysis
- Order flow indicators
- Micro-support/resistance
- Short-term momentum

**Decision Rules:**
- Execute entries at LTF levels
- Add to positions on LTF confirmations
- Trail stops using LTF structure
- Take partial profits at LTF targets

### Multi-timeframe Alignment

#### 1. Trend Alignment Matrix
**Bullish Alignment:**
- HTF: Uptrend (higher highs/lows)
- MTF: Uptrend or consolidation
- LTF: Uptrend or pullback

**Bearish Alignment:**
- HTF: Downtrend (lower highs/lows)
- MTF: Downtrend or consolidation
- LTF: Downtrend or pullback

**Sideways Alignment:**
- HTF: Range-bound
- MTF: Range-bound
- LTF: Range-bound or micro-trends

#### 2. Signal Hierarchy
**Primary Signals (HTF):**
- Trend changes
- Major support/resistance breaks
- Reversal patterns
- Volume climaxes

**Secondary Signals (MTF):**
- Setup confirmations
- Entry timing windows
- Risk level identification
- Pattern completions

**Tertiary Signals (LTF):**
- Precise entry points
- Position building
- Exit timing
- Stop management

#### 3. Timeframe Confluence
**Confluence Rules:**
- Multiple timeframes showing same signal
- Higher timeframe confirmation required
- Lower timeframe for execution precision
- Weight higher timeframes more heavily

**Confluence Examples:**
- HTF trend + MTF pullback + LTF reversal
- HTF support + MTF bounce + LTF breakout
- HTF reversal + MTF confirmation + LTF entry

### Multi-timeframe Risk Management

#### 1. Timeframe-Based Stop Placement
**HTF Stops:**
- Major support/resistance levels
- Trend line breaks
- Moving average levels
- Pattern failure points

**MTF Stops:**
- Swing highs/lows
- Minor support/resistance
- Indicator-based stops
- Volatility stops

**LTF Stops:**
- Micro-structure levels
- Recent swing points
- Short-term volatility
- Time-based stops

#### 2. Position Sizing by Timeframe
**HTF-Based Sizing:**
- Larger positions for major trends
- Longer holding periods
- Wider stop distances
- Higher profit targets

**MTF-Based Sizing:**
- Medium position sizes
- Medium holding periods
- Moderate stop distances
- Moderate profit targets

**LTF-Based Sizing:**
- Smaller positions for scalping
- Short holding periods
- Tighter stop distances
- Smaller profit targets

#### 3. Multi-timeframe Exit Strategy
**HTF Exits:**
- Trend reversal signals
- Major resistance/support
- Long-term target reached
- Market regime change

**MTF Exits:**
- Profit targets reached
- Risk-reward achieved
- Pattern completion
- Momentum divergence

**LTF Exits:**
- Partial profit taking
- Stop trailing
- Time-based exits
- Micro-structure changes

---

## Advanced Position Management

### Pyramiding Strategies

#### 1. Progressive Pyramiding
**Entry Sequence:**
- Initial Entry: 0.25R at primary setup
- Confirmation Add: 0.25R at first confirmation
- Continuation Add: 0.5R at trend continuation
- Maximum Position: 1.0R total exposure

**Add Conditions:**
- Price moves favorably from initial entry
- Technical indicators confirm direction
- Volume supports continuation
- Risk-reward ratio improves

**Risk Management:**
- Move stop to breakeven after first add
- Trail stop as position builds
- Reduce size if volatility increases
- Take partial profits at targets

#### 2. Aggressive Pyramiding
**Entry Sequence:**
- Initial Entry: 0.5R at strong setup
- Quick Add: 0.5R at immediate confirmation
- Full Size: 1.0R at trend confirmation
- Maximum: 2.0R for exceptional setups

**Add Conditions:**
- Strong momentum confirmation
- Multiple indicator alignment
- Volume expansion
- Market regime support

**Risk Management:**
- Immediate breakeven stops
- Tight trailing stops
- Quick partial profits
- Reduced holding periods

#### 3. Conservative Pyramiding
**Entry Sequence:**
- Initial Entry: 0.5R at high-probability setup
- Single Add: 0.5R at strong confirmation
- Maximum: 1.0R total exposure
- Only on A+ setups

**Add Conditions:**
- Multiple timeframe alignment
- Strong technical confirmation
- Favorable risk-reward ratio
- Low correlation to existing positions

**Risk Management:**
- Conservative stop placement
- Slower position building
- Longer holding periods
- Higher profit targets

### Recycling Strategies

#### 1. Partial Cover and Re-entry
**Cover Strategy:**
- Cover 50% at first target
- Cover 25% at second target
- Hold 25% for final target
- Re-enter at better price levels

**Re-entry Rules:**
- Wait for pullback/retracement
- Better price than initial cover
- Technical confirmation
- Volume support

**Risk Management:**
- Reduce size on re-entries
- Use tighter stops
- Take quicker profits
- Monitor correlation

#### 2. Full Position Recycling
**Complete Exit:**
- Exit entire position at target
- Wait for better setup
- Re-enter full position
- Often different timeframe

**Recycling Conditions:**
- Market regime change
- Better risk-reward setup
- Correlation shift
- Volatility change

**Cycle Management:**
- Track recycling frequency
- Monitor performance impact
- Adjust based on market conditions
- Consider transaction costs

#### 3. Multi-Leg Recycling
**Leg Structure:**
- Leg 1: Initial position (0.5R)
- Leg 2: First recycle (0.5R)
- Leg 3: Second recycle (0.5R)
- Maximum: 1.5R total exposure

**Timing Rules:**
- Wait for setup completion
- Allow time for market structure change
- Use multiple timeframe confirmation
- Consider volatility cycles

**Position Management:**
- Independent stop management per leg
- Correlation monitoring
- Size adjustment based on performance
- Overall portfolio risk limits

### Dynamic Stop Management

#### 1. ATR-Based Stops
**ATR Stop Calculation:**
- Initial Stop: Entry ± (2 × ATR)
- Trail Stop: Highest high ± (1.5 × ATR)
- Breakeven: Entry price when profit ≥ 1 × ATR
- Time Stop: Exit after N periods without progress

**ATR Period Selection:**
- Short-term: 5-10 period ATR
- Medium-term: 14-20 period ATR
- Long-term: 20-50 period ATR
- Volatility-adjusted based on market

**Advantages:**
- Adapts to market volatility
- Objective stop placement
- Reduces whipsaw in low volatility
- Provides breathing room in high volatility

#### 2. Swing Point Stops
**Swing Point Identification:**
- Higher lows for uptrends
- Lower highs for downtrends
- Key reversal points
- Volume confirmation points

**Stop Placement Rules:**
- Below recent swing low (long positions)
- Above recent swing high (short positions)
- Add small buffer for noise
- Adjust for volatility

**Management Rules:**
- Move stop to new swing points
- Use higher timeframe swing points for major trends
- Combine with other stop methods
- Consider market structure

#### 3. Indicator-Based Stops
**Moving Average Stops:**
- Below key moving average (long)
- Above key moving average (short)
- Multiple moving average layers
- Exponential vs simple selection

**Momentum Stops:**
- RSI crossing key levels
- MACD histogram reversal
- Stochastic extreme reversals
- Momentum divergence

**Volatility Stops:**
- Bollinger Band extremes
- Keltner Channel breaks
- Standard deviation bands
- Volatility contraction/expansion

### Position Sizing Adjustments

#### 1. Volatility-Based Sizing
**Volatility Measurement:**
- ATR (Average True Range)
- Standard deviation of returns
- Bollinger Band width
- Historical volatility

**Sizing Formula:**
- Base Size = Account Risk / ATR
- Adjust for market conditions
- Reduce size in high volatility
- Increase size in low volatility

**Implementation:**
- Calculate daily ATR
- Determine volatility percentile
- Adjust position size accordingly
- Monitor and adjust regularly

#### 2. Correlation-Based Sizing
**Correlation Analysis:**
- Calculate correlation between positions
- Identify highly correlated assets
- Group assets by correlation
- Adjust exposure based on correlation

**Sizing Rules:**
- Reduce size for highly correlated positions
- Increase size for negatively correlated positions
- Limit total correlation exposure
- Monitor correlation changes

**Portfolio Impact:**
- Diversification benefits
- Risk concentration reduction
- Performance optimization
- Drawdown mitigation

#### 3. Performance-Based Sizing
**Performance Tracking:**
- Win rate by strategy
- Profit factor by asset
- Average win/loss ratios
- Maximum drawdown periods

**Sizing Adjustment:**
- Increase size for high-performing strategies
- Decrease size for underperforming strategies
- Consider recency bias
- Implement size limits

**Risk Controls:**
- Maximum size per strategy
- Minimum size for new strategies
- Size adjustment frequency
- Performance review periods

---

## Market Conditions & Regimes

### Market Regime Identification

#### 1. Trending Markets
**Bull Market Characteristics:**
- Price above key moving averages
- Higher highs and higher lows
- Positive momentum readings
- Volume expansion on rallies

**Bear Market Characteristics:**
- Price below key moving averages
- Lower highs and lower lows
- Negative momentum readings
- Volume expansion on declines

**Trending Market Strategies:**
- Trend following (moving averages, trend lines)
- Breakout trading (pattern breaks)
- Momentum trading (indicators)
- Position building with trend

#### 2. Range-Bound Markets
**Sideways Market Characteristics:**
- Price oscillating between support/resistance
- Flattening moving averages
- Mixed momentum signals
- Variable volume patterns

**Range-Bound Strategies:**
- Mean reversion (Bollinger Bands, RSI)
- Support/resistance trading
- Fade extensions
- Range-bound pattern trading

#### 3. Volatile Markets
**High Volatility Characteristics:**
- Wide price ranges
- High ATR readings
- Large volume spikes
- Frequent gap openings

**Low Volatility Characteristics:**
- Narrow price ranges
- Low ATR readings
- Consolidation patterns
- Decreasing volume

**Volatility-Based Strategies:**
- High volatility: Breakout trading, wider stops
- Low volatility: Mean reversion, tighter stops
- Volatility expansion: Breakout confirmation
- Volatility contraction: Coiled spring patterns

### Economic Event Management

#### 1. Fed Meetings
**Pre-Fed Meeting:**
- Reduce position sizes
- Tighten stop losses
- Increase cash position
- Avoid new positions

**During Fed Announcement:**
- No trading during announcement
- Prepare for volatility spike
- Have trading plan ready
- Monitor market reaction

**Post-Fed Meeting:**
- Wait for initial reaction
- Assess market direction
- Look for trading opportunities
- Implement trading plan

#### 2. Earnings Seasons
**Pre-Earnings:**
- Reduce exposure to reporting stocks
- Tighten stops on existing positions
- Avoid new positions in reporting stocks
- Consider hedging strategies

**During Earnings:**
- No trading during earnings releases
- Monitor post-earnings movement
- Assess gap direction and size
- Prepare for trading opportunities

**Post-Earnings:**
- Wait for initial reaction to settle
- Look for gap fade opportunities
- Assess trend changes
- Implement trading strategies

#### 3. Economic Data Releases
**High-Impact Data:**
- Non-Farm Payrolls
- CPI Inflation Data
- GDP Reports
- Interest Rate Decisions

**Trading Around Data:**
- Reduce position sizes before releases
- Avoid new positions before releases
- Prepare for volatility spikes
- Trade the reaction, not the prediction

**Management Strategies:**
- Wait 5-15 minutes after release
- Assess market direction
- Look for confirmation signals
- Implement trading plan

### Time-Based Trading Rules

#### 1. Session Timing
**Regular Session (9:30-16:00 ET):**
- Highest liquidity
- Best for trend following
- Most indicator reliability
- Standard risk parameters

**Pre-Market (4:00-9:30 ET):**
- Lower liquidity
- Gap trading opportunities
- Higher volatility
- Reduced position sizes

**After-Hours (16:00-20:00 ET):**
- Lowest liquidity
- Earnings moves
- Limited participation
- Very conservative trading

#### 2. Intraday Timing
**Opening Range (9:30-10:30 ET):**
- High volatility
- Gap fills
- Trend establishment
- Increased opportunity

**Mid-Day (10:30-15:00 ET):**
- Trend continuation
- Range development
- Standard patterns
- Normal liquidity

**Close Period (15:00-16:00 ET):**
- Position squaring
- End-of-day trends
- Liquidity changes
- Reversal opportunities

#### 3. Weekly Timing
**Monday:**
- Weekend gap reactions
- Week trend establishment
- Economic data reactions
- Position adjustments

**Tuesday-Thursday:**
- Trend continuation
- Pattern development
- Standard trading
- Normal volatility

**Friday:**
- Position squaring
- Weekly options expiration
- Trend exhaustion
- Weekend risk reduction

### Seasonal and Cyclical Patterns

#### 1. Monthly Patterns
**Beginning of Month:**
- New money inflows
- Positive bias historically
- Trend continuation
- Increased volume

**End of Month:**
- Window dressing
Portfolio rebalancing
- Tax loss harvesting
- Increased volatility

**Quarter-End:**
- Institutional rebalancing
- Large portfolio adjustments
- Increased volatility
- Trend changes

#### 2. Holiday Patterns
**Pre-Holiday:**
- Reduced volume
- Positive bias
- Range-bound trading
- Early closes

**Post-Holiday:**
- Volume return
- Trend establishment
- Increased volatility
- New money deployment

#### 3. Earnings Season Patterns
**Earnings Season Start:**
- Increased volatility
- Sector rotation
- Trend changes
- High beta movement

**Mid-Earnings Season:**
- Sector divergence
- Trend establishment
- Reduced volatility
- Normal patterns

**Earnings Season End:**
- Trend exhaustion
- Consolidation
- Volume reduction
- Position adjustment

---

## Strategy Validation & Testing

### Streamlit Strategy Viewer Testing

#### 1. Strategy Artifact Format
**Required JSON Structure:**
```json
{
  "strategy_name": "Strategy_Name_Timeframe",
  "description": "Clear strategy description",
  "timeframe": "5min|15min|hour|day",
  "symbol": "SPY|QQQ|AAPL",
  "entry_conditions": [...],
  "exit_conditions": [...],
  "risk_management": {...},
  "signals": [...]
}
```

**Signal Format Requirements:**
- Timestamp in market hours (9:30-16:00 ET)
- Correct signal types (entry_long, entry_short, exit_long, exit_short)
- Realistic price levels for symbol/timeframe
- Accurate P&L calculations
- Professional execution language

#### 2. Visual Validation Checklist
**Chart Display:**
- [ ] Arrows appear at correct timestamps
- [ ] Arrow colors match trade direction (green ▲ long, red ▼ short)
- [ ] Candles display correctly for timeframe
- [ ] Indicators plot correctly

**Signal Placement:**
- [ ] Entry signals near intended price levels
- [ ] Exit signals properly paired with entries
- [ ] Reasonable time distance between entries/exits
- [ ] No overlapping or conflicting signals

**Performance Metrics:**
- [ ] Win rate within expected range (40-70%)
- [ ] Profit factor reasonable (>1.0)
- [ ] Average win/loss ratios realistic
- [ ] Maximum drawdown acceptable

#### 3. Execution Log Validation
**Execution Language:**
- Entry Long: "BOUGHT {shares} shares @ ${price}"
- Entry Short: "SOLD SHORT {shares} shares @ ${price}"
- Exit Long: "SOLD {shares} shares @ ${price}"
- Exit Short: "BUY TO COVER {shares} shares @ ${price}"

**Calculation Accuracy:**
- Long P&L: (Exit Price - Entry Price) × Shares
- Short P&L: (Entry Price - Exit Price) × Shares
- R calculations correct
- Position sizing consistent

**Reason Descriptions:**
- Technical conditions clearly stated
- Price levels specified
- Indicator readings included
- Market context provided

### Manual Checkpoint Validation

#### 1. HTF/Daily Setup Validation
**Market Context Review:**
- Does the strategy correctly identify market regime?
- Are higher timeframe trends properly aligned?
- Is market structure correctly interpreted?
- Are key support/resistance levels identified?

**Setup Logic Assessment:**
- Do entry conditions make sense for the regime?
- Are confirmation rules appropriate?
- Is the timeframe hierarchy logical?
- Are invalidators properly implemented?

**Validation Questions:**
- "Does this HTF setup match how you would identify opportunities?"
- "Are the confirmation rules filtering out low-quality setups?"
- "Would this trigger catch the right opportunities without false signals?"

#### 2. Trade Start/Trigger Validation
**Entry Timing Review:**
- Do entries occur at advantageous price levels?
- Is the entry timing consistent with the strategy type?
- Are position building rules appropriate?
- Is initial risk management sound?

**Position Building Assessment:**
- Does pyramiding logic make sense?
- Are add conditions properly specified?
- Is size progression appropriate?
- Are risk management adjustments correct?

**Validation Questions:**
- "Does this entry approach match your style of buying dips/selling rallies?"
- "Is the position building logic consistent with your pyramiding approach?"
- "Would these triggers catch the right entries without chasing?"

#### 3. Execution Accuracy Validation
**Execution Mechanics:**
- Are order types appropriate for the strategy?
- Is stop management logical and implementable?
- Are partial exits properly structured?
- Is recycling logic sound?

**Position Management:**
- Does stop trailing make sense?
- Are breakeven rules appropriate?
- Is position sizing dynamic and logical?
- Are invalidator conditions relevant?

**Validation Questions:**
- "Does the execution reflect your style of hitting pops when short and pullbacks when long?"
- "Are the recycling mechanics implemented correctly for partial covers?"
- "Would this execution build positions the way you want them built?"

### Performance Analysis

#### 1. Key Performance Metrics
**Win Rate Analysis:**
- Calculate: Winning Trades / Total Trades
- Expected ranges: 40-70% depending on strategy type
- Compare to historical performance
- Assess consistency over time

**Profit Factor:**
- Calculate: Gross Profit / Gross Loss
- Minimum acceptable: >1.0
- Good: >1.5
- Excellent: >2.0

**Expectancy:**
- Calculate: (Win Rate × Average Win) - (Loss Rate × Average Loss)
- Positive expectancy required
- Compare to risk-free rate
- Assess consistency

**Maximum Drawdown:**
- Calculate: Largest peak-to-trough decline
- Acceptable ranges: <20% for aggressive, <10% for conservative
- Compare to historical drawdowns
- Assess recovery time

#### 2. Risk-Adjusted Returns
**Sharpe Ratio:**
- Calculate: (Return - Risk-Free Rate) / Standard Deviation
- Good: >1.0
- Excellent: >2.0
- Compare to benchmark

**Sortino Ratio:**
- Calculate: (Return - Risk-Free Rate) / Downside Deviation
- Focuses on downside risk
- Better for asymmetric returns
- Compare to Sharpe ratio

**Calmar Ratio:**
- Calculate: Annual Return / Maximum Drawdown
- Measures return relative to drawdown
- Good: >2.0
- Excellent: >5.0

#### 3. Strategy Comparison
**Benchmark Comparison:**
- Compare to buy-and-hold
- Compare to relevant index
- Compare to similar strategies
- Assess alpha generation

**Peer Comparison:**
- Compare to other strategies
- Assess relative performance
- Identify competitive advantages
- Determine best use cases

**Market Condition Analysis:**
- Performance in different regimes
- Correlation to market conditions
- Adaptability to changing markets
- Robustness assessment

---

## Implementation & Coding

### VectorBT Translation Guide

#### 1. Basic Strategy Structure
**Strategy Class Template:**
```python
import vectorbt as vbt
import pandas as pd
import numpy as np

class Strategy:
    def __init__(self, data, params):
        self.data = data
        self.params = params

    def calculate_indicators(self):
        # Calculate all technical indicators
        pass

    def generate_signals(self):
        # Generate entry/exit signals
        pass

    def calculate_positions(self):
        # Calculate position sizes
        pass

    def run_backtest(self):
        # Execute backtest
        pass
```

**Data Structure Requirements:**
- OHLCV data with proper datetime index
- Timezone-aware timestamps for intraday
- Consistent timeframe alignment
- Clean data without gaps

#### 2. Indicator Implementation
**Moving Averages:**
```python
# EMA Calculation
def calculate_ema(self, price, period):
    return price.ewm(span=period, adjust=False).mean()

# Multiple EMAs
def calculate_ema_cross(self, fast_period=9, slow_period=20):
    fast_ema = self.calculate_ema(self.data['close'], fast_period)
    slow_ema = self.calculate_ema(self.data['close'], slow_period)
    crossover = fast_ema > slow_ema
    return crossover
```

**VWAP Calculation:**
```python
def calculate_vwap(self):
    typical_price = (self.data['high'] + self.data['low'] + self.data['close']) / 3
    vwap = (typical_price * self.data['volume']).cumsum() / self.data['volume'].cumsum()
    return vwap
```

**RSI Calculation:**
```python
def calculate_rsi(self, period=14):
    delta = self.data['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi
```

#### 3. Signal Generation
**Entry Signal Logic:**
```python
def generate_entry_signals(self):
    # Multiple timeframe alignment
    htf_trend = self.calculate_htf_trend()
    mtf_signal = self.calculate_mtf_signal()
    ltf_entry = self.calculate_ltf_entry()

    # Combine timeframes
    entry_signal = htf_trend & mtf_signal & ltf_entry

    return entry_signal
```

**Exit Signal Logic:**
```python
def generate_exit_signals(self, positions):
    # Stop loss
    stop_loss = self.calculate_stop_loss()

    # Take profit
    take_profit = self.calculate_take_profit()

    # Time exit
    time_exit = self.calculate_time_exit()

    # Combine exit conditions
    exit_signal = stop_loss | take_profit | time_exit

    return exit_signal
```

**Position Sizing:**
```python
def calculate_position_size(self, signal, account_value=100000):
    # Risk per trade (1% of account)
    risk_per_trade = account_value * 0.01

    # Stop distance in dollars
    stop_distance = self.calculate_stop_distance()

    # Position size
    position_size = risk_per_trade / stop_distance

    return position_size
```

#### 4. Advanced Features
**Multi-timeframe Analysis:**
```python
def resample_timeframe(self, data, timeframe):
    """Resample data to different timeframe"""
    resampled = data.resample(timeframe).agg({
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last',
        'volume': 'sum'
    })
    return resampled

def align_timeframes(self):
    """Align multiple timeframes"""
    self.htf_data = self.resample_timeframe(self.data, '1D')
    self.mtf_data = self.resample_timeframe(self.data, '1H')
    self.ltf_data = self.data  # Original timeframe
```

**Pyramiding Logic:**
```python
def pyramid_positions(self, entry_signal, base_size):
    """Implement pyramiding strategy"""
    positions = pd.DataFrame(index=self.data.index, columns=['size'])

    # Initial entry
    positions.loc[entry_signal, 'size'] = base_size * 0.25

    # Add at confirmation
    confirmation_signal = self.calculate_confirmation()
    positions.loc[confirmation_signal, 'size'] += base_size * 0.25

    # Add at continuation
    continuation_signal = self.calculate_continuation()
    positions.loc[continuation_signal, 'size'] += base_size * 0.5

    return positions.fillna(0)
```

**Dynamic Stop Management:**
```python
def calculate_trailing_stop(self, positions, atr_period=14):
    """Calculate ATR-based trailing stops"""
    atr = self.calculate_atr(period=atr_period)

    # Initial stop placement
    stop_distance = atr * 2

    # Trail stop logic
    trailing_stop = pd.DataFrame(index=self.data.index, columns=['stop'])

    for i in range(1, len(self.data)):
        if positions.iloc[i] > 0:  # Long position
            if self.data['close'].iloc[i] > trailing_stop['stop'].iloc[i-1]:
                trailing_stop['stop'].iloc[i] = self.data['close'].iloc[i] - stop_distance.iloc[i]
            else:
                trailing_stop['stop'].iloc[i] = trailing_stop['stop'].iloc[i-1]
        elif positions.iloc[i] < 0:  # Short position
            if self.data['close'].iloc[i] < trailing_stop['stop'].iloc[i-1]:
                trailing_stop['stop'].iloc[i] = self.data['close'].iloc[i] + stop_distance.iloc[i]
            else:
                trailing_stop['stop'].iloc[i] = trailing_stop['stop'].iloc[i-1]
        else:
            trailing_stop['stop'].iloc[i] = np.nan

    return trailing_stop
```

### Performance Metrics Calculation

#### 1. Basic Metrics
**Total Return:**
```python
def calculate_total_return(self, portfolio_value):
    initial_value = portfolio_value.iloc[0]
    final_value = portfolio_value.iloc[-1]
    total_return = (final_value - initial_value) / initial_value
    return total_return
```

**Win Rate:**
```python
def calculate_win_rate(self, trades):
    winning_trades = trades[trades['pnl'] > 0]
    win_rate = len(winning_trades) / len(trades)
    return win_rate
```

**Profit Factor:**
```python
def calculate_profit_factor(self, trades):
    gross_profit = trades[trades['pnl'] > 0]['pnl'].sum()
    gross_loss = abs(trades[trades['pnl'] < 0]['pnl'].sum())
    profit_factor = gross_profit / gross_loss if gross_loss > 0 else np.inf
    return profit_factor
```

#### 2. Advanced Metrics
**Sharpe Ratio:**
```python
def calculate_sharpe_ratio(self, returns, risk_free_rate=0.02):
    excess_returns = returns - risk_free_rate / 252  # Daily risk-free rate
    sharpe_ratio = excess_returns.mean() / excess_returns.std() * np.sqrt(252)
    return sharpe_ratio
```

**Maximum Drawdown:**
```python
def calculate_max_drawdown(self, portfolio_value):
    peak = portfolio_value.expanding().max()
    drawdown = (portfolio_value - peak) / peak
    max_drawdown = drawdown.min()
    return max_drawdown
```

**Calmar Ratio:**
```python
def calculate_calmar_ratio(self, returns, max_drawdown):
    annual_return = returns.mean() * 252
    calmar_ratio = annual_return / abs(max_drawdown) if max_drawdown != 0 else np.inf
    return calmar_ratio
```

### Risk Management Implementation

#### 1. Position Sizing
**Fixed Fractional Sizing:**
```python
def fixed_fractional_sizing(self, signal, account_value, risk_fraction=0.01):
    """Fixed fractional position sizing"""
    risk_amount = account_value * risk_fraction
    stop_distance = self.calculate_stop_distance()

    position_size = risk_amount / stop_distance
    return position_size
```

**Volatility-Adjusted Sizing:**
```python
def volatility_adjusted_sizing(self, signal, account_value, base_risk=0.01):
    """Volatility-adjusted position sizing"""
    atr = self.calculate_atr(period=14)
    volatility_factor = atr / atr.rolling(252).mean()  # Relative volatility

    # Reduce size in high volatility
    adjusted_risk = base_risk / volatility_factor
    risk_amount = account_value * adjusted_risk

    stop_distance = atr * 2
    position_size = risk_amount / stop_distance

    return position_size
```

#### 2. Stop Management
**ATR Stop:**
```python
def atr_stop_loss(self, entry_price, atr_multiplier=2, atr_period=14):
    """ATR-based stop loss"""
    atr = self.calculate_atr(period=atr_period)
    stop_distance = atr * atr_multiplier

    if self.position_type == 'long':
        stop_price = entry_price - stop_distance
    else:  # short
        stop_price = entry_price + stop_distance

    return stop_price
```

**Swing Point Stop:**
```python
def swing_point_stop(self, lookback_period=5):
    """Swing point-based stop loss"""
    highs = self.data['high'].rolling(lookback_period).max()
    lows = self.data['low'].rolling(lookback_period).min()

    if self.position_type == 'long':
        stop_price = lows.shift(1)  # Previous swing low
    else:  # short
        stop_price = highs.shift(1)  # Previous swing high

    return stop_price
```

#### 3. Portfolio Management
**Portfolio Class:**
```python
class Portfolio:
    def __init__(self, initial_capital=100000):
        self.initial_capital = initial_capital
        self.current_capital = initial_capital
        self.positions = {}
        self.trades = []
        self.equity_curve = []

    def add_position(self, symbol, size, entry_price, stop_loss):
        """Add new position"""
        position = {
            'symbol': symbol,
            'size': size,
            'entry_price': entry_price,
            'stop_loss': stop_loss,
            'entry_time': pd.Timestamp.now()
        }
        self.positions[symbol] = position

    def update_position(self, symbol, current_price):
        """Update position value and check stops"""
        if symbol in self.positions:
            position = self.positions[symbol]

            # Check stop loss
            if position['size'] > 0 and current_price <= position['stop_loss']:
                self.close_position(symbol, current_price, 'stop_loss')
            elif position['size'] < 0 and current_price >= position['stop_loss']:
                self.close_position(symbol, current_price, 'stop_loss')

    def close_position(self, symbol, exit_price, reason):
        """Close position and record trade"""
        position = self.positions[symbol]

        pnl = (exit_price - position['entry_price']) * position['size']

        trade = {
            'symbol': symbol,
            'entry_price': position['entry_price'],
            'exit_price': exit_price,
            'size': position['size'],
            'pnl': pnl,
            'reason': reason,
            'entry_time': position['entry_time'],
            'exit_time': pd.Timestamp.now()
        }

        self.trades.append(trade)
        del self.positions[symbol]
        self.current_capital += pnl

    def calculate_performance(self):
        """Calculate portfolio performance metrics"""
        if not self.trades:
            return {}

        trades_df = pd.DataFrame(self.trades)

        win_rate = (trades_df['pnl'] > 0).mean()
        total_return = (self.current_capital - self.initial_capital) / self.initial_capital

        return {
            'total_return': total_return,
            'win_rate': win_rate,
            'total_trades': len(self.trades),
            'current_capital': self.current_capital
        }
```

---

## Command Reference

### Available Commands

#### /skeleton - Create Strategy Skeleton
**Usage:** `/skeleton [strategy idea description]`

**Purpose:** Convert a trading idea into a structured skeleton document for strategy development.

**Examples:**
```
/skeleton I want to build a mean reversion strategy for QQQ that fades big morning gaps. When QQQ gaps up more than 1%, I want to short the pop and cover when it returns to VWAP.

/screenshot [analyze chart screenshots]
/video [analyze YouTube video for strategy]
/strategy [generate complete strategy artifact]
/validate [validate strategy against checkpoints]
/optimize [optimize strategy parameters]
/translate [convert strategy to VectorBT code]
/help [show command reference and workflows]
```

**Output:** Structured skeleton document with all sections filled based on strategy description.

#### /video - Analyze Video Content
**Usage:** `/video [YouTube URL or video description]`

**Purpose:** Extract trading strategy rules and concepts from YouTube videos or other video content.

**Examples:**
```
/video https://youtube.com/watch?v=example Extract the VWAP fade strategy rules
/video This video explains a scalping strategy using order flow and volume profiles
```

**Process:**
1. Extract video transcript and content
2. Identify strategy sections and rules
3. Extract specific parameters and indicators
4. Map concepts to structured strategy format
5. Generate skeleton document or strategy artifact

**Output:** Strategy rules extracted from video content in structured format.

#### /screenshot - Analyze Chart Screenshots
**Usage:** `/screenshot [screenshot description or upload]`

**Purpose:** Analyze chart screenshots to extract trading patterns, indicators, and strategy rules.

**Examples:**
```
/screenshot Analyze this chart showing a head and shoulders pattern with volume confirmation
/screenshot This screenshot shows EMA crossover signals with RSI confirmation
```

**Analysis Capabilities:**
- Chart pattern recognition
- Indicator identification
- Entry/exit point mapping
- Support/resistance level identification
- Trend and momentum analysis

**Output:** Strategy rules and patterns extracted from chart analysis.

#### /strategy - Generate Complete Strategy
**Usage:** `/strategy [skeleton document or strategy description]`

**Purpose:** Generate a complete, testable strategy artifact in JSON format.

**Examples:**
```
/strategy [paste skeleton document content]
/strategy Create a complete mean reversion strategy for QQQ on 15min timeframe using VWAP and RSI
```

**Output:** Complete JSON strategy artifact compatible with Streamlit Strategy Viewer.

#### /validate - Validate Strategy
**Usage:** `/validate [strategy artifact or validation request]`

**Purpose:** Validate strategy against manual checkpoints and best practices.

**Examples:**
```
/validate [paste strategy JSON]
/validate Check if this mean reversion strategy meets all checkpoint requirements
```

**Validation Areas:**
- HTF/Daily setup validation
- Trade start/trigger validation
- Execution accuracy validation
- Performance reasonableness checks
- JSON format validation

**Output:** Validation report with pass/fail status and improvement suggestions.

#### /optimize - Optimize Strategy Parameters
**Usage:** `/optimize [strategy artifact + optimization goals]`

**Purpose:** Optimize strategy parameters for better performance.

**Examples:**
```
/optimize [paste strategy] Optimize for higher win rate while maintaining profit factor
/optimize [paste strategy] Optimize entry timing and stop placement for reduced drawdown
```

**Optimization Areas:**
- Indicator parameters
- Entry/exit timing
- Risk management settings
- Position sizing rules
- Timeframe combinations

**Output:** Optimized strategy with improved parameters.

#### /translate - Convert to VectorBT Code
**Usage:** `/translate [strategy artifact]`

**Purpose:** Convert strategy artifact to implementable VectorBT code.

**Examples:**
```
/translate [paste strategy JSON] Convert to complete VectorBT implementation
/translate [paste strategy] Generate backtest code with performance metrics
```

**Output:** VectorBT Python code ready for backtesting and implementation.

#### /help - Command Reference
**Usage:** `/help [specific command or general help]`

**Purpose:** Show command reference and workflow guidance.

**Examples:**
```
/help Show all available commands
/help /skeleton Show detailed help for skeleton command
/help workflow Show complete workflow examples
```

**Output:** Comprehensive help documentation and usage examples.

### Workflow Commands

#### /workflow - Show Complete Workflow
**Usage:** `/workflow [workflow type]`

**Purpose:** Display complete workflow examples for different strategy development paths.

**Examples:**
```
/workflow Show all available workflows
/workflow idea-to-strategy Show workflow from idea to complete strategy
/workflow video-to-strategy Show workflow from video analysis to strategy
/workflow optimization Show workflow for strategy optimization
```

**Output:** Step-by-step workflow documentation with examples.

#### /template - Show Strategy Templates
**Usage:** `/template [strategy type]`

**Purpose:** Show pre-built strategy templates for common trading approaches.

**Examples:**
```
/template Show all available templates
/template mean-reversion Show mean reversion strategy template
/template trend-following Show trend following strategy template
/template breakout Show breakout strategy template
```

**Output:** Ready-to-use strategy templates with parameters and rules.

#### /example - Show Strategy Examples
**Usage:** `/example [example type]`

**Purpose:** Show complete example strategies for reference and learning.

**Examples:**
```
/example Show all available examples
/example simple Show simple strategy examples
/example advanced Show advanced strategy examples
/example multi-timeframe Show multi-timeframe strategy examples
```

**Output:** Complete example strategies with full documentation.

### Advanced Commands

#### /backtest - Run Strategy Backtest
**Usage:** `/backtest [strategy artifact + backtest parameters]`

**Purpose:** Run comprehensive backtest on strategy with historical data.

**Examples:**
```
/backtest [paste strategy] Run backtest on last 6 months of data
/backtest [paste strategy] Backtest with SPY data from 2023-2024
```

**Parameters:**
- Date range for backtest
- Symbol or symbols to test
- Initial capital
- Commission and slippage settings
- Performance metrics to calculate

**Output:** Comprehensive backtest report with performance metrics and equity curve.

#### /compare - Compare Strategies
**Usage:** `/compare [strategy artifacts or descriptions]`

**Purpose:** Compare multiple strategies across key performance metrics.

**Examples:**
```
/compare [strategy1] [strategy2] Compare two strategies side by side
/compare [strategies] Compare mean reversion vs trend following approaches
```

**Comparison Metrics:**
- Win rate and profit factor
- Maximum drawdown and recovery time
- Risk-adjusted returns (Sharpe, Sortino)
- Correlation and diversification benefits

**Output:** Detailed comparison report with recommendations.

#### /analyze - Analyze Market Conditions
**Usage:** `/analyze [market analysis request]`

**Purpose:** Analyze current market conditions and suggest appropriate strategies.

**Examples:**
```
/analyze Analyze current market conditions for QQQ
/analyze What strategies work best in current market regime?
/analyze Analyze volatility and suggest appropriate position sizing
```

**Analysis Areas:**
- Market regime identification
- Volatility analysis
- Trend strength assessment
- Correlation analysis
- Seasonal factors

**Output:** Market analysis report with strategy recommendations.

### Utility Commands

#### /export - Export Strategy
**Usage:** `/export [strategy artifact + export format]`

**Purpose:** Export strategy in various formats for different platforms.

**Examples:**
```
/export [paste strategy] Export as JSON for Streamlit
/export [paste strategy] Export as Python code for VectorBT
/export [paste strategy] Export as documentation
```

**Export Formats:**
- JSON (Streamlit compatible)
- Python (VectorBT implementation)
- Documentation (PDF/Markdown)
- TradingView Pine Script
- Other platform formats

**Output:** Strategy exported in requested format.

#### /import - Import Strategy
**Usage:** `/import [strategy data or file reference]`

**Purpose:** Import strategy from external sources or formats.

**Examples:**
```
/import [JSON data] Import strategy from JSON
/import [file reference] Import strategy from file
/import [TradingView code] Import from TradingView Pine Script
```

**Import Sources:**
- JSON files
- Python code
- TradingView Pine Script
- Other platform formats
- Text descriptions

**Output:** Imported strategy in standard WZRD format.

#### /settings - Configure Settings
**Usage:** `/settings [setting type + configuration]`

**Purpose:** Configure strategy generation settings and preferences.

**Examples:**
```
/settings Show current settings
/set risk-management Set default risk management parameters
/set indicators Set preferred indicator defaults
/set timeframes Set default timeframe preferences
```

**Configuration Areas:**
- Risk management defaults
- Indicator parameters
- Timeframe preferences
- Performance targets
- Validation criteria

**Output:** Settings confirmation and updated configuration.

---

## Workflow Examples

### Workflow 1: Idea to Complete Strategy

#### Step 1: Initial Strategy Idea
**User Input:**
```
/skeleton I want to build a mean reversion strategy for QQQ that fades big morning gaps. When QQQ gaps up more than 1%, I want to short the pop and cover when it returns to VWAP. I like to pyramid into the position as it goes against me.
```

**GPT Response:**
"I understand you want to build a mean reversion strategy for QQQ. Based on your input, I can see this aligns with your style of fading extremes and building positions. Let me create a skeleton document and ask a few clarifying questions..."

**Generated Skeleton:**
- Strategy Type: Mean reversion (short bias)
- Symbol: QQQ
- Timeframe: 5min/15min
- Entry: Gap up >1%, fade the pop
- Exit: Return to VWAP
- Position Building: Pyramid against position
- Risk Management: 1% account risk

**Clarification Questions:**
1. "What specific VWAP anchor do you prefer? (session start, week start, etc.)"
2. "What's your preferred pyramiding sequence? (0.25R → 0.5R → 1R)"
3. "Do you use any confirmation indicators like RSI or volume?"
4. "What's your maximum holding period for gap fades?"

#### Step 2: Strategy Generation
**User Input:**
```
/strategy [paste completed skeleton with answers]
```

**GPT Response:**
"Perfect! Based on your completed skeleton, I'll generate a complete strategy artifact with realistic signals and proper risk management."

**Generated Strategy Artifact:**
```json
{
  "strategy_name": "QQQ_5min_Gap_Fade_Mean_Reversion",
  "description": "Short QQQ when it gaps up more than 1% above VWAP, pyramid against position, cover at VWAP",
  "timeframe": "5min",
  "symbol": "QQQ",
  "entry_conditions": [
    {
      "type": "price_level",
      "description": "Price gaps up >1% above VWAP session start with RSI overbought",
      "direction": "short",
      "indicators": ["vwap", "rsi", "volume"]
    }
  ],
  "exit_conditions": [
    {
      "type": "price_level",
      "description": "Price returns to VWAP or stop loss triggered",
      "direction": "close_short"
    }
  ],
  "risk_management": {
    "stop_loss": {
      "type": "percentage",
      "value": 0.75
    },
    "take_profit": {
      "type": "percentage",
      "value": 1.5
    },
    "position_size": {
      "type": "r_based",
      "value": 1.0
    }
  },
  "signals": [
    {
      "timestamp": "2025-09-26 09:45:00",
      "type": "entry_short",
      "price": 594.50,
      "shares": 300,
      "reason": "Price gapped up 1.4% above VWAP, RSI overbought at 77",
      "execution": "SOLD SHORT 300 shares @ $594.50",
      "calculation": "Entry: $594.50 | Exit: $593.00 | Difference: $1.50 x 300 shares",
      "pnl": 450.0
    }
  ]
}
```

#### Step 3: Streamlit Validation
**User Action:**
- Paste JSON into Streamlit Strategy Viewer
- Review chart visualization
- Check signal placement and arrow colors
- Verify performance metrics

**GPT Guidance:**
"Now let's validate this strategy through the manual checkpoints. Load this into your Streamlit viewer and let me know:

1. Do the arrows appear at the correct gap points?
2. Are the entry prices realistic for gap fades?
3. Does the pyramiding logic make sense on the chart?
4. Are the performance metrics reasonable?"

#### Step 4: Checkpoint Validation
**User Feedback:**
"The gap fade entries look good, but I need more aggressive pyramiding. Also, the RSI confirmation isn't working well - I'd rather use volume confirmation."

**GPT Response:**
"Excellent feedback! Let me optimize the strategy based on your validation results."

**Optimized Strategy:**
- Updated pyramiding: 0.5R initial, 0.5R add, 1.0R total
- Changed confirmation from RSI to volume spike
- Added gap size filtering
- Optimized timing windows

#### Step 5: Final Validation
**User:**
"Perfect! The optimized strategy looks great in Streamlit. The signals are exactly what I want."

**GPT Response:**
"Excellent! Now let's create the final PRD document for ClaudeCode implementation."

**Final Output:**
- Complete PRD document
- VectorBT code translation
- Implementation specifications
- Testing and deployment guidelines

---

### Workflow 2: Video Analysis to Strategy

#### Step 1: Video Analysis Request
**User Input:**
```
/video https://youtube.com/watch?v=example Extract the VWAP trading strategy rules
```

**GPT Response:**
"I'll analyze this YouTube video to extract the VWAP trading strategy rules and concepts."

**Video Analysis Process:**
1. Extract video transcript and content
2. Identify strategy sections and rules
3. Extract specific parameters and indicators
4. Map concepts to structured format

**Extracted Strategy Elements:**
- Strategy Type: VWAP mean reversion
- Timeframes: 15min setup, 5min execution
- Entry: Price extension from VWAP
- Exit: Return to VWAP
- Confirmation: Volume spike
- Risk Management: ATR-based stops

#### Step 2: Strategy Skeleton Generation
**GPT Response:**
"Based on the video analysis, I've extracted the core strategy rules. Here's a structured skeleton document. Please review and fill in any missing details."

**Generated Skeleton:**
- Strategy Name: VWAP Mean Reversion (from video)
- Core Concept: Fade price extensions from VWAP
- Timeframes: 15min for setup, 5min for execution
- Entry Rules: Price >1% from VWAP + volume spike
- Exit Rules: Return to VWAP or ATR stop
- Risk Management: ATR-based position sizing

**Clarification Questions:**
1. "What specific VWAP anchor does the video recommend?"
2. "What's the exact volume spike threshold for confirmation?"
3. "How many ATR for stop placement?"
4. "What's the preferred position sizing approach?"

#### Step 3: Complete Strategy Generation
**User Input:**
```
/strategy [completed skeleton with video-specific parameters]
```

**GPT Response:**
"Perfect! I'll generate a complete strategy artifact based on the video rules and your parameter specifications."

**Generated Strategy:**
- Complete JSON with video-based rules
- Realistic signal generation
- Proper risk management
- Professional execution logs

#### Step 4: Validation and Testing
**User Action:**
- Test strategy in Streamlit viewer
- Compare with video examples
- Validate signal timing and logic
- Check performance reasonableness

**GPT Response:**
"Let's validate this strategy against the video examples and best practices. How do the signals compare to what was shown in the video?"

#### Step 5: Final Implementation
**User:**
"The strategy matches the video concepts perfectly! The signals are exactly what was demonstrated."

**GPT Response:**
"Excellent! Now let's create the complete implementation package including VectorBT code and documentation."

**Final Output:**
- Complete strategy documentation
- VectorBT implementation code
- Testing and deployment guide
- Performance optimization suggestions

---

### Workflow 3: Strategy Optimization

#### Step 1: Strategy Performance Analysis
**User Input:**
```
/optimize [paste underperforming strategy] The win rate is too low at 35%, need to improve entry timing
```

**GPT Response:**
"I'll analyze this strategy and optimize it to improve the win rate while maintaining profitability."

**Performance Analysis:**
- Current win rate: 35%
- Profit factor: 1.2
- Maximum drawdown: 15%
- Main issue: Poor entry timing

**Optimization Areas:**
- Entry timing refinement
- Additional confirmation filters
- Stop loss adjustment
- Position sizing optimization

#### Step 2: Parameter Optimization
**GPT Response:**
"Based on the analysis, I'll optimize the key parameters to improve entry timing and win rate."

**Optimized Parameters:**
- Added RSI filter for entry timing
- Tightened stop loss from 1.5% to 1.0%
- Added volume confirmation
- Optimized entry timing windows

#### Step 3: Validation and Testing
**User Action:**
- Test optimized strategy in Streamlit
- Compare performance with original
- Validate improvements
- Check for over-optimization

**GPT Response:**
"The optimized strategy shows significant improvements. Let me validate these results and ensure we haven't over-optimized."

**Validation Results:**
- Win rate improved: 35% → 48%
- Profit factor maintained: 1.2 → 1.3
- Drawdown reduced: 15% → 10%
- No signs of over-optimization

#### Step 4: Final Implementation
**User:**
"Excellent! The optimized strategy performs much better while maintaining the core logic."

**GPT Response:**
"Perfect! Here's the complete optimized strategy package with documentation and implementation code."

**Final Output:**
- Optimized strategy artifact
- Performance comparison report
- Implementation specifications
- Monitoring and maintenance guidelines

---

## Troubleshooting & FAQ

### Common Issues

#### 1. JSON Format Errors
**Issue:** "Invalid JSON format in strategy artifact"

**Causes:**
- Missing required fields
- Incorrect data types
- Malformed JSON syntax
- Missing commas or brackets

**Solutions:**
- Use JSON validator to check syntax
- Ensure all required fields are present
- Verify correct data types (numbers vs strings)
- Check for proper comma and bracket placement

**Example Fix:**
```json
// Incorrect
"risk_management": {
  "stop_loss": "0.75"  // String instead of number
}

// Correct
"risk_management": {
  "stop_loss": 0.75  // Number
}
```

#### 2. Signal Timing Issues
**Issue:** "Signals appear at wrong times or don't trigger"

**Causes:**
- Timestamps outside market hours
- Incorrect timezone handling
- Signal logic errors
- Indicator calculation issues

**Solutions:**
- Ensure timestamps are during market hours (9:30-16:00 ET)
- Use timezone-aware timestamps for intraday strategies
- Verify signal logic matches intended rules
- Check indicator parameters and calculations

**Example Fix:**
```json
// Incorrect
"timestamp": "2025-09-26 08:30:00"  // Pre-market

// Correct
"timestamp": "2025-09-26 09:45:00"  // Market hours
```

#### 3. P&L Calculation Errors
**Issue:** "P&L calculations are incorrect"

**Causes:**
- Wrong formula for short positions
- Missing position size in calculations
- Incorrect entry/exit price matching
- Missing calculation field

**Solutions:**
- Use correct formula: Short P&L = (Entry - Exit) × Shares
- Include position size in all calculations
- Ensure proper entry/exit pair matching
- Add calculation field for transparency

**Example Fix:**
```json
// Short position P&L
"pnl": 450.0,  // (594.50 - 593.00) × 300
"calculation": "Entry: $594.50 | Exit: $593.00 | Difference: $1.50 x 300 shares"
```

#### 4. Arrow Color Issues
**Issue:** "Arrow colors are wrong in Streamlit"

**Causes:**
- Incorrect signal type mapping
- Color logic errors
- Trade direction confusion

**Solutions:**
- Long entries: Green ▲
- Long exits: Red ▼
- Short entries: Red ▼
- Short exits: Green ▲

**Example Fix:**
```json
// Short exit should be green arrow
{
  "type": "exit_short",
  "reason": "Covered at VWAP",
  "execution": "BUY TO COVER 300 shares @ $593.00"
}
```

### Performance Issues

#### 1. Low Win Rate
**Symptoms:** Win rate below 40% consistently

**Causes:**
- Entry timing too early/late
- Insufficient confirmation filters
- Poor stop loss placement
- Wrong market regime for strategy

**Solutions:**
- Add confirmation indicators
- Tighten entry criteria
- Optimize stop loss placement
- Add market regime filters

#### 2. High Drawdown
**Symptoms:** Drawdown exceeds 20%

**Causes:**
- Position size too large
- Stop loss too wide
- No position sizing adjustments
- Poor risk management

**Solutions:**
- Reduce position size
- Tighten stop loss
- Add volatility-based sizing
- Implement maximum drawdown stops

#### 3. Low Profit Factor
**Symptoms:** Profit factor below 1.0

**Causes:**
- Average loss larger than average win
- Too many losing trades
- Poor risk-reward ratio
- Inadequate exit strategy

**Solutions:**
- Improve risk-reward ratio
- Add confirmation filters
- Optimize take profit levels
- Implement trailing stops

### Implementation Issues

#### 1. VectorBT Translation Errors
**Issue:** "Strategy doesn't translate properly to VectorBT"

**Causes:**
- Complex logic not easily translatable
- Missing indicator implementations
- Multi-timeframe alignment issues
- Discrete vs continuous signal handling

**Solutions:**
- Simplify complex logic
- Implement custom indicators
- Use proper timeframe alignment
- Handle signal discretization

#### 2. Backtest Performance Mismatch
**Issue:** "Backtest results don't match Streamlit results"

**Causes:**
- Different data sources
- Slippage and commission assumptions
- Signal timing differences
- Position sizing calculations

**Solutions:**
- Use same data source
- Include transaction costs
- Align signal timing
- Match position sizing logic

#### 3. Live Trading Issues
**Issue:** "Live performance doesn't match backtest"

**Causes:**
- Market regime changes
- Liquidity issues
- Slippage larger than expected
- Over-optimization

**Solutions:**
- Implement regime detection
- Add liquidity filters
- Account for slippage
- Use robust optimization methods

### User Interface Issues

#### 1. Command Not Recognized
**Issue:** "Command not found or not working"

**Causes:**
- Typo in command name
- Missing required parameters
- Command not available
- Formatting issues

**Solutions:**
- Check command spelling
- Verify required parameters
- Use `/help` for available commands
- Check input formatting

#### 2. Output Format Issues
**Issue:** "Output format is not as expected"

**Causes:**
- Wrong output type requested
- Missing export options
- Formatting errors
- Display limitations

**Solutions:**
- Specify desired output format
- Use appropriate export command
- Check formatting requirements
- Use multiple smaller outputs

### Data Issues

#### 1. Missing or Incorrect Data
**Issue:** "Strategy references data that doesn't exist"

**Causes:**
- Incorrect symbol names
- Wrong timeframe specifications
- Missing indicator calculations
- Data source issues

**Solutions:**
- Verify symbol names
- Check timeframe availability
- Implement indicator calculations
- Use reliable data sources

#### 2. Timezone Issues
**Issue:** "Timestamps are in wrong timezone"

**Causes:**
- Missing timezone information
- Incorrect timezone conversion
- Daylight saving time issues
- Market hour assumptions

**Solutions:**
- Use timezone-aware timestamps
- Convert to proper timezone (ET)
- Handle daylight saving time
- Respect market hours

### Strategy Logic Issues

#### 1. Contradictory Rules
**Issue:** "Strategy rules contradict each other"

**Causes:**
- Overlapping conditions
- Conflicting signals
- Logic errors
- Poor strategy design

**Solutions:**
- Review rule logic
- Remove contradictions
- Implement signal hierarchy
- Test edge cases

#### 2. Missing Edge Cases
**Issue:** "Strategy doesn't handle edge cases"

**Causes:**
- Incomplete rule coverage
- Missing market conditions
- Unusual price action
- Extreme volatility

**Solutions:**
- Add edge case handling
- Implement market regime filters
- Add volatility adjustments
- Test extreme scenarios

---

## Glossary & Terminology

### Trading Terms

#### A
- **Accumulation:** Market phase where institutional buyers are accumulating positions
- **ADR (Average Daily Range):** Average price range over a specified period
- **ADX (Average Directional Index):** Indicator measuring trend strength
- **ATR (Average True Range):** Volatility indicator measuring average price range
- **Auction Market:** Market where prices are determined by matching buy and sell orders

#### B
- **Backtesting:** Testing strategy performance on historical data
- **Base Currency:** First currency in a currency pair
- **Bear Market:** Market condition with falling prices
- **Bull Market:** Market condition with rising prices
- **Breakout:** Price movement beyond established support/resistance

#### C
- **Candlestick:** Price chart showing open, high, low, close for a period
- **Channel:** Price movement between two parallel trend lines
- **Confirmation:** Additional indicators validating a signal
- **Consolidation:** Price movement in a range with no clear trend
- **Correlation:** Statistical relationship between two assets

#### D
- **Day Trading:** Opening and closing positions within the same day
- **Distribution:** Market phase where institutional sellers are distributing positions
- **Divergence:** Price and indicator moving in opposite directions
- **Drawdown:** Peak-to-trough decline in portfolio value
- **Double Top/Bottom:** Reversal pattern with two peaks/troughs at similar levels

#### E
- **Earnings:** Company profit reports that can cause price volatility
- **EMA (Exponential Moving Average):** Moving average giving more weight to recent prices
- **Entry Signal:** Signal indicating when to open a position
- **Exit Signal:** Signal indicating when to close a position
- **Equity Curve:** Graph showing portfolio value over time

#### F
- **Fibonacci:** Mathematical ratios used for support/resistance levels
- **Flag:** Continuation pattern resembling a flag on a flagpole
- **Fade:** Trading against the current price move
- **Fill:** Execution of an order at a specific price
- **Fundamental Analysis:** Analysis based on financial and economic factors

#### G
- **Gap:** Price difference between close and next open
- **Gap Fill:** Price returning to fill a previous gap
- **Gross Profit:** Total profit from winning trades
- **Gross Loss:** Total loss from losing trades

#### H
- **Head and Shoulders:** Reversal pattern with three peaks
- **Hedge:** Position taken to offset risk of another position
- **Higher Highs/Lows:** Price pattern indicating uptrend
- **Highs and Lows:** Peak and trough points in price movement

#### I
- **Indicator:** Mathematical calculation based on price and/or volume
- **Inside Bar:** Candle with high/low within previous candle's range
- **Insider Trading:** Trading based on non-public information
- **Institutional:** Large financial organizations trading in markets

#### L
- **Leverage:** Using borrowed capital to increase position size
- **Liquidity:** Ease of buying/selling without affecting price
- **Long:** Position that profits from price increases
- **Lower Highs/Lows:** Price pattern indicating downtrend

#### M
- **MACD (Moving Average Convergence Divergence):** Momentum indicator
- **Margin:** Borrowed money for trading
- **Market Order:** Order to buy/sell at current market price
- **Momentum:** Rate of price change
- **Moving Average:** Average price over specified period

#### O
- **Order Flow:** Flow of buy and sell orders
- **Overbought:** Condition where asset is considered overvalued
- **Oversold:** Condition where asset is considered undervalued
- **Outside Bar:** Candle with high/low outside previous candle's range

#### P
- **P&L (Profit and Loss):** Financial result of trading activities
- **Pattern:** Recognizable formation in price charts
- **Pivot Point:** Key support/resistance level
- **Position:** Open trade in the market
- **Profit Factor:** Ratio of gross profit to gross loss
- **Pullback:** Temporary price movement against main trend

#### R
- **R (Risk Multiple):** Unit of risk measurement
- **Rally:** Sustained price increase
- **Range:** Price movement between support and resistance
- **Reversal:** Change in price direction
- **Resistance:** Price level where selling pressure increases
- **Retracement:** Temporary price movement against main trend
- **Risk Management:** Techniques to minimize trading risk
- **RSI (Relative Strength Index):** Momentum oscillator
- **Round Numbers:** Psychological price levels (e.g., 100, 50)

#### S
- **Scalping:** Very short-term trading for small profits
- **Setup:** Specific market conditions for trading
- **Sharpe Ratio:** Risk-adjusted performance measure
- **Short:** Position that profits from price decreases
- **Slippage:** Difference between expected and actual execution price
- **SMA (Simple Moving Average):** Unweighted moving average
- **Spread:** Difference between bid and ask prices
- **Stop Loss:** Order to limit potential loss
- **Support:** Price level where buying pressure increases
- **Swing Trading:** Medium-term trading holding positions for days/weeks
- **Symmetry:** Balance between similar patterns or movements

#### T
- **Take Profit:** Order to close position at profit target
- **Technical Analysis:** Analysis of price charts and indicators
- **Timeline:** Period over which trading occurs
- **Trend:** General direction of price movement
- **Triangle:** Chart pattern with converging trend lines
- **Trailing Stop:** Stop loss that moves with price
- **Trend Line:** Line drawn along price highs or lows

#### V
- **Volatility:** Rate of price fluctuation
- **Volume:** Number of shares/contracts traded
- **VWAP (Volume Weighted Average Price):** Average price weighted by volume

#### W
- **Whipsaw:** Rapid price movement causing false signals
- **Win Rate:** Percentage of profitable trades
- **With Trend:** Trading in direction of main trend

### Technical Analysis Terms

#### Indicator Types
- **Leading Indicators:** Indicators that predict future price movements
- **Lagging Indicators:** Indicators that confirm price movements
- **Oscillators:** Indicators that oscillate between fixed levels
- **Momentum Indicators:** Indicators measuring rate of price change
- **Volume Indicators:** Indicators based on trading volume
- **Volatility Indicators:** Indicators measuring price volatility

#### Pattern Types
- **Reversal Patterns:** Patterns indicating trend reversal
- **Continuation Patterns:** Patterns indicating trend continuation
- **Bilateral Patterns:** Patterns that can signal reversal or continuation
- **Harmonic Patterns:** Patterns based on Fibonacci ratios
- **Candlestick Patterns:** Patterns formed by individual candles

#### Chart Types
- **Line Chart:** Simple chart showing closing prices
- **Bar Chart:** Chart showing open, high, low, close
- **Candlestick Chart:** Chart showing price action with candlesticks
- **Point and Figure Chart:** Chart focusing on price movements
- **Renko Chart:** Chart showing price movements with bricks

### Risk Management Terms

#### Position Sizing
- **Fixed Fractional:** Risking fixed percentage of account per trade
- **Fixed Dollar:** Risking fixed dollar amount per trade
- **Volatility Adjusted:** Sizing based on market volatility
- **Kelly Criterion:** Mathematical formula for optimal position sizing
- **Optimal F:** Position sizing to maximize growth

#### Stop Loss Types
- **Fixed Stop:** Stop at fixed price level
- **Trailing Stop:** Stop that moves with price
- **ATR Stop:** Stop based on Average True Range
- **Swing Point Stop:** Stop at recent swing high/low
- **Time Stop:** Stop based on holding period

#### Performance Metrics
- **Win Rate:** Percentage of winning trades
- **Profit Factor:** Gross profit divided by gross loss
- **Expectancy:** Expected profit per trade
- **Sharpe Ratio:** Risk-adjusted return measure
- **Sortino Ratio:** Risk-adjusted return focusing on downside risk
- **Calmar Ratio:** Return relative to maximum drawdown
- **Maximum Drawdown:** Largest peak-to-trough decline

### Strategy Terms

#### Strategy Types
- **Trend Following:** Strategies that follow established trends
- **Mean Reversion:** Strategies that bet on price returning to mean
- **Breakout:** Strategies that bet on price breaking out of ranges
- **Scalping:** Very short-term trading strategies
- **Swing Trading:** Medium-term trading strategies
- **Position Trading:** Long-term trading strategies

#### Timeframes
- **Scalping:** Seconds to minutes
- **Day Trading:** Minutes to hours
- **Swing Trading:** Days to weeks
- **Position Trading:** Weeks to months
- **Investing:** Months to years

#### Market Conditions
- **Trending Market:** Market with clear directional movement
- **Range-Bound Market:** Market moving between support and resistance
- **Volatile Market:** Market with large price movements
- **Quiet Market:** Market with small price movements
- **Liquid Market:** Market with high trading volume
- **Illiquid Market:** Market with low trading volume

### Technology Terms

#### Backtesting
- **VectorBT:** Python library for backtesting
- **Pandas:** Python library for data manipulation
- **NumPy:** Python library for numerical operations
- **Historical Data:** Past price and volume data
- **Walk-Forward Analysis:** Rolling window backtesting
- **Out-of-Sample Testing:** Testing on unseen data

#### Implementation
- **Algorithmic Trading:** Automated trading using algorithms
- **API (Application Programming Interface):** Interface for software communication
- **JSON (JavaScript Object Notation):** Data format for strategy artifacts
- **Python:** Programming language used for implementation
- **Streamlit:** Web framework for strategy visualization
- **Polygon API:** Data source for market data

#### Data Formats
- **OHLCV:** Open, High, Low, Close, Volume data format
- **Time Series:** Data indexed by time
- **Timestamp:** Date and time information
- **Timezone:** Geographic time specification
- **Resampling:** Converting data between timeframes

### Trading Psychology Terms

#### Emotional States
- **Fear:** Emotion causing hesitation or early exits
- **Greed:** Emotion causing overtrading or excessive risk
- **FOMO (Fear of Missing Out):** Emotion causing chasing trades
- **Revenge Trading:** Emotional trading after losses
- **Overconfidence:** Excessive belief in trading abilities

#### Psychological Biases
- **Confirmation Bias:** Seeking information confirming existing beliefs
- **Loss Aversion:** Preference for avoiding losses over acquiring gains
- **Recency Bias:** Overweighting recent events
- **Anchoring:** Relying too heavily on first information
- **Hindsight Bias:** Believing past events were predictable

#### Discipline Terms
- **Trading Plan:** Written plan for trading activities
- **Trading Journal:** Record of trading activities and analysis
- **Risk Rules:** Rules for managing trading risk
- **Emotional Control:** Managing emotions while trading
- **Patience:** Waiting for high-probability setups

### Market Structure Terms

#### Market Participants
- **Retail Traders:** Individual traders
- **Institutional Traders:** Large financial organizations
- **Market Makers:** Firms providing liquidity
- **High-Frequency Traders:** Traders using high-speed algorithms
- **Hedge Funds:** Investment funds using various strategies

#### Market Microstructure
- **Order Book:** List of buy and sell orders
- **Bid Price:** Highest price buyers are willing to pay
- **Ask Price:** Lowest price sellers are willing to accept
- **Spread:** Difference between bid and ask prices
- **Depth:** Amount of orders at different price levels
- **Liquidity:** Ability to execute large orders without price impact

#### Trading Sessions
- **Pre-Market:** Trading before regular session
- **Regular Session:** Main trading hours
- **After-Hours:** Trading after regular session
- **Extended Hours:** Pre-market and after-hours trading
- **Globex:** Extended trading hours for futures

---

*This comprehensive knowledge base provides the WZRD Strategy Generator with all necessary information to create, validate, and implement professional trading strategies across the entire development lifecycle.*