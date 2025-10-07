"""
Claude MCP Client - Connects to Claude Desktop via MCP (Model Context Protocol)
"""

import os
import requests
import json
from typing import Dict, List, Optional, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ClaudeMCPClient:
    """Client for connecting to Claude Desktop via MCP"""

    def __init__(self, base_url: Optional[str] = None, auth_token: Optional[str] = None):
        """Initialize the Claude MCP client

        Args:
            base_url: MCP base URL. If None, will try to get from environment
            auth_token: MCP auth token. If None, will try to get from environment
        """
        # Try different environment variable names for MCP connection
        self.base_url = (
            base_url or 
            os.getenv('ANTHROPIC_BASE_URL') or 
            os.getenv('GLM_URL') or
            os.getenv('CLAUDE_MCP_URL')
        )
        
        self.auth_token = (
            auth_token or 
            os.getenv('ANTHROPIC_AUTH_TOKEN') or 
            os.getenv('GLM_API_TOKEN') or
            os.getenv('CLAUDE_MCP_TOKEN')
        )
        
        if not self.base_url or not self.auth_token:
            raise ValueError(
                "MCP connection details are required. Please set:\n"
                "- ANTHROPIC_BASE_URL (or GLM_URL)\n"
                "- ANTHROPIC_AUTH_TOKEN (or GLM_API_TOKEN)\n"
                "Or run the MCP setup script."
            )

        # Ensure base_url ends with the correct endpoint
        if not self.base_url.endswith('/v1/messages'):
            if self.base_url.endswith('/'):
                self.base_url = self.base_url.rstrip('/')
            
            # Check if it's a Claude Desktop MCP URL (usually localhost)
            if 'localhost' in self.base_url or '127.0.0.1' in self.base_url:
                # Claude Desktop MCP endpoint
                self.base_url = f"{self.base_url}/v1/messages"
            else:
                # Anthropic API endpoint
                self.base_url = f"{self.base_url}/v1/messages"

        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.auth_token}",
            "x-api-key": self.auth_token,  # Some setups use this instead
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
        """Send a message to Claude via MCP

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
            # Try alternative header format for some MCP setups
            if "Authorization" in str(e):
                alt_headers = self.headers.copy()
                alt_headers.pop("Authorization", None)
                alt_headers["x-api-key"] = self.auth_token
                
                try:
                    response = requests.post(self.base_url, headers=alt_headers, json=payload)
                    response.raise_for_status()
                    return response.json()
                except:
                    pass
            
            raise Exception(f"Error calling Claude MCP API: {str(e)}")

    def get_trading_analysis(self, market_data: Dict[str, Any]) -> str:
        """Get trading analysis from Claude via MCP

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

    def get_connection_info(self) -> Dict[str, Any]:
        """Get information about the MCP connection"""
        return {
            "provider": "Claude MCP",
            "base_url": self.base_url,
            "auth_token_preview": f"{self.auth_token[:10]}..." if self.auth_token else "Not set",
            "connection_type": "MCP (Model Context Protocol)"
        }


# Backward compatibility alias
ClaudeGLMClient = ClaudeMCPClient


# Example usage
if __name__ == "__main__":
    # Initialize client
    try:
        client = ClaudeMCPClient()
        print("✅ MCP client initialized successfully!")
        
        # Show connection info
        info = client.get_connection_info()
        print(f"Connection info: {info}")
        
        # Simple test
        response = client.send_message("Hello! Please respond with 'MCP connection successful!'", max_tokens=50)
        print("✅ MCP connection test successful!")
        print(f"Response: {response['content'][0]['text']}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nTo fix this, you need to set up your MCP connection.")
        print("Run: python setup_mcp_connection.py")
