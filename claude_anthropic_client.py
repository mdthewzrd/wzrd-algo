"""
Claude Anthropic API Client - Direct connection to Anthropic's Claude API
"""

import os
import requests
import json
from typing import Dict, List, Optional, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ClaudeAnthropicClient:
    """Client for Anthropic's Claude API"""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize the Claude client

        Args:
            api_key: Your Anthropic API key. If None, will try to get from environment
        """
        self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY')
        if not self.api_key:
            raise ValueError("Anthropic API key is required. Set ANTHROPIC_API_KEY environment variable or pass api_key parameter.")

        # Anthropic API endpoint
        self.base_url = "https://api.anthropic.com/v1/messages"
        self.headers = {
            "Content-Type": "application/json",
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01"
        }

    def send_message(
        self,
        message: str,
        max_tokens: int = 1000,
        temperature: float = 0.7,
        system_prompt: Optional[str] = None,
        conversation_history: Optional[List[Dict]] = None,
        model: str = "claude-3-5-sonnet-20241022"
    ) -> Dict[str, Any]:
        """Send a message to Claude

        Args:
            message: The user message to send
            max_tokens: Maximum tokens in response
            temperature: Response randomness (0.0 to 1.0)
            system_prompt: Optional system prompt
            conversation_history: Optional conversation history
            model: Claude model to use

        Returns:
            API response dictionary
        """

        # Prepare messages
        messages = []

        # Add conversation history if provided
        if conversation_history:
            messages.extend(conversation_history)

        # Add current user message
        messages.append({
            "role": "user",
            "content": message
        })

        # Prepare request payload
        payload = {
            "model": model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": messages
        }

        # Add system prompt if provided
        if system_prompt:
            payload["system"] = system_prompt

        try:
            response = requests.post(self.base_url, headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            raise Exception(f"Error calling Claude API: {str(e)}")

    def get_trading_analysis(self, market_data: Dict[str, Any]) -> str:
        """Get trading analysis from Claude

        Args:
            market_data: Dictionary containing market data

        Returns:
            Trading analysis text
        """
        system_prompt = """You are an expert trading analyst. Analyze the provided market data and provide trading insights,
        including entry/exit points, risk assessment, and market sentiment. Be concise and actionable."""

        message = f"""Analyze this market data for trading opportunities:

        Market Data:
        {json.dumps(market_data, indent=2)}

        Provide:
        1. Market sentiment analysis
        2. Key support/resistance levels
        3. Recommended entry/exit points
        4. Risk assessment
        5. Trading strategy recommendations
        """

        response = self.send_message(
            message=message,
            system_prompt=system_prompt,
            max_tokens=1500
        )

        return response['content'][0]['text']

    def generate_strategy_code(self, strategy_description: str) -> str:
        """Generate trading strategy code

        Args:
            strategy_description: Description of the trading strategy

        Returns:
            Python code for the trading strategy
        """
        system_prompt = """You are an expert Python developer specializing in trading algorithms.
        Generate clean, well-commented Python code for trading strategies using pandas and numpy."""

        message = f"""Generate a Python trading strategy based on this description:

        Strategy Description:
        {strategy_description}

        Include:
        1. Strategy logic implementation
        2. Signal generation
        3. Risk management
        4. Entry/exit conditions
        5. Comments explaining the code
        """

        response = self.send_message(
            message=message,
            system_prompt=system_prompt,
            max_tokens=2000
        )

        return response['content'][0]['text']

    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the current model being used"""
        return {
            "provider": "Anthropic",
            "model": "claude-3-5-sonnet-20241022",
            "api_version": "2023-06-01",
            "base_url": self.base_url
        }


# Backward compatibility alias - so existing code doesn't break
ClaudeGLMClient = ClaudeAnthropicClient


# Example usage
if __name__ == "__main__":
    # Initialize client
    client = ClaudeAnthropicClient()

    # Simple test
    try:
        response = client.send_message("Hello! I'm ready to help with trading analysis.")
        print("✅ API connection successful!")
        print(f"Response: {response['content'][0]['text']}")
    except Exception as e:
        print(f"❌ Error: {e}")

    # Test model info
    try:
        model_info = client.get_model_info()
        print(f"Model info: {model_info}")
    except Exception as e:
        print(f"❌ Error getting model info: {e}")
