#!/bin/bash

# SMM Drip Feed Automation - Startup Script
# This script starts both the Next.js app and Convex backend

echo "🚀 Starting SMM Drip Feed Automation Platform"
echo "============================================="
echo ""
echo "📍 App Location: /Users/michaeldurante/wzrd ai/smm-app"
echo "🌐 Web Interface: http://localhost:3456"
echo "🔧 Convex Backend: http://localhost:5555"
echo ""

cd "/Users/michaeldurante/wzrd ai/smm-app"

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Shutting down services..."
    kill $NEXTJS_PID $CONVEX_PID 2>/dev/null
    exit 0
}

trap cleanup INT TERM

echo "📦 Starting Convex Backend (Port 5555)..."
npm run convex:dev &
CONVEX_PID=$!

echo "⏳ Waiting for Convex to initialize..."
sleep 5

echo "🌐 Starting Next.js App (Port 3456)..."
npm run dev &
NEXTJS_PID=$!

echo ""
echo "✨ Services Started Successfully!"
echo "================================="
echo ""
echo "📌 Access Points:"
echo "   Web App:     http://localhost:3456"
echo "   Convex Dev:  http://localhost:5555"
echo ""
echo "📊 Dashboard Features:"
echo "   • Real-time campaign monitoring"
echo "   • Parallel worker processing"
echo "   • 6 intelligent drip feed algorithms"
echo "   • Circuit breaker protection"
echo "   • Live metrics and analytics"
echo ""
echo "Press Ctrl+C to stop all services"
echo ""

# Keep script running
wait $NEXTJS_PID $CONVEX_PID