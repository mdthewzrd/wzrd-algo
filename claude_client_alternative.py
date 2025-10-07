"""
Alternative Claude API Client - trying different endpoints
"""

import os
import requests
import json
from typing import Dict, List, Optional, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ClaudeGLMClientAlternative:
    """Alternative client for different Claude API endpoints"""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize the Claude client

        Args:
            api_key: Your Claude API key. If None, will try to get from environment
        """
        self.api_key = api_key or os.getenv('CLAUDE_API_KEY')
        if not self.api_key:
            raise ValueError("Claude API key is required. Set CLAUDE_API_KEY environment variable or pass api_key parameter.")

        # Try different endpoints
        self.endpoints = [
            {
                "url": "https://api.anthropic.com/v1/messages",
                "headers": {
                    "Content-Type": "application/json",
                    "x-api-key": self.api_key,
                    "anthropic-version": "2023-06-01"
                }
            },
            {
                "url": "https://api.claude.ai/v1/messages",
                "headers": {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.api_key}"
                }
            },
            {
                "url": "https://api.anthropic.com/v1/complete",
                "headers": {
                    "Content-Type": "application/json",
                    "x-api-key": self.api_key,
                    "anthropic-version": "2023-06-01"
                }
            }
        ]

    def test_endpoints(self):
        """Test all possible endpoints"""
        print("🔍 Testing different Claude API endpoints...")

        test_message = "Hello! Just testing the connection."

        for i, endpoint in enumerate(self.endpoints):
            print(f"\n📡 Testing endpoint {i+1}: {endpoint['url']}")

            try:
                response = requests.post(
                    endpoint['url'],
                    headers=endpoint['headers'],
                    json={
                        "model": "claude-3-sonnet-20240229",
                        "max_tokens": 100,
                        "messages": [{"role": "user", "content": test_message}]
                    },
                    timeout=10
                )

                print(f"Status Code: {response.status_code}")

                if response.status_code == 200:
                    print("✅ SUCCESS!")
                    return endpoint, response.json()
                else:
                    print(f"❌ Failed: {response.text}")

            except Exception as e:
                print(f"❌ Error: {e}")

        return None, None

    def send_message_simple(self, message: str, working_endpoint: Dict = None):
        """Send message using the working endpoint"""
        if working_endpoint is None:
            working_endpoint, _ = self.test_endpoints()

        if working_endpoint is None:
            raise ValueError("No working endpoint found")

        try:
            response = requests.post(
                working_endpoint['url'],
                headers=working_endpoint['headers'],
                json={
                    "model": "claude-3-sonnet-20240229",
                    "max_tokens": 1000,
                    "messages": [{"role": "user", "content": message}]
                }
            )
            response.raise_for_status()
            return response.json()

        except Exception as e:
            raise Exception(f"Error calling Claude API: {str(e)}")


# Quick test
if __name__ == "__main__":
    client = ClaudeGLMClientAlternative()
    endpoint, response = client.test_endpoints()

    if endpoint:
        print(f"\n🎉 Working endpoint found: {endpoint['url']}")
        if response:
            print(f"Response: {response}")
    else:
        print("\n❌ No working endpoints found")