#!/usr/bin/env python3
"""
🚀 Streamlined Workflow Launcher

Launch both Signal Codifier and Strategy Viewer with optimized ports
for the streamlined WZRD workflow: Web Chat → Signal Codifier → Strategy Viewer → VectorBT
"""

import subprocess
import time
import threading
import sys
from pathlib import Path

# ANSI color codes for better terminal output
GREEN = '\033[92m'
BLUE = '\033[94m'
YELLOW = '\033[93m'
RED = '\033[91m'
CYAN = '\033[96m'
BOLD = '\033[1m'
RESET = '\033[0m'

def print_header():
    """Print the workflow header"""
    print(f"\n{CYAN}{BOLD}🎯 WZRD Streamlined Workflow Launcher{RESET}")
    print(f"📊 Web Chat → Signal Codifier → Strategy Viewer → VectorBT")
    print("=" * 60)

def print_service_info():
    """Print service URLs and information"""
    print(f"\n{GREEN}🚀 Services Starting...{RESET}")
    print(f"{BLUE}📊 Signal Codifier: {YELLOW}http://localhost:8502{RESET}")
    print(f"{BLUE}📈 Strategy Viewer:  {YELLOW}http://localhost:8501{RESET}")
    print(f"\n{CYAN}🎯 Workflow Steps:{RESET}")
    print(f"1. {YELLOW}Web Chat{RESET} → Create strategy JSON with GPT")
    print(f"2. {YELLOW}Signal Codifier{RESET} → Generate code-true signals")
    print(f"3. {YELLOW}Strategy Viewer{RESET} → Visual verification")
    print(f"4. {YELLOW}Iterate{RESET} → Refine based on performance")
    print(f"\n{RED}Press Ctrl+C to stop all services{RESET}")

def run_streamlit_app(script_path, port, app_name):
    """Run a Streamlit app with proper error handling"""
    try:
        cmd = [
            sys.executable, "-m", "streamlit", "run",
            str(script_path),
            "--server.port", str(port),
            "--server.headless", "true",
            "--server.fileWatcherType", "none",
            "--server.runOnSave", "false",
            "--browser.gatherUsageStats", "false"
        ]

        print(f"{CYAN}🚀 Starting {app_name} on port {port}...{RESET}")
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Wait a moment to see if it starts successfully
        time.sleep(3)
        if process.poll() is None:
            print(f"{GREEN}✅ {app_name} started successfully!{RESET}")
        else:
            print(f"{RED}❌ {app_name} failed to start{RESET}")
            return None

        return process

    except Exception as e:
        print(f"{RED}❌ Error starting {app_name}: {e}{RESET}")
        return None

def check_dependencies():
    """Check if required files exist"""
    required_files = [
        "signal_codifier.py",
        "strategy_viewer.py",
        "wzrd_mini_chart.py",
        "chart_templates.py"
    ]

    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)

    if missing_files:
        print(f"{RED}❌ Missing required files: {missing_files}{RESET}")
        return False

    print(f"{GREEN}✅ All required files found{RESET}")
    return True

def main():
    """Main launcher function"""
    print_header()

    # Check dependencies
    if not check_dependencies():
        sys.exit(1)

    print_service_info()

    # Start Signal Codifier first
    signal_codifier_process = run_streamlit_app(
        "signal_codifier.py",
        8502,
        "Signal Codifier"
    )

    if not signal_codifier_process:
        print(f"{RED}❌ Failed to start Signal Codifier{RESET}")
        sys.exit(1)

    # Start Strategy Viewer
    strategy_viewer_process = run_streamlit_app(
        "strategy_viewer.py",
        8501,
        "Strategy Viewer"
    )

    if not strategy_viewer_process:
        print(f"{RED}❌ Failed to start Strategy Viewer{RESET}")
        signal_codifier_process.terminate()
        sys.exit(1)

    print(f"\n{GREEN}🎉 All services started successfully!{RESET}")
    print(f"{CYAN}📊 Signal Codifier: {YELLOW}http://localhost:8502{RESET}")
    print(f"{BLUE}📈 Strategy Viewer:  {YELLOW}http://localhost:8501{RESET}")
    print(f"\n{YELLOW}💡 Workflow Tips:{RESET}")
    print(f"• Paste strategy JSON from Web Chat into Signal Codifier")
    print(f"• Copy the generated codified artifact")
    print(f"• Paste artifact into Strategy Viewer for verification")
    print(f"• Iterate based on visual feedback and performance")
    print(f"\n{RED}Press Ctrl+C to stop all services{RESET}")

    try:
        # Keep the script running
        while True:
            time.sleep(1)
            # Check if processes are still running
            if signal_codifier_process.poll() is not None:
                print(f"{RED}❌ Signal Codifier process stopped unexpectedly{RESET}")
                break
            if strategy_viewer_process.poll() is not None:
                print(f"{RED}❌ Strategy Viewer process stopped unexpectedly{RESET}")
                break
    except KeyboardInterrupt:
        print(f"\n{YELLOW}🛑 Stopping services...{RESET}")
    finally:
        # Clean up processes
        if signal_codifier_process:
            signal_codifier_process.terminate()
            signal_codifier_process.wait()
        if strategy_viewer_process:
            strategy_viewer_process.terminate()
            strategy_viewer_process.wait()
        print(f"{GREEN}✅ All services stopped{RESET}")

if __name__ == "__main__":
    main()