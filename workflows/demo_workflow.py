#!/usr/bin/env python3
"""
Demo script showing the complete workflow with running services
This demonstrates how to use the Signal Codifier and Strategy Viewer
"""

import json
import webbrowser
import time
import subprocess
import os
from datetime import datetime

def open_services():
    """Open both services in browser"""
    print("🌐 Opening services in browser...")
    try:
        # Open Signal Codifier
        webbrowser.open("http://localhost:8502")
        print("✅ Signal Codifier opened: http://localhost:8502")

        # Open Strategy Viewer
        webbrowser.open("http://localhost:8501")
        print("✅ Strategy Viewer opened: http://localhost:8501")

        return True
    except Exception as e:
        print(f"❌ Failed to open browser: {e}")
        return False

def show_workflow_instructions():
    """Show step-by-step workflow instructions"""
    print("\n🎯 COMPLETE WORKFLOW DEMONSTRATION")
    print("=" * 60)

    print("\n📋 Step 1: Strategy Development (Web Chat)")
    print("   • Create strategy idea with GPT")
    print("   • Get strategy JSON specification")
    print("   • Example: test_strategy_workflow.json")

    print("\n📊 Step 2: Signal Codifier (Port 8502)")
    print("   • Open: http://localhost:8502")
    print("   • Paste strategy JSON into the interface")
    print("   • Configure parameters (symbol, timeframe, etc.)")
    print("   • Click 'Process Strategy'")
    print("   • Get codified strategy with signals")
    print("   • Copy the codified JSON output")

    print("\n📈 Step 3: Strategy Viewer (Port 8501)")
    print("   • Open: http://localhost:8501")
    print("   • Paste codified JSON into the interface")
    print("   • View strategy visualization")
    print("   • Analyze signals and performance")
    print("   • Verify strategy behavior")

    print("\n🔄 Step 4: Iteration")
    print("   • Analyze performance in Strategy Viewer")
    print("   • Return to Web Chat with feedback")
    print("   • Refine strategy based on results")
    print("   • Repeat workflow")

def show_example_usage():
    """Show how to use the example files"""
    print("\n📁 EXAMPLE FILES USAGE")
    print("=" * 40)

    print("\n1. Test Strategy JSON:")
    print("   File: test_strategy_workflow.json")
    print("   Use this as input for Signal Codifier")

    print("\n2. Codified Strategy JSON:")
    print("   File: test_codified_workflow.json")
    print("   Use this as input for Strategy Viewer")

    print("\n3. Other Examples:")
    print("   - example_strategy_rules_qqq_mean_reversion.json")
    print("   - test_strategy.json")
    print("   - qqq_mean_reversion_example_codified.json")

def verify_api_key():
    """Verify API key is configured"""
    print("\n🔑 API Key Configuration")
    print("=" * 30)

    try:
        with open('.env', 'r') as f:
            content = f.read()
            if 'POLYGON_API_KEY=Fm7brz4s23eSocDErnL68cE7wspz2K1I' in content:
                print("✅ Polygon API key configured successfully")
            else:
                print("❌ API key not found in .env file")
    except FileNotFoundError:
        print("❌ .env file not found")

def main():
    """Main demo function"""
    print("🚀 Wizard Algo Mini - Workflow Demo")
    print("=" * 50)
    print(f"📅 Demo Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Verify API key
    verify_api_key()

    # Show workflow instructions
    show_workflow_instructions()

    # Show example usage
    show_example_usage()

    # Check if services are running
    print("\n🔍 Service Status Check")
    print("=" * 30)

    import requests
    try:
        response1 = requests.get("http://localhost:8501", timeout=5)
        print("✅ Strategy Viewer: RUNNING (Port 8501)")
    except:
        print("❌ Strategy Viewer: NOT RUNNING")

    try:
        response2 = requests.get("http://localhost:8502", timeout=5)
        print("✅ Signal Codifier: RUNNING (Port 8502)")
    except:
        print("❌ Signal Codifier: NOT RUNNING")

    # Ask user if they want to open the services
    print("\n🌐 Would you like to open the services in your browser?")
    print("   (This will open two browser tabs)")

    try:
        choice = input("\nOpen services? (y/n): ").strip().lower()
        if choice == 'y':
            success = open_services()
            if success:
                print("\n✅ Services opened successfully!")
                print("📊 Use the Signal Codifier to process strategy JSON")
                print("📈 Use the Strategy Viewer to visualize results")
            else:
                print("❌ Failed to open services")
        else:
            print("\n💡 You can manually open:")
            print("   Signal Codifier: http://localhost:8502")
            print("   Strategy Viewer:  http://localhost:8501")
    except KeyboardInterrupt:
        print("\n\n👋 Demo completed!")

    print("\n🎯 Workflow Summary")
    print("=" * 30)
    print("1. Develop strategy → Get JSON")
    print("2. Signal Codifier → Generate signals")
    print("3. Strategy Viewer → Visualize results")
    print("4. Analyze → Iterate → Improve")

    print("\n✅ Demo completed successfully!")
    print("🚀 Your wizard algo mini is ready to use!")

if __name__ == "__main__":
    main()