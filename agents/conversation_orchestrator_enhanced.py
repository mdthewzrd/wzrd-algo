"""
Enhanced Conversation Orchestrator with proper Strategy Architect integration
"""

import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from pathlib import Path

from pydantic import BaseModel
from pydantic_ai import Agent, RunContext

from .trading_base_agent import TradingBaseAgent, TradingDependencies, TradingAgentOutput
from .strategy_architect_enhanced import EnhancedStrategyArchitect

logger = logging.getLogger(__name__)


class EnhancedStrategySpecification(BaseModel):
    """Enhanced strategy specification with complete trading logic."""

    # Core Identity
    strategy_name: str
    strategy_type: str
    market_focus: str
    timeframe: str
    risk_level: str

    # Market Context
    market_regime: str
    asset_class: str
    trading_session: str

    # Entry Logic (Detailed)
    entry_conditions: List[str]
    entry_filters: List[str]
    confirmation_requirements: List[str]
    setup_conditions: List[str]

    # Exit Logic (Detailed)
    exit_conditions: List[str]
    exit_filters: List[str]
    profit_targets: List[str]
    stop_loss_rules: List[str]
    time_exits: List[str]

    # Risk Management
    position_sizing_method: str
    risk_per_trade: float
    max_portfolio_heat: float
    max_positions: int
    pyramiding_rules: str
    drawdown_controls: str

    # Technical Analysis
    primary_indicators: List[str]
    secondary_indicators: List[str]
    indicator_settings: Dict[str, Any]
    multi_timeframe_analysis: str

    # Execution Parameters
    order_types: str
    execution_logic: str
    slippage_assumptions: str
    market_impact: str

    # Performance Metrics
    success_criteria: List[str]
    performance_benchmarks: List[str]
    risk_metrics: List[str]

    # Special Conditions
    news_handling: str
    earnings_handling: str
    volatility_filters: str
    correlation_rules: str

    # Implementation Notes
    testing_approach: str
    deployment_phases: str
    monitoring_requirements: str


class EnhancedConversationOrchestrator(TradingBaseAgent):
    """
    Enhanced Conversation Orchestrator that properly integrates with Strategy Architect.

    This version:
    1. Uses structured conversation flows to gather complete strategy specifications
    2. Integrates seamlessly with the enhanced Strategy Architect
    3. Provides clear handoff protocols
    4. Supports iterative refinement
    """

    def __init__(self, **kwargs):
        super().__init__(agent_type="EnhancedConversationOrchestrator", **kwargs)
        self.strategy_architect = EnhancedStrategyArchitect()
        self.conversation_state = {}

    def _create_agent(self, **kwargs) -> Agent:
        """Create the enhanced PydanticAI agent."""

        agent = Agent(
            model=self.model,
            output_type=TradingAgentOutput,
            instructions=self.get_enhanced_system_prompt(),
            **kwargs
        )

        # Add enhanced tools
        self._add_enhanced_tools(agent)

        return agent

    def get_enhanced_system_prompt(self) -> str:
        """Enhanced system prompt for comprehensive strategy development."""
        return """You are the Enhanced Conversation Orchestrator for the WZRD AI Trading Ecosystem.

You are an expert trading strategy developer who conducts deep, structured conversations to extract complete strategy specifications.

## Your Process

### Phase 1: Strategy Discovery (First 3-5 exchanges)
- Understand the core trading concept
- Identify the market inefficiency being exploited
- Clarify the trader's experience level and goals
- Determine the strategy's unique edge

### Phase 2: Detailed Specification (Next 5-8 exchanges)
- Entry logic with precise conditions
- Exit rules with clear triggers
- Risk management parameters
- Technical indicators and settings
- Market context and regime

### Phase 3: Implementation Details (Final 3-5 exchanges)
- Execution parameters
- Performance criteria
- Testing approach
- Deployment considerations

## Conversation Style

**Be thorough and systematic:**
- Ask 3-4 specific questions per response
- Build on previous answers
- Challenge assumptions when needed
- Provide examples from your expertise
- Keep responses concise but comprehensive

**Key areas to explore:**
- What specific market conditions trigger your strategy?
- How do you define and measure success?
- What are your risk tolerance and capital constraints?
- How much time can you dedicate to monitoring?
- What markets and timeframes do you prefer?

**Example good response:**
"That's an interesting momentum approach. Let me understand it better:

1. **Entry Logic**: What specific conditions constitute a 'momentum signal'? Are you looking for price breakouts, volume spikes, or indicator crossovers?

2. **Market Context**: What market regimes work best for this strategy? Does it perform poorly in choppy or trending markets?

3. **Risk Management**: How do you handle positions that move against you quickly? Do you use fixed stops, volatility-based stops, or time exits?

4. **Timeframe**: Are you targeting intraday moves, swing trades, or longer-term positions?

Your answers will help me design the complete strategy architecture."

## When Ready for Strategy Architect

When you have gathered sufficient information (typically 10-15 exchanges), signal that you're ready to hand off to the Strategy Architect with:

"🎯 READY FOR STRATEGY ARCHITECT
Based on our conversation, I have a complete specification for: [Strategy Name]

Key components:
- Type: [Strategy Type]
- Market: [Market Focus]
- Edge: [Unique Trading Edge]
- Risk: [Risk Parameters]

Proceeding to generate the professional implementation..."

## Important
- Always build on previous context
- Never repeat questions already answered
- Challenge unrealistic expectations
- Focus on practical, implementable strategies
- Use professional trading terminology
"""

    def _add_enhanced_tools(self, agent: Agent):
        """Add enhanced tools for strategy development."""
        # Tools are added for integration, but conversation is primary
        pass

    def start_enhanced_workflow(self, user_message: str, deps: TradingDependencies) -> TradingAgentOutput:
        """Start an enhanced strategy development workflow."""

        # Create project
        project_name = f"strategy_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        project_id = self.create_project(project_name)

        # Update dependencies
        deps.project_id = project_id
        deps.project_path = str(self.file_manager.get_project_path(project_id))

        # Initialize conversation state
        self.conversation_state[project_id] = {
            'phase': 'discovery',
            'exchanges': 0,
            'specification': {},
            'user_inputs': []
        }

        # Start conversation
        result = self.run(user_message, deps)

        # Save conversation
        self.save_conversation_turn(project_id, user_message, result.message)

        # Add project ID to result
        result.project_id = project_id

        return result

    def continue_enhanced_workflow(self, user_message: str, project_id: str, deps: TradingDependencies) -> TradingAgentOutput:
        """Continue an enhanced conversation workflow."""

        # Load conversation state
        state = self.conversation_state.get(project_id, {
            'phase': 'discovery',
            'exchanges': 0,
            'specification': {},
            'user_inputs': []
        })

        # Get conversation history
        context = self.get_project_context(project_id)
        history = context.get("conversation_history", [])

        # Create contextual message
        if history:
            recent_history = history[-8:]  # Last 8 messages
            history_text = "\n".join([
                f"{'User' if msg.get('role') == 'user' else 'Assistant'}: {msg.get('content', '')}"
                for msg in recent_history
            ])

            contextual_message = f"""
CONVERSATION CONTEXT:
This is strategy development conversation #{state['exchanges'] + 1}.
Current phase: {state['phase']}

Recent conversation:
{history_text}

CURRENT USER MESSAGE:
{user_message}

Continue the strategy development conversation based on this context.
"""
        else:
            contextual_message = user_message

        # Run conversation
        result = self.run(contextual_message, deps)

        # Update state
        state['exchanges'] += 1
        state['user_inputs'].append(user_message)

        # Check if ready for handoff to Strategy Architect
        if self._should_handoff_to_architect(result.message, state):
            return self._handoff_to_strategy_architect(project_id, deps, result)

        # Save conversation
        self.save_conversation_turn(project_id, user_message, result.message)
        self.conversation_state[project_id] = state

        result.project_id = project_id
        return result

    def _should_handoff_to_architect(self, assistant_response: str, state: Dict) -> bool:
        """Determine if conversation is ready for Strategy Architect handoff."""

        # Check for explicit handoff signal
        if "READY FOR STRATEGY ARCHITECT" in assistant_response:
            return True

        # Check if sufficient exchanges have occurred
        if state['exchanges'] >= 8:
            # Check if we have core specification elements
            spec = state.get('specification', {})
            has_core_elements = (
                spec.get('strategy_type') and
                spec.get('market_focus') and
                spec.get('entry_conditions') and
                spec.get('risk_management')
            )
            return has_core_elements

        return False

    def _handoff_to_strategy_architect(self, project_id: str, deps: TradingDependencies, conversation_result: TradingAgentOutput) -> TradingAgentOutput:
        """Hand off conversation to Strategy Architect for implementation."""

        try:
            # Get complete conversation history
            context = self.get_project_context(project_id)
            history = context.get("conversation_history", [])

            # Create strategy document from conversation
            strategy_document = self._create_strategy_document_from_conversation(history)

            # Process with Strategy Architect
            architect_result = self.strategy_architect.process_strategy_document(
                strategy_document,
                f"Conversation_Derived_Strategy_{project_id[:8]}"
            )

            # Save generated files to project
            self._save_generated_files(project_id, architect_result['generated_files'])

            # Create success response
            success_message = f"""
🎉 **Strategy Implementation Complete!**

Based on our conversation, I've generated a complete trading strategy implementation:

## 📋 Strategy Overview
- **Name**: {architect_result['strategy_name']}
- **Type**: {architect_result['components']['strategy_type']}
- **Market**: {architect_result['components']['market_focus']}
- **Complexity**: {architect_result['metadata']['complexity_score']}/100

## 📁 Generated Files
{chr(10).join(f"- {filename}" for filename in architect_result['generated_files'].keys())}

## 📊 Implementation Details
- **Estimated Development Time**: {architect_result['metadata']['estimated_development_time']}
- **Technical Indicators**: {', '.join(architect_result['components']['indicators'])}
- **Risk Management**: {architect_result['components']['position_sizing']}

## 🚀 Next Steps
1. Review the generated code in your project directory
2. Test with historical data using the backtesting framework
3. Optimize parameters based on your preferences
4. Deploy to paper trading for validation

The strategy is ready for backtesting and optimization!
"""

            # Save final conversation turn
            self.save_conversation_turn(project_id, "Strategy Architect Handoff", success_message)

            # Update project state
            if project_id in self.conversation_state:
                self.conversation_state[project_id]['phase'] = 'completed'
                self.conversation_state[project_id]['architect_result'] = architect_result

            return TradingAgentOutput(
                message=success_message,
                project_id=project_id,
                agent_type="EnhancedConversationOrchestrator",
                tools_used=["strategy_architect_handoff"],
                metadata={
                    "handoff_successful": True,
                    "generated_files": list(architect_result['generated_files'].keys()),
                    "strategy_complexity": architect_result['metadata']['complexity_score']
                }
            )

        except Exception as e:
            logger.error(f"Strategy Architect handoff failed: {e}")
            error_message = f"""
❌ **Strategy Generation Issue**

I encountered an issue while generating the strategy implementation. Let me continue our conversation to gather more details and try again.

Error: {str(e)}

Let's refine some aspects of your strategy:
- Are there specific technical indicators you prefer?
- What's your typical holding period?
- How do you handle market volatility?
"""

            return TradingAgentOutput(
                message=error_message,
                project_id=project_id,
                agent_type="EnhancedConversationOrchestrator",
                tools_used=["strategy_architect_handoff_failed"],
                metadata={"error": str(e)}
            )

    def _create_strategy_document_from_conversation(self, history: List[Dict]) -> str:
        """Create a structured strategy document from conversation history."""

        # Extract key information from conversation
        user_inputs = [msg['content'] for msg in history if msg.get('role') == 'user']
        assistant_responses = [msg['content'] for msg in history if msg.get('role') == 'assistant']

        # Create markdown document
        document = f"""# Strategy Document from Conversation

Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Conversation Summary
This strategy was developed through an iterative conversation process.

## User Requirements
{chr(10).join(f"- {input_}" for input_ in user_inputs)}

## Strategy Analysis
{chr(10).join(f"- {response}" for response in assistant_responses)}

## Implementation Notes
This strategy should be implemented with the following considerations:
- Professional-grade code structure
- Comprehensive risk management
- Backtesting framework integration
- Real-time execution capabilities
- Performance monitoring and optimization

## Next Steps
Generate complete Python implementation with backtesting capabilities.
"""

        return document

    def _save_generated_files(self, project_id: str, generated_files: Dict[str, str]):
        """Save generated files to project directory."""

        project_path = self.file_manager.get_project_path(project_id)

        for filename, content in generated_files.items():
            file_path = project_path / filename

            # Create parent directories if needed
            file_path.parent.mkdir(parents=True, exist_ok=True)

            # Write file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

            logger.info(f"Saved generated file: {file_path}")

    def get_conversation_summary(self, project_id: str) -> Dict[str, Any]:
        """Get summary of conversation progress."""

        state = self.conversation_state.get(project_id, {})
        context = self.get_project_context(project_id)
        history = context.get("conversation_history", [])

        return {
            "project_id": project_id,
            "phase": state.get('phase', 'discovery'),
            "exchanges": state.get('exchanges', 0),
            "conversation_length": len(history),
            "ready_for_handoff": state.get('phase') == 'completed',
            "has_architect_result": 'architect_result' in state
        }


# Example usage and testing
async def test_enhanced_orchestrator():
    """Test the enhanced conversation orchestrator."""

    orchestrator = EnhancedConversationOrchestrator()
    deps = TradingDependencies(
        request_id="test_enhanced_001",
        user_id="trader_001"
    )

    # Test workflow start
    user_input = "I want to build a momentum strategy for large-cap stocks with volume confirmation"

    result = orchestrator.start_enhanced_workflow(user_input, deps)

    print(f"Enhanced Orchestrator Result: {result}")
    print(f"Project ID: {result.project_id}")

    # Simulate conversation continuation
    follow_up = "I'm looking for stocks breaking above their 20-day high with strong volume"

    result2 = orchestrator.continue_enhanced_workflow(follow_up, result.project_id, deps)

    print(f"Follow-up Result: {result2.message[:200]}...")

    return result


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_enhanced_orchestrator())