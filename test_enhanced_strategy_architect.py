"""
Comprehensive testing framework for the Enhanced Strategy Architect
"""

import asyncio
import logging
import sys
import os
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime

# Add project root to path
sys.path.append(str(Path(__file__).parent))

from agents.strategy_architect_enhanced import EnhancedStrategyArchitect
from agents.conversation_orchestrator_enhanced import EnhancedConversationOrchestrator
from claude_mcp_client import ClaudeMCPClient as ClaudeGLMClient

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class StrategyArchitectTestSuite:
    """Comprehensive test suite for the Enhanced Strategy Architect."""

    def __init__(self):
        self.architect = EnhancedStrategyArchitect()
        self.orchestrator = EnhancedConversationOrchestrator()
        self.test_results = []

    async def run_all_tests(self) -> Dict[str, Any]:
        """Run all tests and return comprehensive results."""

        print("🚀 Starting Enhanced Strategy Architect Test Suite")
        print("=" * 60)

        tests = [
            self.test_parsing_capability,
            self.test_code_generation,
            self.test_workflow_integration,
            self.test_error_handling,
            self.test_complex_strategy,
            self.test_edge_cases
        ]

        results = {}
        for test_func in tests:
            test_name = test_func.__name__
            try:
                print(f"\n📋 Running: {test_name}")
                result = await test_func()
                results[test_name] = result
                self.test_results.append({
                    'test': test_name,
                    'status': 'PASSED' if result['success'] else 'FAILED',
                    'details': result
                })
                print(f"✅ {test_name}: {'PASSED' if result['success'] else 'FAILED'}")
            except Exception as e:
                print(f"❌ {test_name}: ERROR - {e}")
                results[test_name] = {'success': False, 'error': str(e)}
                self.test_results.append({
                    'test': test_name,
                    'status': 'ERROR',
                    'error': str(e)
                })

        return await self.generate_test_summary(results)

    async def test_parsing_capability(self) -> Dict[str, Any]:
        """Test strategy document parsing capabilities."""

        # Test documents of varying complexity
        test_documents = [
            {
                'name': 'Simple Momentum Strategy',
                'content': '''
                # Simple Momentum Strategy

                This strategy buys stocks that are breaking out with momentum.

                ## Entry
                - Price above 50-day moving average
                - RSI above 60
                - Volume above average

                ## Exit
                - Take profit at 10%
                - Stop loss at 5%
                ''',
                'expected_complexity': 'low'
            },
            {
                'name': 'Complex Mean Reversion',
                'content': '''
                # Advanced Mean Reversion Strategy

                This strategy identifies overextended conditions for mean reversion opportunities.

                ## Market Context
                - Large-cap US equities
                - 15-minute timeframe
                - Avoid earnings periods
                - Trending markets only

                ## Entry Logic
                - Price > 2 standard deviations above 20-period Bollinger Band
                - RSI > 70 (overbought)
                - Volume declining from peak
                - MACD showing divergence

                ## Entry Filters
                - Minimum $10 stock price
                - Minimum 10M daily volume
                - Market cap > $2B
                - Avoid biotech and news-driven stocks

                ## Exit Conditions
                - Primary: Price reverts to 20-period moving average
                - Secondary: RSI drops below 50
                - Time-based exit after 48 hours
                - Stop loss at 3R below entry

                ## Risk Management
                - Position sizing: 1% account risk per trade
                - Maximum portfolio heat: 15%
                - Maximum 8 concurrent positions
                - Correlation limits: Max 3 positions in same sector

                ## Pyramiding Rules
                - Maximum 2 additions per position
                - Add only if original position profitable
                - Each addition 50% size of original

                ## Technical Indicators
                - Primary: Bollinger Bands (20, 2)
                - Secondary: RSI (14), MACD (12,26,9), Volume Profile
                - Confirmation: Money Flow Index, Stochastic

                ## Performance Metrics
                - Target win rate: 65%
                - Profit factor: 1.8+
                - Maximum drawdown: <12%
                - Average holding period: 8-24 hours

                ## Special Conditions
                - No trades during FOMC announcements
                - Reduced size during high VIX periods
                    - Sector rotation awareness
                - News sentiment filtering
                ''',
                'expected_complexity': 'high'
            }
        ]

        results = []
        for doc in test_documents:
            try:
                result = self.architect.process_strategy_document(doc['content'], doc['name'])
                success = result['metadata']['complexity_score'] > 0

                results.append({
                    'document': doc['name'],
                    'success': success,
                    'complexity_score': result['metadata']['complexity_score'],
                    'files_generated': len(result['generated_files']),
                    'estimated_time': result['metadata']['estimated_development_time']
                })

                logger.info(f"Parsed {doc['name']}: complexity {result['metadata']['complexity_score']}")

            except Exception as e:
                results.append({
                    'document': doc['name'],
                    'success': False,
                    'error': str(e)
                })

        all_passed = all(r['success'] for r in results)
        return {
            'success': all_passed,
            'results': results,
            'total_documents': len(test_documents)
        }

    async def test_code_generation(self) -> Dict[str, Any]:
        """Test code generation quality."""

        test_strategy = '''
        # RSI Divergence Strategy

        ## Entry
        - Bullish divergence on RSI
        - Price support level
        - Volume confirmation

        ## Exit
        - RSI above 70
        - 2R profit target
        '''

        try:
            result = self.architect.process_strategy_document(test_strategy, "RSI Divergence Test")

            # Check generated files
            files = result['generated_files']
            required_files = ['strategy.py', 'config.py', 'utils.py']

            file_checks = {}
            code_quality = {}

            for file_name in required_files:
                if file_name in files:
                    content = files[file_name]
                    file_checks[file_name] = {
                        'exists': True,
                        'size': len(content),
                        'has_functions': 'def ' in content,
                        'has_classes': 'class ' in content,
                        'has_type_hints': ': ' in content and '->' in content
                    }
                else:
                    file_checks[file_name] = {'exists': False}

            return {
                'success': len(files) >= 3,
                'files_generated': list(files.keys()),
                'file_quality': file_checks,
                'total_code_size': sum(len(content) for content in files.values())
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    async def test_workflow_integration(self) -> Dict[str, Any]:
        """Test conversation orchestrator integration."""

        try:
            from agents.trading_base_agent import TradingDependencies

            deps = TradingDependencies(
                request_id="workflow_test_001",
                user_id="test_user"
            )

            # Start workflow
            initial_message = "I want to build a breakout strategy for crypto with volume confirmation"
            result = self.orchestrator.start_enhanced_workflow(initial_message, deps)

            # Continue conversation
            follow_up = "Looking for coins breaking resistance with 2x volume spike"
            result2 = self.orchestrator.continue_enhanced_workflow(follow_up, result.project_id, deps)

            # Check state
            summary = self.orchestrator.get_conversation_summary(result.project_id)

            return {
                'success': result.project_id is not None,
                'project_created': result.project_id is not None,
                'conversation_exchanges': summary['exchanges'],
                'current_phase': summary['phase'],
                'files_generated': summary.get('has_architect_result', False)
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    async def test_error_handling(self) -> Dict[str, Any]:
        """Test error handling capabilities."""

        error_tests = [
            {
                'name': 'Empty Document',
                'content': '',
                'should_fail': True
            },
            {
                'name': 'Invalid Document',
                'content': 'This is not a strategy document.',
                'should_fail': False  # Should still work with fallback
            },
            {
                'name': 'Malformed JSON',
                'content': '{"broken": json}',
                'should_fail': False  # Should handle gracefully
            }
        ]

        results = []
        for test in error_tests:
            try:
                result = self.architect.process_strategy_document(test['content'], test['name'])
                handled_gracefully = 'generated_files' in result

                results.append({
                    'test': test['name'],
                    'success': test['should_fail'] != handled_gracefully,
                    'handled_gracefully': handled_gracefully
                })

            except Exception as e:
                results.append({
                    'test': test['name'],
                    'success': test['should_fail'],  # Expected to fail
                    'error': str(e)
                })

        return {
            'success': all(r['success'] for r in results),
            'error_tests': results
        }

    async def test_complex_strategy(self) -> Dict[str, Any]:
        """Test with the actual Lingua Parabolic Fade strategy."""

        try:
            # Load the complex strategy document if it exists
            lingua_doc_path = Path("knowledge/lingua_parabolic_fade.md")
            if lingua_doc_path.exists():
                with open(lingua_doc_path, 'r') as f:
                    complex_content = f.read()
            else:
                # Use a simplified version for testing
                complex_content = '''
                # Lingua Parabolic Fade Strategy

                ## Overview
                Multi-timeframe mean reversion targeting parabolic exhaustion in large-cap equities.

                ## Market Context
                - Large-cap US equities ($2B+ market cap)
                - 15m context + 5m execution timeframes
                - Intraday trading only
                - Avoid earnings, FOMC, high VIX periods

                ## Entry Logic
                - Price extension > 2% above EMA72/89 confluence
                - Volume declining from 5-day peak
                - RSI showing potential divergence
                - Gap threshold: 0.75× ATR minimum

                ## Entry Filters
                - Minimum 8M daily volume
                - Minimum $300M daily dollar volume
                - Price range $10-$500
                - 2.5% minimum daily range

                ## Risk Management
                - 1% risk per trade
                - 20% maximum portfolio heat
                - ATR-based position sizing
                - Maximum 6 concurrent positions

                ## Pyramiding
                - Max 2 additions per position
                - 50% size reduction on additions
                - Only if original position profitable

                ## Exit Logic
                - Primary: Mean reversion to EMAs
                - Secondary: RSI normalization
                - Time exit: 75 minutes max
                - Stop: 1.5× ATR below entry

                ## Technical Indicators
                - Primary: EMA72/89 confluence
                - Secondary: RSI, Volume analysis, ATR
                - Multi-timeframe confirmation
                '''

            result = self.architect.process_strategy_document(complex_content, "Lingua Parabolic Fade")

            return {
                'success': True,
                'complexity_score': result['metadata']['complexity_score'],
                'files_generated': len(result['generated_files']),
                'estimated_time': result['metadata']['estimated_development_time'],
                'strategy_components': result['components']
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    async def test_edge_cases(self) -> Dict[str, Any]:
        """Test edge cases and boundary conditions."""

        edge_cases = [
            {
                'name': 'Very Long Document',
                'content': '# Strategy\n' + 'Detail line.\n' * 1000,
                'should_succeed': True
            },
            {
                'name': 'Special Characters',
                'content': '# Strategy @#$%\nEntry: 条件\nExit: 出口',
                'should_succeed': True
            },
            {
                'name': 'No Technical Indicators',
                'content': '# Price Action Strategy\nBuy when price goes up.\nSell when price goes down.',
                'should_succeed': True
            }
        ]

        results = []
        for case in edge_cases:
            try:
                result = self.architect.process_strategy_document(case['content'], case['name'])
                success = result['metadata']['complexity_score'] >= 0

                results.append({
                    'case': case['name'],
                    'success': success == case['should_succeed'],
                    'complexity': result['metadata']['complexity_score']
                })

            except Exception as e:
                results.append({
                    'case': case['name'],
                    'success': case['should_succeed'] == False,  # Expected to fail
                    'error': str(e)
                })

        return {
            'success': all(r['success'] for r in results),
            'edge_case_results': results
        }

    async def generate_test_summary(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive test summary."""

        total_tests = len(results)
        passed_tests = sum(1 for r in results.values() if r.get('success', False))

        summary = {
            'total_tests': total_tests,
            'passed_tests': passed_tests,
            'failed_tests': total_tests - passed_tests,
            'success_rate': (passed_tests / total_tests) * 100 if total_tests > 0 else 0,
            'test_results': results,
            'recommendations': self._generate_recommendations(results)
        }

        # Print summary
        print(f"\n📊 Test Summary")
        print("=" * 60)
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {total_tests - passed_tests}")
        print(f"Success Rate: {summary['success_rate']:.1f}%")

        if summary['recommendations']:
            print(f"\n🔧 Recommendations:")
            for rec in summary['recommendations']:
                print(f"  - {rec}")

        return summary

    def _generate_recommendations(self, results: Dict[str, Any]) -> List[str]:
        """Generate improvement recommendations based on test results."""

        recommendations = []

        # Check for common failure patterns
        failed_tests = [name for name, result in results.items() if not result.get('success', False)]

        if 'test_parsing_capability' in failed_tests:
            recommendations.append("Improve document parsing robustness")

        if 'test_code_generation' in failed_tests:
            recommendations.append("Enhance code generation templates")

        if 'test_workflow_integration' in failed_tests:
            recommendations.append("Fix workflow integration between agents")

        if 'test_error_handling' in failed_tests:
            recommendations.append("Improve error handling and fallback mechanisms")

        if len(failed_tests) > 2:
            recommendations.append("Consider implementing more comprehensive logging")

        return recommendations


async def main():
    """Main test runner."""

    print("🧪 Enhanced Strategy Architect Test Suite")
    print("=" * 60)

    # Check if Claude API is available
    try:
        claude_client = ClaudeGLMClient()
        test_response = claude_client.send_message("Test connection", max_tokens=10)
        print("✅ Claude API connection successful")
    except Exception as e:
        print(f"⚠️ Claude API connection failed: {e}")
        print("⚠️ Running tests in fallback mode (limited functionality)")

    # Run test suite
    test_suite = StrategyArchitectTestSuite()
    results = await test_suite.run_all_tests()

    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = f"test_results_{timestamp}.json"

    import json
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)

    print(f"\n📁 Detailed results saved to: {results_file}")

    return results


if __name__ == "__main__":
    results = asyncio.run(main())