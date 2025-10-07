"""
Launch all three Streamlit apps for the complete workflow
- Signal Codifier (localhost:8502)
- Strategy Viewer (localhost:8501)
- Instructions for running all three
"""

import subprocess
import sys
import time
import webbrowser
from threading import Thread

def launch_app(script_name, port, app_name):
    """Launch a Streamlit app on the specified port"""
    print(f"🚀 Launching {app_name} on http://localhost:{port}")
    try:
        cmd = [sys.executable, "-m", "streamlit", "run", script_name, "--server.port", str(port), "--server.headless", "true"]
        subprocess.run(cmd)
    except Exception as e:
        print(f"❌ Failed to launch {app_name}: {e}")

def open_browser():
    """Open browser tabs for all apps"""
    time.sleep(3)  # Wait for apps to start
    try:
        webbrowser.open("http://localhost:8501")  # Strategy Viewer
        webbrowser.open("http://localhost:8502")  # Signal Codifier
        print("🌐 Opened browser tabs for both apps")
    except Exception as e:
        print(f"⚠️ Could not open browser: {e}")

def main():
    print("🎯 WZRD Strategy Workflow Launcher")
    print("=" * 50)
    print()
    print("📋 This launcher will start both Streamlit apps:")
    print("   🎯 Signal Codifier - http://localhost:8502")
    print("   📊 Strategy Viewer  - http://localhost:8501")
    print()
    print("🔄 Your Complete Workflow:")
    print("   1. Web Chat → Develop strategy with GPT")
    print("   2. Signal Codifier → Convert to code-true signals")
    print("   3. Strategy Viewer → Verify signals visually")
    print("   4. Web Chat → Iterate or proceed to VectorBT")
    print()

    # Ask user what to launch
    print("Choose what to launch:")
    print("1. Launch both apps (recommended)")
    print("2. Launch Signal Codifier only (port 8502)")
    print("3. Launch Strategy Viewer only (port 8501)")
    print("4. Just show me the commands")

    choice = input("\nEnter your choice (1-4): ").strip()

    if choice == "1":
        print("\n🚀 Launching both apps...")
        print("   Signal Codifier: http://localhost:8502")
        print("   Strategy Viewer:  http://localhost:8501")
        print("\nPress Ctrl+C to stop the apps")

        # Start browser opener in background
        browser_thread = Thread(target=open_browser)
        browser_thread.daemon = True
        browser_thread.start()

        # Launch both apps (this will block)
        try:
            # Launch Strategy Viewer first
            viewer_thread = Thread(target=launch_app, args=("strategy_viewer.py", 8501, "Strategy Viewer"))
            viewer_thread.daemon = True
            viewer_thread.start()

            # Launch Signal Codifier
            launch_app("signal_codifier.py", 8502, "Signal Codifier")
        except KeyboardInterrupt:
            print("\n👋 Stopping apps...")

    elif choice == "2":
        print("\n🚀 Launching Signal Codifier on http://localhost:8502")
        print("Press Ctrl+C to stop")
        try:
            webbrowser.open("http://localhost:8502")
            launch_app("signal_codifier.py", 8502, "Signal Codifier")
        except KeyboardInterrupt:
            print("\n👋 Stopping app...")

    elif choice == "3":
        print("\n🚀 Launching Strategy Viewer on http://localhost:8501")
        print("Press Ctrl+C to stop")
        try:
            webbrowser.open("http://localhost:8501")
            launch_app("strategy_viewer.py", 8501, "Strategy Viewer")
        except KeyboardInterrupt:
            print("\n👋 Stopping app...")

    elif choice == "4":
        print("\n📋 Manual Launch Commands:")
        print()
        print("Launch Signal Codifier (port 8502):")
        print("   streamlit run signal_codifier.py --server.port 8502")
        print()
        print("Launch Strategy Viewer (port 8501):")
        print("   streamlit run strategy_viewer.py --server.port 8501")
        print()
        print("Or use this shortcut script:")
        print("   python launch_workflow.py")

    else:
        print("❌ Invalid choice")

if __name__ == "__main__":
    main()