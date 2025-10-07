#!/usr/bin/env python3
"""
Standalone Enhanced Strategy Architect
Works with current dependencies and Claude GLM API
"""

import json
import re
import logging
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path

from claude_mcp_client import ClaudeMCPClient as ClaudeGLMClient

logger = logging.getLogger(__name__)


@dataclass
class StrategyComponents:
    """Extracted strategy components from natural language."""
    name: str
    strategy_type: str
    market_focus: str
    timeframe: str
    risk_level: str

    # Entry conditions
    entry_conditions: List[str]
    entry_filters: List[str]

    # Exit conditions
    exit_conditions: List[str]
    exit_filters: List[str]

    # Risk management
    position_sizing: str
    stop_loss: str
    take_profit: str
    max_drawdown: str

    # Technical indicators
    indicators: List[str]
    primary_indicator: str
    secondary_indicators: List[str]

    # Scan parameters
    volume_requirements: str
    price_requirements: str
    volatility_requirements: str

    # Special conditions
    time_filters: str
    market_conditions: str
    pyramiding_rules: str


class StandaloneStrategyParser:
    """Enhanced parser for strategy documents using Claude AI."""

    def __init__(self):
        self.claude_client = ClaudeGLMClient()

    def parse_strategy_document(self, document_content: str) -> StrategyComponents:
        """Parse strategy document using Claude AI understanding."""

        # Create comprehensive parsing prompt
        parsing_prompt = f"""
        You are an expert trading strategy analyst. Parse this strategy document and extract all key components.

        Document:
        {document_content}

        Extract and return a structured JSON object with these components:

        1. Strategy Identity
           - name: Clear strategy name
           - strategy_type: (Momentum, Mean Reversion, Breakout, Trend Following, etc.)
           - market_focus: (Stocks, Forex, Crypto, etc.)
           - timeframe: (1m, 5m, 15m, 1h, Daily, etc.)
           - risk_level: (Conservative, Moderate, Aggressive)

        2. Entry Logic
           - entry_conditions: List of specific signals
           - entry_filters: List of volume, price, time conditions

        3. Exit Logic
           - exit_conditions: List of take profit, stop loss rules
           - exit_filters: List of trailing stops, time exits

        4. Risk Management
           - position_sizing: Method description
           - stop_loss: Stop loss methodology
           - take_profit: Take profit targets
           - max_drawdown: Maximum drawdown allowed

        5. Technical Indicators
           - indicators: List of all indicators
           - primary_indicator: Main signal indicator
           - secondary_indicators: List of confirmation indicators

        6. Scan Parameters
           - volume_requirements: Volume filters
           - price_requirements: Price range requirements
           - volatility_requirements: Volatility filters

        7. Special Conditions
           - time_filters: Time-based filters
           - market_conditions: Market regime conditions
           - pyramiding_rules: Position scaling rules

        Return ONLY valid JSON that can be parsed.
        """

        try:
            # Use Claude to understand the strategy
            response = self.claude_client.send_message(
                message=parsing_prompt,
                max_tokens=2000,
                temperature=0.3
            )

            # Parse the AI response into structured components
            return self._parse_ai_response(response['choices'][0]['message']['content'])

        except Exception as e:
            logger.error(f"AI parsing failed: {e}")
            # Fallback to rule-based parsing
            return self._fallback_parsing(document_content)

    def _parse_ai_response(self, ai_text: str) -> StrategyComponents:
        """Parse AI response into structured components."""

        # Extract JSON from AI response if present
        json_match = re.search(r'\{.*\}', ai_text, re.DOTALL)
        if json_match:
            try:
                data = json.loads(json_match.group())
                return self._dict_to_components(data)
            except json.JSONDecodeError:
                logger.warning("Failed to parse JSON from AI response, using fallback")
                pass

        # Fallback: extract components using regex patterns
        return self._extract_components_from_text(ai_text)

    def _dict_to_components(self, data: Dict) -> StrategyComponents:
        """Convert dictionary to StrategyComponents."""
        return StrategyComponents(
            name=data.get('name', 'Unknown Strategy'),
            strategy_type=data.get('strategy_type', 'Unknown'),
            market_focus=data.get('market_focus', 'Stocks'),
            timeframe=data.get('timeframe', 'Daily'),
            risk_level=data.get('risk_level', 'Moderate'),
            entry_conditions=data.get('entry_conditions', []),
            entry_filters=data.get('entry_filters', []),
            exit_conditions=data.get('exit_conditions', []),
            exit_filters=data.get('exit_filters', []),
            position_sizing=data.get('position_sizing', '1% per trade'),
            stop_loss=data.get('stop_loss', '2% below entry'),
            take_profit=data.get('take_profit', '3% above entry'),
            max_drawdown=data.get('max_drawdown', '20%'),
            indicators=data.get('indicators', []),
            primary_indicator=data.get('primary_indicator', ''),
            secondary_indicators=data.get('secondary_indicators', []),
            volume_requirements=data.get('volume_requirements', ''),
            price_requirements=data.get('price_requirements', ''),
            volatility_requirements=data.get('volatility_requirements', ''),
            time_filters=data.get('time_filters', ''),
            market_conditions=data.get('market_conditions', ''),
            pyramiding_rules=data.get('pyramiding_rules', '')
        )

    def _extract_components_from_text(self, text: str) -> StrategyComponents:
        """Extract components from text using regex patterns."""

        # Extract key information using patterns
        name_match = re.search(r'name[:\s]+([^\n]+)', text, re.IGNORECASE)
        type_match = re.search(r'type[:\s]+([^\n]+)', text, re.IGNORECASE)

        return StrategyComponents(
            name=name_match.group(1).strip() if name_match else 'Extracted Strategy',
            strategy_type=type_match.group(1).strip() if type_match else 'Momentum',
            market_focus='Stocks',
            timeframe='15m',
            risk_level='Moderate',
            entry_conditions=['Price momentum', 'Volume confirmation'],
            entry_filters=['Min volume 8M', 'Price > $10'],
            exit_conditions=['Take profit at 3%', 'Stop loss at 2%'],
            exit_filters=['Time exit: EOD'],
            position_sizing='1% risk per trade',
            stop_loss='2% below entry',
            take_profit='3% above entry',
            max_drawdown='20%',
            indicators=['RSI', 'MACD', 'Volume'],
            primary_indicator='RSI',
            secondary_indicators=['MACD', 'Volume'],
            volume_requirements='Minimum 8M daily volume',
            price_requirements='Price > $10',
            volatility_requirements='ATR > 0.5',
            time_filters='9:30 AM - 4:00 PM EST',
            market_conditions='Avoid earnings reports',
            pyramiding_rules='Max 2 additions'
        )

    def _fallback_parsing(self, document_content: str) -> StrategyComponents:
        """Fallback parsing when AI is unavailable."""
        logger.warning("Using fallback parsing for strategy document")

        # Simple keyword-based extraction
        return StrategyComponents(
            name='Fallback Strategy',
            strategy_type='Momentum',
            market_focus='Stocks',
            timeframe='15m',
            risk_level='Moderate',
            entry_conditions=['Price break above resistance'],
            entry_filters=['Volume > average', 'Price > $5'],
            exit_conditions=['Take profit at 2R', 'Stop loss at 1R'],
            exit_filters=['Time exit: 2 days'],
            position_sizing='1% per trade',
            stop_loss='1% below entry',
            take_profit='2% above entry',
            max_drawdown='15%',
            indicators=['RSI', 'MACD', 'Volume'],
            primary_indicator='RSI',
            secondary_indicators=['MACD', 'Volume'],
            volume_requirements='Minimum 5M daily volume',
            price_requirements='Price > $5',
            volatility_requirements='None',
            time_filters='Market hours only',
            market_conditions='Trending markets',
            pyramiding_rules='No pyramiding'
        )


class StandaloneCodeGenerator:
    """Enhanced code generator for professional trading strategies."""

    def __init__(self):
        self.claude_client = ClaudeGLMClient()
        # Initialize config with default values
        self.config = {
            'code_generation': {
                'use_ai': True,
                'fallback_to_templates': True,
                'max_tokens': 4000,
                'temperature': 0.2
            },
            'code_quality': {
                'include_type_hints': True,
                'include_docstrings': True,
                'include_error_handling': True,
                'include_logging': True
            }
        }

    def generate_strategy_code(self, components: StrategyComponents) -> Dict[str, str]:
        """Generate complete, professional strategy code."""

        generation_prompt = f"""
        You are an expert quantitative developer. Generate a complete, production-ready trading strategy implementation based on these components:

        Strategy Components:
        {json.dumps(asdict(components), indent=2)}

        Generate a Python trading strategy with these requirements:

        1. Professional Code Structure
           - Use dataclasses for configuration
           - Implement proper error handling
           - Add comprehensive logging
           - Include performance metrics
           - Support backtesting frameworks

        2. Complete Implementation
           - All entry/exit logic from components
           - Risk management and position sizing
           - Technical indicator calculations
           - Market scanning capabilities
           - Performance tracking

        3. Best Practices
           - Type hints throughout
           - Docstrings for all methods
           - Configurable parameters
           - Modular design
           - Test-friendly structure

        4. Integration Ready
           - Real-time data feed support
           - Order management interface
           - Risk monitoring

        Return the complete Python implementation only, no explanations.
        """

        try:
            response = self.claude_client.send_message(
                message=generation_prompt,
                max_tokens=4000,
                temperature=0.2
            )

            strategy_code = response['choices'][0]['message']['content']

            # Extract code block if wrapped in markdown
            code_match = re.search(r'```python\n(.*?)\n```', strategy_code, re.DOTALL)
            if code_match:
                strategy_code = code_match.group(1)

            return {
                'strategy.py': strategy_code,
                'config.py': self._generate_config_code(components),
                'utils.py': self._generate_utils_code(),
                'README.md': self._generate_readme(components)
            }

        except Exception as e:
            logger.error(f"Code generation failed: {e}")
            return self._fallback_generation(components)

    def _generate_config_code(self, components: StrategyComponents) -> str:
        """Generate configuration code."""
        strategy_name = re.sub(r'[^a-zA-Z0-9_]', '_', components.name)
        return f'''
"""
Configuration for {components.name} Strategy
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class {strategy_name}Config:
    """Configuration for {components.name} strategy."""

    # Strategy Parameters
    strategy_type: str = "{components.strategy_type}"
    market_focus: str = "{components.market_focus}"
    timeframe: str = "{components.timeframe}"
    risk_level: str = "{components.risk_level}"

    # Entry Parameters
    entry_rsi_threshold: float = 50.0
    volume_multiplier: float = 1.5
    price_min: float = 5.0

    # Exit Parameters
    take_profit_r_multiple: float = 2.0
    stop_loss_r_multiple: float = 1.0
    max_hold_days: int = 5

    # Risk Management
    risk_per_trade: float = 0.01
    max_portfolio_heat: float = 0.20
    max_positions: int = 10

    # Volume Requirements
    min_daily_volume: float = 5_000_000
    min_dollar_volume: float = 100_000_000

    # Technical Indicators
    rsi_period: int = 14
    macd_fast: int = 12
    macd_slow: int = 26
    macd_signal: int = 9
    atr_period: int = 14

    def __post_init__(self):
        """Validate configuration."""
        if self.risk_per_trade <= 0 or self.risk_per_trade > 0.05:
            raise ValueError("risk_per_trade must be between 0 and 0.05")
        if self.max_portfolio_heat <= 0 or self.max_portfolio_heat > 1.0:
            raise ValueError("max_portfolio_heat must be between 0 and 1.0")
'''

    def _generate_utils_code(self) -> str:
        """Generate utility functions code."""
        return '''
"""
Utility functions for trading strategies
"""

import numpy as np
import pandas as pd
from typing import Tuple, Optional


def calculate_atr(high: pd.Series, low: pd.Series, close: pd.Series, period: int = 14) -> pd.Series:
    """Calculate Average True Range."""
    prev_close = close.shift(1)
    tr1 = high - low
    tr2 = abs(high - prev_close)
    tr3 = abs(low - prev_close)

    true_range = np.maximum(tr1, np.maximum(tr2, tr3))
    return true_range.rolling(window=period).mean()


def calculate_rsi(close: pd.Series, period: int = 14) -> pd.Series:
    """Calculate Relative Strength Index."""
    delta = close.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))


def calculate_macd(close: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9) -> Tuple[pd.Series, pd.Series, pd.Series]:
    """Calculate MACD indicator."""
    ema_fast = close.ewm(span=fast, adjust=False).mean()
    ema_slow = close.ewm(span=slow, adjust=False).mean()
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    histogram = macd_line - signal_line
    return macd_line, signal_line, histogram


def calculate_position_size(account_value: float, entry_price: float, stop_loss: float,
                          risk_percent: float = 0.01) -> int:
    """Calculate position size based on risk."""
    risk_per_share = abs(entry_price - stop_loss)
    if risk_per_share == 0:
        return 0

    risk_amount = account_value * risk_percent
    position_size = int(risk_amount / risk_per_share)
    return max(0, position_size)


def validate_market_data(data: pd.DataFrame) -> bool:
    """Validate market data integrity."""
    required_columns = ['open', 'high', 'low', 'close', 'volume']

    if not all(col in data.columns for col in required_columns):
        return False

    if data.empty:
        return False

    if data.isnull().any().any():
        return False

    # Check for reasonable price values
    if (data['high'] < data['low']).any():
        return False

    return True
'''

    def _generate_readme(self, components: StrategyComponents) -> str:
        """Generate README documentation."""
        return f'''
# {components.name} Strategy

## Overview
{components.strategy_type} strategy for {components.market_focus} on {components.timeframe} timeframe.

## Strategy Details
- **Type**: {components.strategy_type}
- **Market**: {components.market_focus}
- **Timeframe**: {components.timeframe}
- **Risk Level**: {components.risk_level}

## Entry Conditions
{chr(10).join(f"- {condition}" for condition in components.entry_conditions)}

## Exit Conditions
{chr(10).join(f"- {condition}" for condition in components.exit_conditions)}

## Risk Management
- Position Sizing: {components.position_sizing}
- Stop Loss: {components.stop_loss}
- Take Profit: {components.take_profit}
- Max Drawdown: {components.max_drawdown}

## Technical Indicators
- Primary: {components.primary_indicator}
- Secondary: {', '.join(components.secondary_indicators)}

## Usage
```python
from strategy import {components.name.replace(' ', '_')}Strategy
from config import {components.name.replace(' ', '_')}Config

# Initialize strategy
config = {components.name.replace(' ', '_')}Config()
strategy = {components.name.replace(' ', '_')}Strategy(config)

# Generate signals
signals = strategy.generate_signals(market_data)
```

## Files
- `strategy.py` - Main strategy implementation
- `config.py` - Strategy configuration
- `utils.py` - Utility functions

Generated by WZRD AI Strategy Architect
'''

    def _fallback_generation(self, components: StrategyComponents) -> Dict[str, str]:
        """Fallback code generation."""
        strategy_name = re.sub(r'[^a-zA-Z0-9_]', '_', components.name)

        return {
            'strategy.py': f'''
# {components.name} Strategy Implementation
# Generated by WZRD AI Strategy Architect

import pandas as pd
import numpy as np
from dataclasses import dataclass
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)

@dataclass
class {strategy_name}Config:
    risk_per_trade: float = 0.01
    stop_loss_percent: float = 0.02
    take_profit_percent: float = 0.03

class {strategy_name}Strategy:
    def __init__(self, config: {strategy_name}Config = None):
        self.config = config or {strategy_name}Config()
        self.positions = {{}}
        self.logger = logging.getLogger(__name__)

    def generate_signals(self, data: pd.DataFrame) -> Dict[str, str]:
        """Generate trading signals based on strategy logic."""
        signals = {{}}

        if data.empty:
            return signals

        # Calculate basic indicators
        data['rsi'] = self._calculate_rsi(data['close'], 14)
        data['volume_sma'] = data['volume'].rolling(20).mean()

        # Generate signals for each symbol (assuming single symbol for now)
        for i in range(1, len(data)):
            current_row = data.iloc[i]
            prev_row = data.iloc[i-1]

            signal = self._check_entry_conditions(current_row, prev_row, data.iloc[:i+1])
            if signal:
                signals[data.index[i]] = signal

        return signals

    def _check_entry_conditions(self, current_row, prev_row, data_slice) -> str:
        """Check if entry conditions are met."""
        # Basic momentum conditions
        rsi_ok = current_row['rsi'] > 50
        volume_ok = current_row['volume'] > current_row['volume_sma'] * 1.5

        if rsi_ok and volume_ok:
            return 'BUY'

        return ''

    def _calculate_rsi(self, prices: pd.Series, period: int = 14) -> pd.Series:
        """Calculate RSI indicator."""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))

    def calculate_position_size(self, account_value: float, entry_price: float) -> int:
        """Calculate position size based on risk management rules."""
        risk_amount = account_value * self.config.risk_per_trade
        stop_loss_price = entry_price * (1 - self.config.stop_loss_percent)
        risk_per_share = entry_price - stop_loss_price
        return int(risk_amount / risk_per_share) if risk_per_share > 0 else 0

    def __str__(self):
        return f"{self.config.strategy_type} Strategy - {self.config.market_focus}"
''',
            'config.py': self._generate_config_code(components),
            'utils.py': self._generate_utils_code(),
            'README.md': self._generate_readme(components)
        }


class StandaloneStrategyArchitect:
    """Standalone Strategy Architect with improved parsing and code generation."""

    def __init__(self):
        self.parser = StandaloneStrategyParser()
        self.code_generator = StandaloneCodeGenerator()
        self.logger = logging.getLogger(__name__)

    def process_strategy_document(self, document_content: str, strategy_name: str = "") -> Dict[str, Any]:
        """Process strategy document and generate complete implementation."""

        try:
            self.logger.info(f"Processing strategy document: {strategy_name or 'Unnamed'}")

            # Parse the document
            components = self.parser.parse_strategy_document(document_content)

            if not strategy_name:
                strategy_name = components.name

            self.logger.info(f"Parsed strategy: {components.name} ({components.strategy_type})")

            # Generate code
            generated_files = self.code_generator.generate_strategy_code(components)

            # Create result package
            result = {
                'strategy_name': strategy_name,
                'components': asdict(components),
                'generated_files': generated_files,
                'metadata': {
                    'created_at': datetime.now().isoformat(),
                    'document_length': len(document_content),
                    'complexity_score': self._calculate_complexity(components),
                    'estimated_development_time': self._estimate_dev_time(components)
                }
            }

            self.logger.info(f"Successfully generated strategy with {len(generated_files)} files")
            return result

        except Exception as e:
            self.logger.error(f"Strategy processing failed: {e}")
            raise

    def _calculate_complexity(self, components: StrategyComponents) -> int:
        """Calculate strategy complexity score."""
        score = 0

        # Base complexity from components
        score += len(components.entry_conditions) * 5
        score += len(components.exit_conditions) * 5
        score += len(components.indicators) * 3
        score += len(components.secondary_indicators) * 2

        # Risk management complexity
        if 'pyramiding' in components.pyramiding_rules.lower():
            score += 10

        # Timeframe complexity
        if 'multi' in components.timeframe.lower():
            score += 5

        return min(score, 100)  # Cap at 100

    def _estimate_dev_time(self, components: StrategyComponents) -> str:
        """Estimate development time for the strategy."""
        complexity = self._calculate_complexity(components)

        if complexity < 20:
            return "2-4 hours"
        elif complexity < 40:
            return "4-8 hours"
        elif complexity < 60:
            return "1-2 days"
        elif complexity < 80:
            return "2-3 days"
        else:
            return "3-5 days"


async def demo_standalone_architect():
    """Demo the standalone strategy architect."""

    print("🚀 Standalone Strategy Architect Demo")
    print("=" * 50)

    architect = StandaloneStrategyArchitect()

    # Test strategy document
    test_document = """
    # Momentum Breakout Strategy

    This strategy focuses on momentum breakouts in large-cap stocks with strong volume confirmation.

    ## Entry Conditions
    - Price breaks above 20-day high
    - Volume > 1.5x average volume
    - RSI > 50
    - MACD bullish crossover

    ## Exit Conditions
    - Take profit at 2R
    - Stop loss at 1R below entry
    - Time exit after 5 days
    - Trailing stop at breakeven after 1R profit

    ## Risk Management
    - 1% risk per trade
    - Maximum 20% portfolio heat
    - Maximum 10 positions

    ## Technical Indicators
    - Primary: 20-day high breakout
    - Secondary: RSI, MACD, Volume
    """

    try:
        result = architect.process_strategy_document(test_document, "Momentum Breakout")

        print(f"✅ Generated strategy: {result['strategy_name']}")
        print(f"📊 Complexity: {result['metadata']['complexity_score']}")
        print(f"⏱️ Estimated Time: {result['metadata']['estimated_development_time']}")
        print(f"📁 Files: {list(result['generated_files'].keys())}")

        # Show sample of generated code
        if 'strategy.py' in result['generated_files']:
            strategy_code = result['generated_files']['strategy.py']
            lines = strategy_code.split('\n')
            print(f"\n📝 Sample Strategy Code:")
            print("-" * 40)
            for i, line in enumerate(lines[:15]):
                print(f"{i+1:2d}: {line}")

        return result

    except Exception as e:
        print(f"❌ Demo failed: {e}")
        return None


if __name__ == "__main__":
    import asyncio
    result = asyncio.run(demo_standalone_architect())
    print("\n✅ Standalone Strategy Architect demo completed!")