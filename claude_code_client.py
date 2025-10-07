#!/usr/bin/env python3
"""
Claude Code Client - Uses Claude Code CLI instead of direct API calls
This is the recommended way to interact with Claude for WZRD Algo project
"""

import subprocess
import json
import sys
from typing import Optional, Dict, Any

class ClaudeCodeClient:
    """Client that uses Claude Code CLI for AI interactions"""

    def __init__(self, project_path: str = "/Users/michaeldurante/wzrd-algo"):
        """Initialize the Claude Code client

        Args:
            project_path: Path to your WZRD Algo project
        """
        self.project_path = project_path

    def ask_claude(self, prompt: str, model: Optional[str] = None) -> str:
        """Send a prompt to Claude using Claude Code CLI

        Args:
            prompt: Your prompt for Claude
            model: Optional model specification (defaults to claude-sonnet-4-5-20250929)

        Returns:
            Claude's response as a string
        """
        try:
            # Build the command
            cmd = [
                "claude",
                "--print",
                "--model", model or "claude-sonnet-4-5-20250929",
                prompt
            ]

            # Run Claude Code CLI from the project directory
            result = subprocess.run(
                cmd,
                cwd=self.project_path,
                capture_output=True,
                text=True,
                timeout=60  # 60 second timeout
            )

            if result.returncode == 0:
                return result.stdout.strip()
            else:
                return f"Error: {result.stderr}"

        except subprocess.TimeoutExpired:
            return "Error: Claude request timed out"
        except Exception as e:
            return f"Error: {str(e)}"

    def analyze_trading_strategy(self, strategy_code: str) -> str:
        """Analyze a trading strategy using Claude

        Args:
            strategy_code: Python code for the trading strategy

        Returns:
            Claude's analysis
        """
        prompt = f"""
Please analyze this trading strategy code for WZRD Algo:

```python
{strategy_code}
```

Provide feedback on:
1. Logic correctness
2. Potential issues or improvements
3. Performance considerations
4. Risk management
"""
        return self.ask_claude(prompt)

    def debug_code(self, code: str, error_message: str) -> str:
        """Get help debugging code

        Args:
            code: The code that's causing issues
            error_message: The error message you're receiving

        Returns:
            Claude's debugging suggestions
        """
        prompt = f"""
I'm getting this error in my WZRD Algo trading code:

Error: {error_message}

Code:
```python
{code}
```

What's causing this issue and how can I fix it?
"""
        return self.ask_claude(prompt)

    def improve_strategy(self, current_strategy: str, goals: str) -> str:
        """Get suggestions for improving a trading strategy

        Args:
            current_strategy: Current strategy code
            goals: What you want to improve (e.g., "better risk management", "higher win rate")

        Returns:
            Claude's improvement suggestions
        """
        prompt = f"""
Here's my current WZRD Algo trading strategy:

```python
{current_strategy}
```

I want to improve it with these goals: {goals}

Please suggest specific improvements and provide updated code.
"""
        return self.ask_claude(prompt)

# Example usage
if __name__ == "__main__":
    client = ClaudeCodeClient()

    # Test the client
    response = client.ask_claude("Hello! Can you help me with my WZRD Algo trading project?")
    print("Claude says:", response)

    # Example strategy analysis
    if len(sys.argv) > 1 and sys.argv[1] == "example":
        example_strategy = """
def simple_ma_strategy(data, short_ma=20, long_ma=50):
    # Simple moving average crossover strategy
    data['short_ma'] = data['close'].rolling(window=short_ma).mean()
    data['long_ma'] = data['close'].rolling(window=long_ma).mean()

    # Generate signals
    data['signal'] = 0
    data.loc[data['short_ma'] > data['long_ma'], 'signal'] = 1
    data.loc[data['short_ma'] < data['long_ma'], 'signal'] = -1

    return data
"""

        analysis = client.analyze_trading_strategy(example_strategy)
        print("\nStrategy Analysis:")
        print(analysis)