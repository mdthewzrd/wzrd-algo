# Final PRD Strategy Document Structure

## Overview

The Final Product Requirements Document (PRD) is the comprehensive, detailed strategy specification that serves as the exact blueprint for VectorBT implementation. This document is created only after successful validation through the streamlined workflow: **Web Chat → Signal Codifier → Strategy Viewer → Validation**.

## Streamlined Workflow Context

### Your Role in the Process
As the WZRD Strategy Generator, you create strategy specifications that flow through the streamlined workflow:

1. **Web Chat (You)**: Create strategy JSON specifications
2. **Signal Codifier**: Generate code-true signals using real market data
3. **Strategy Viewer**: Visual verification and performance analysis
4. **Validation**: Manual checkpoint validation
5. **Final PRD (You)**: Comprehensive implementation document

### Key Advantages
- **Code-True Signals**: All signals computed by actual market data and rules
- **Visual Verification**: See signals on real charts before implementation
- **Perfect VectorBT Compatibility**: Ensured by the Signal Codifier
- **Rapid Iteration**: Quick feedback loop for strategy refinement

---

## Document Structure

### 1. Executive Summary

#### 1.1 Strategy Overview
- **Strategy Name:** Final, approved name
- **Strategy Classification:** [Swing/Intraday/Scalping/Position]
- **Target Markets:** [Specific symbols, market types]
- **Timeframes:** [HTF, MTF, LTF specifications]
- **Strategy Type:** [Trend Following/Mean Reversion/Breakout/etc.]

#### 1.2 Performance Expectations
- **Expected Win Rate:** [Percentage with confidence interval]
- **Expected Profit Factor:** [Target range]
- **Expected Expectancy:** [$ per R risked]
- **Sharpe Ratio Target:** [Risk-adjusted return target]
- **Max Drawdown Limit:** [Acceptable drawdown %]
- **Trade Frequency:** [Trades per period]

#### 1.3 Market Conditions
- **Bull Market Performance:** [Expected characteristics]
- **Bear Market Performance:** [Expected characteristics]
- **Sideways Market Performance:** [Expected characteristics]
- **High Volatility Performance:** [Expected characteristics]
- **Low Volatility Performance:** [Expected characteristics]

### 2. Complete Strategy Rules

#### 2.1 Higher Timeframe Rules (HTF)
- **HTF Definition:** [Daily/Hourly/etc. with exact specifications]
- **Market Structure Rules:** [Trend definition, regime detection]
- **Setup Conditions:** [Exact conditions that must be met]
- **Filter Rules:** [What filters out bad setups]
- **Confirmation Rules:** [What confirms a valid setup]

#### 2.2 Medium Timeframe Rules (MTF)
- **MTF Definition:** [15min/Hourly/etc. with exact specifications]
- **Trigger Conditions:** [Exact trigger logic]
- **Timing Rules:** [When triggers are valid]
- **Entry Signal Rules:** [Precise entry conditions]
- **Position Sizing Rules:** [How initial size is determined]

#### 2.3 Lower Timeframe Rules (LTF)
- **LTF Definition:** [5min/2min/1min with exact specifications]
- **Execution Rules:** [Precise execution logic]
- **Entry Timing Rules:** [Exact entry timing conditions]
- **Scaling Rules:** [How and when to add to positions]
- **Exit Timing Rules:** [When and how to exit]

### 3. Technical Specifications

#### 3.1 Indicator Requirements
- **Primary Indicators:** [List with exact parameters]
- **Secondary Indicators:** [List with exact parameters]
- **Custom Indicators:** [Any custom code or calculations]
- **Indicator Settings:** [Exact parameter values]

#### 3.2 Data Requirements
- **Timeframe Data:** [Specific timeframes needed]
- **Historical Data:** [Lookback periods required]
- **Real-time Data:** [Real-time data requirements]
- **Market Data:** [Specific market data requirements]

#### 3.3 Code Specifications
- **Language:** [Python/Pine Script/Other]
- **Libraries:** [Specific libraries and versions]
- **Dependencies:** [External dependencies]
- **API Requirements:** [Any API calls needed]

### 4. Position Management

#### 4.1 Initial Position Sizing
- **Risk Per Trade:** [Exact percentage or R multiple]
- **Position Sizing Method:** [Exact calculation method]
- **Account Size Considerations:** [How account size affects sizing]
- **Maximum Position Size:** [Absolute maximum size limits]

#### 4.2 Position Building (Pyramiding)
- **Scaling In Rules:** [Exact rules for adding to positions]
- **Add Conditions:** [When to add more]
- **Add Sizing:** [How much to add each time]
- **Maximum Additions:** [Maximum number of additions]

#### 4.3 Position Reduction
- **Partial Exit Rules:** [When and how much to exit]
- **Profit Taking Rules:** [When to take profits]
- **Stop Loss Rules:** [When and how to move stops]
- **Breakeven Rules:** [When to move to breakeven]

### 5. Risk Management

#### 5.1 Stop Loss Management
- **Initial Stop Placement:** [Exact rules for initial stop]
- **Stop Trailing Rules:** [How and when to trail stops]
- **Stop Tightening Rules:** [How and when to tighten stops]
- **Time-based Stops:** [Time-based exit rules]

#### 5.2 Risk per Trade
- **Account Risk Percentage:** [Exact percentage]
- **R Multiple Definition:** [How R is calculated]
- **Maximum Daily Risk:** [Total risk per day]
- **Correlation Risk:** [How to handle correlated positions]

#### 5.3 Portfolio Level Risk
- **Maximum Concurrent Positions:** [Number of positions]
- **Sector Concentration:** [Sector exposure limits]
- **Market Exposure:** [Total market exposure limits]
- **Drawdown Controls:** [How to handle drawdowns]

### 6. Execution Logic

#### 6.1 Order Types
- **Entry Orders:** [Market/Limit/Stop order types]
- **Exit Orders:** [Market/Limit/Stop order types]
- **Order Timing:** [When to place orders]
- **Order Duration:** [How long orders remain active]

#### 6.2 Execution Rules
- **Entry Execution:** [How entries are executed]
- **Exit Execution:** [How exits are executed]
- **Partial Execution:** [How partial fills are handled]
- **Rejection Handling:** [How order rejections are handled]

#### 6.3 Special Execution Cases
- **Gap Handling:** [How to handle gaps]
- **Volatility Handling:** [How to handle high volatility]
- **Low Liquidity Handling:** [How to handle low liquidity]
- **Market Close Handling:** [How to handle market close]

### 7. Trade Management

#### 7.1 In-Trade Management
- **Active Position Monitoring:** [How positions are monitored]
- **Adjustment Rules:** [When and how to adjust positions]
- **Hedging Rules:** [When and how to hedge]
- **Scaling Rules:** [When and how to scale]

#### 7.2 Exit Management
- **Profit Target Rules:** [When to take profits]
- **Stop Loss Rules:** [When to cut losses]
- **Time Exit Rules:** [When to exit based on time]
- **Condition Exit Rules:** [When to exit based on conditions]

#### 7.3 Trade Completion
- **Trade Review:** [How completed trades are reviewed]
- **Performance Analysis:** [How trade performance is analyzed]
- **Strategy Adjustment:** [How strategy is adjusted based on performance]
- **Documentation:** [How trades are documented]

### 8. Performance Metrics

#### 8.1 Required Metrics
- **Win Rate:** [How it's calculated]
- **Profit Factor:** [How it's calculated]
- **Expectancy:** [How it's calculated]
- **Sharpe Ratio:** [How it's calculated]
- **Max Drawdown:** [How it's calculated]
- **Average Trade:** [How it's calculated]

#### 8.2 Monitoring Requirements
- **Real-time Monitoring:** [What needs to be monitored in real-time]
- **Daily Monitoring:** [What needs to be monitored daily]
- **Weekly Monitoring:** [What needs to be monitored weekly]
- **Monthly Monitoring:** [What needs to be monitored monthly]

#### 8.3 Performance Thresholds
- **Minimum Win Rate:** [Threshold for strategy validity]
- **Minimum Profit Factor:** [Threshold for strategy validity]
- **Maximum Drawdown:** [Threshold for strategy halt]
- **Performance Review:** [When to review performance]

### 9. Validation Documentation

#### 9.1 Streamlit Validation Results
- **Test Strategy Performance:** [Results from Streamlit testing]
- **Visual Validation:** [Screenshots and observations]
- **Checkpoint Results:** [Results from manual checkpoint validation]
- **Performance Metrics:** [Actual vs expected performance]

#### 9.2 Backtest Requirements
- **Historical Period:** [Period for backtesting]
- **Market Conditions:** [Market conditions to test]
- **Slippage Assumptions:** [Slippage assumptions]
- **Commission Assumptions:** [Commission assumptions]

#### 9.3 Forward Testing Requirements
- **Paper Trading Period:** [Duration for paper trading]
- **Live Testing Period:** [Duration for live testing]
- **Position Sizing:** [Position sizing for testing]
- **Risk Limits:** [Risk limits during testing]

### 10. Implementation Specifications

#### 10.1 Code Structure
- **File Organization:** [How code should be organized]
- **Class Structure:** [Object-oriented design requirements]
- **Function Specifications:** [Required functions and their specifications]
- **Data Structures:** [Required data structures]

#### 10.2 Integration Requirements
- **API Integration:** [Required API integrations]
- **Database Requirements:** [Database requirements]
- **User Interface:** [User interface requirements]
- **Reporting Requirements:** [Reporting requirements]

#### 10.3 Deployment Requirements
- **Environment:** [Development/production environment requirements]
- **Dependencies:** [Required dependencies and versions]
- **Configuration:** [Configuration requirements]
- **Monitoring:** [Monitoring and logging requirements]

### 11. Appendices

#### 11.1 Glossary
- **Trading Terms:** [Definitions of trading terms used]
- **Technical Terms:** [Definitions of technical terms]
- **Strategy-Specific Terms:** [Definitions of strategy-specific terms]

#### 11.2 Reference Materials
- **Related Strategies:** [Links to related strategies]
- **Market Data Sources:** [Market data source information]
- **Indicator Documentation:** [Indicator documentation links]
- **Code Examples:** [Relevant code examples]

#### 11.3 Change History
- **Version History:** [Document version history]
- **Changes Made:** [Changes made in each version]
- **Validation Results:** [Validation results for each version]
- **Performance Impact:** [Performance impact of changes]

---

## Document Status and Sign-off

### Final Approval Checklist
- [ ] Strategy validated in Streamlit viewer
- [ ] All three checkpoints passed
- [ ] Performance metrics meet expectations
- [ ] All edge cases documented
- [ ] Implementation specifications complete
- [ ] Risk management rules comprehensive
- [ ] Code requirements detailed
- [ ] Testing requirements defined

### Approval Status
- **Strategy Name:** [Strategy Name]
- **Version:** [Version Number]
- **Validation Date:** [Date of final validation]
- **Approved By:** [Your Name]
- **Implementation Ready:** [Yes/No]
- **Next Steps:** [Recommended next actions]

---

## Integration with ClaudeCode

### Handoff Requirements
- **Complete Documentation:** All sections must be complete
- **Tested Strategy:** Strategy must be validated in Streamlit
- **Clear Specifications:** Implementation requirements must be clear
- **Performance Data:** Performance expectations must be documented

### Success Criteria
- **Clear Understanding:** ClaudeCode can implement without clarification
- **Complete Coverage:** All aspects of strategy are documented
- **Testable:** Strategy can be backtested and validated
- **Maintainable:** Documentation supports future maintenance

---

*This final PRD structure ensures that every aspect of the strategy is documented in sufficient detail for ClaudeCode implementation, with no ambiguity or gaps in the specification.*