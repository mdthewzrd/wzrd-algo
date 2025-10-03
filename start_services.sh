#!/bin/bash

# WZRD-Algo-Mini Service Launcher
# Starts all core services for the trading strategy system

echo "🚀 Starting WZRD-Algo-Mini Services..."
echo "======================================="

# Check if we're in the right directory
if [[ ! -f "apps/signal_codifier.py" ]]; then
    echo "❌ Error: Please run this script from the wzrd-algo-mini root directory"
    echo "Current directory: $(pwd)"
    echo "Expected files: apps/signal_codifier.py, apps/strategy_viewer_enhanced.py, apps/scan_builder.py"
    exit 1
fi

# Check for Python dependencies
echo "🔍 Checking dependencies..."
python -c "import streamlit, pandas, plotly" 2>/dev/null || {
    echo "❌ Missing dependencies. Please install:"
    echo "pip install streamlit pandas plotly numpy python-dotenv pytz"
    exit 1
}

# Check for .env file
if [[ ! -f ".env" ]]; then
    echo "⚠️  Warning: .env file not found. API features may not work."
    echo "Create .env with: POLYGON_API_KEY=your_key_here"
fi

# Kill any existing streamlit processes
echo "🧹 Cleaning up existing services..."
pkill -f "streamlit run" 2>/dev/null || true

# Start Signal Codifier
echo "📊 Starting Signal Codifier (Port 8502)..."
streamlit run apps/signal_codifier.py --server.port 8502 --server.headless true &
CODIFIER_PID=$!

# Wait a moment for first service to start
sleep 2

# Start Enhanced Strategy Viewer
echo "📈 Starting Enhanced Strategy Viewer (Port 8510)..."
streamlit run apps/strategy_viewer_enhanced.py --server.port 8510 --server.headless true &
VIEWER_PID=$!

# Wait a moment before starting next service
sleep 2

# Start Scan Builder
echo "🔍 Starting Scan Builder (Port 8503)..."
streamlit run apps/scan_builder.py --server.port 8503 --server.headless true &
SCAN_PID=$!

# Wait for services to initialize
echo "⏳ Waiting for services to initialize..."
sleep 5

# Check if services are running
echo "🔍 Checking service status..."

if lsof -i :8502 >/dev/null 2>&1; then
    echo "✅ Signal Codifier running on http://localhost:8502"
else
    echo "❌ Signal Codifier failed to start"
fi

if lsof -i :8510 >/dev/null 2>&1; then
    echo "✅ Strategy Viewer Enhanced running on http://localhost:8510"
else
    echo "❌ Strategy Viewer Enhanced failed to start"
fi

if lsof -i :8503 >/dev/null 2>&1; then
    echo "✅ Scan Builder running on http://localhost:8503"
else
    echo "❌ Scan Builder failed to start"
fi

echo ""
echo "🎉 WZRD-Algo-Mini Services Started!"
echo "======================================="
echo "📊 Signal Codifier:     http://localhost:8502"
echo "🔍 Scan Builder:        http://localhost:8503"
echo "📈 Strategy Viewer:     http://localhost:8510"
echo ""
echo "📚 Quick Start:"
echo "🔍 Scan Builder (8503): Paste AI scan JSON → Select tickers/dates → Run scan"
echo "📊 Signal Codifier (8502): Convert strategy rules to executable signals"
echo "📈 Strategy Viewer (8510): Load strategy files → View backtests"
echo ""
echo "🛑 To stop services: pkill -f streamlit"
echo ""

# Keep script running and show process IDs
echo "Running processes:"
echo "Signal Codifier PID: $CODIFIER_PID"
echo "Scan Builder PID: $SCAN_PID"
echo "Strategy Viewer PID: $VIEWER_PID"
echo ""
echo "Press Ctrl+C to stop all services..."

# Wait for user interrupt
trap 'echo ""; echo "🛑 Stopping services..."; kill $CODIFIER_PID $SCAN_PID $VIEWER_PID 2>/dev/null; echo "✅ Services stopped"; exit 0' INT

# Keep the script alive
while true; do
    sleep 1
done