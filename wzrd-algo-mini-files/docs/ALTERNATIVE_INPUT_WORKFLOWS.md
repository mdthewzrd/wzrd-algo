# Alternative Input Workflows for Strategy Generation

## Workflow Overview

The strategy generation process supports multiple starting points. Each workflow ultimately produces a completed **Skeleton Document** that serves as the foundation for strategy creation.

---

## Workflow 1: Paragraph Idea Input

### Process Flow
```
User Input → GPT Analysis → Skeleton Document → Strategy Generation
```

### GPT Analysis Steps
1. **Extract Core Concepts**
   - Identify timeframe preferences
   - Determine strategy type (swing, intraday, scalping)
   - Extract entry/exit logic
   - Identify risk management approach

2. **Clarification Questions**
   - "What's your preferred timeframe for setup?"
   - "What indicators do you typically use?"
   - "How do you manage position sizing?"
   - "What's your risk tolerance per trade?"

3. **Skeleton Document Generation**
   - Fill in known sections
   - Flag areas needing clarification
   - Suggest parameters based on your trading style

### Example User Input
*"I want to build a mean reversion strategy for QQQ that fades big morning gaps. When QQQ gaps up more than 1%, I want to short the pop and cover when it returns to VWAP. I like to pyramid into the position as it goes against me."*

### GPT Response
"I understand you want to build a mean reversion strategy for QQQ. Based on your input, I can see this aligns with your style of fading extremes and building positions. Let me create a skeleton document and ask a few clarifying questions..."

[Proceeds to fill skeleton with known info, asks about specific timeframes, indicators, risk parameters]

---

## Workflow 2: Screenshot/Chart Analysis

### Process Flow
```
User Screenshots → GPT Chart Analysis → Pattern Recognition → Skeleton Document → Strategy Generation
```

### GPT Analysis Steps
1. **Chart Pattern Recognition**
   - Identify timeframe (check timestamps, candles)
   - Recognize patterns (head and shoulders, flags, trends)
   - Detect indicators visible on chart
   - Note support/resistance levels

2. **Strategy Logic Extraction**
   - Determine entry points (arrows, annotations)
   - Identify exit conditions (lines, text)
   - Extract stop loss levels
   - Note position sizing clues

3. **Skeleton Document Generation**
   - Map chart patterns to strategy sections
   - Fill in technical indicators used
   - Document entry/exit logic
   - Ask clarification on missing elements

### Example Screenshot Types
- **Annotated Chart Entries:** Entry arrows, stop lines, targets
- **Multi-timeframe Charts:** HTF setup + LTF execution
- **Indicator Setups:** EMA crossovers, VWAP bounces, RSI extremes
- **Pattern Examples:** Flags, triangles, head and shoulders

### GPT Questions for Screenshots
- "What timeframe is this chart?"
- "What indicators are you using that aren't visible?"
- "Is this a HTF setup or LTF execution?"
- "What's your position sizing approach here?"

---

## Workflow 3: Video/Article Analysis

### Process Flow
```
Video/Article → Transcript Extraction → Strategy Rule Extraction → Skeleton Document → Strategy Generation
```

### GPT Analysis Steps
1. **Content Processing**
   - Extract transcript (video) or text (article)
   - Identify strategy sections and rules
   - Extract specific parameters and indicators
   - Note examples and case studies

2. **Strategy Rule Mapping**
   - Convert narrative to structured rules
   - Extract entry/exit conditions
   - Identify risk management parameters
   - Document timeframe specifications

3. **Skeleton Document Generation**
   - Convert video/article rules to skeleton format
   - Fill in all technical details
   - Note multiple strategies if present
   - Ask for clarification on ambiguous points

### Video Analysis Capabilities
- **YouTube Strategy Videos:** Extract rules, parameters, examples
- **Trading Course Content:** Convert lessons to strategy format
- **Market Analysis Videos:** Extract actionable rules
- **Backtest Results:** Analyze performance metrics

### Article Analysis Capabilities
- **Trading Blog Posts:** Convert concepts to strategies
- **Research Papers:** Extract quantitative rules
- **Strategy Guides:** Document step-by-step processes
- **Market Commentaries:** Extract actionable insights

### Example Video Input
User: *"Watch this YouTube video about the VWAP fade strategy and create a skeleton document for it: [YouTube link]"

### GPT Response
"I've analyzed the VWAP fade strategy video. Here's what I extracted:

**Core Strategy:** Fade price extensions above/below VWAP
**Timeframes:** 5min execution, 15min context
**Entry Rules:** Wait for 1% extension from VWAP
**Exit Rules:** Target return to VWAP, stop at 1.5x extension

I've created a skeleton document, but need clarification on:
1. What's your preferred position sizing approach?
2. Do you use any confirmation indicators?
3. How do you handle multiple entries in one session?"

---

## Workflow 4: Existing Strategy Analysis

### Process Flow
```
Existing Strategy → Performance Analysis → Optimization Ideas → Skeleton Document → Enhanced Strategy Generation
```

### Analysis Types
1. **Test Strategy Files:** Analyze your JSON artifacts
2. **Backtest Results:** Review performance metrics
3. **Trade Logs:** Extract winning/losing patterns
4. **Execution Records:** Identify timing improvements

### Enhancement Opportunities
- **Parameter Optimization:** Adjust stops, targets, sizing
- **Timeframe Refinements:** Better HTF/LTF combinations
- **Indicator Additions:** New confirmation tools
- **Risk Management:** Improved position building

---

## Multi-Strategy Handling

### When Content Contains Multiple Strategies
1. **Strategy Separation**
   - Identify distinct strategy boundaries
   - Create separate skeleton documents
   - Note interdependencies between strategies

2. **Strategy Integration**
   - Determine how strategies complement each other
   - Identify shared risk management
   - Document portfolio-level considerations

3. **User Selection**
   - Present strategy options
   - Recommend based on trading style
   - Suggest testing priority

---

## Quality Assurance

### Input Validation
- **Completeness Check:** Ensure all critical sections covered
- **Clarity Verification:** Confirm understanding of strategy logic
- **Feasibility Assessment:** Verify strategy can be implemented
- **Style Alignment:** Ensure matches your trading personality

### Clarification Protocol
1. **Missing Parameters:** Ask for specific values
2. **Ambiguous Rules:** Request exact conditions
3. **Conflicting Logic:** Point out contradictions
4. **Style Mismatches:** Note deviations from your approach

---

## Integration with Main Workflow

### Connection to Streamlit Validation
- All workflows produce **Strategy Artifacts** for testing
- Generate **multiple test cases** for validation
- Include **checkpoint questions** for manual review
- Provide **expected performance metrics** for comparison

### Preparation for Final PRD
- Document **all decision points** during creation
- Note **assumptions made** by GPT
- Record **clarifications provided** by user
- Track **optimization suggestions** discovered

---

*These workflows ensure that regardless of input method, the GPT produces comprehensive, testable strategy artifacts that align with your trading style and validation process.*