#!/bin/bash

# COMMANDER2TTS Server Launcher (Bash version)
# Simple wrapper to start a local HTTP server

PORT=8000
HTML_FILE="commander2tts.html"

echo "========================================================"
echo "⚔️  COMMANDER2TTS Server Launcher"
echo "========================================================"

# Check if commander2tts.html exists
if [ ! -f "$HTML_FILE" ]; then
    echo "❌ Error: $HTML_FILE not found in current directory"
    echo "   Please run this script in the same folder as commander2tts.html"
    exit 1
fi

# Kill any existing server on this port
echo ""
echo "🔍 Checking for existing server on port $PORT..."

if command -v lsof &> /dev/null; then
    # Use lsof if available (most common)
    PID=$(lsof -ti:$PORT 2>/dev/null)
    if [ ! -z "$PID" ]; then
        echo "🔨 Killing existing server (PID: $PID)..."
        kill -9 $PID 2>/dev/null
        sleep 1
        echo "✅ Old server stopped"
    else
        echo "✅ No existing server found"
    fi
elif command -v netstat &> /dev/null; then
    # Fallback to netstat
    PID=$(netstat -tulpn 2>/dev/null | grep ":$PORT " | awk '{print $7}' | cut -d'/' -f1)
    if [ ! -z "$PID" ]; then
        echo "🔨 Killing existing server (PID: $PID)..."
        kill -9 $PID 2>/dev/null
        sleep 1
        echo "✅ Old server stopped"
    else
        echo "✅ No existing server found"
    fi
elif command -v ss &> /dev/null; then
    # Fallback to ss (newer systems)
    PID=$(ss -tulpn 2>/dev/null | grep ":$PORT " | grep -oP 'pid=\K[0-9]+')
    if [ ! -z "$PID" ]; then
        echo "🔨 Killing existing server (PID: $PID)..."
        kill -9 $PID 2>/dev/null
        sleep 1
        echo "✅ Old server stopped"
    else
        echo "✅ No existing server found"
    fi
else
    echo "⚠️  Cannot detect existing server (lsof/netstat/ss not found)"
    echo "   If port $PORT is in use, you may need to kill it manually"
fi

echo ""
echo "Starting server on port $PORT..."
echo ""

# Try Python 3 first
if command -v python3 &> /dev/null; then
    echo "✅ Using Python 3"
    echo "🌐 Server: http://localhost:$PORT/$HTML_FILE"
    echo ""
    echo "💡 Press Ctrl+C to stop the server"
    echo "========================================================"
    echo ""
    
    # Try to open browser (works on most Linux distros)
    if command -v xdg-open &> /dev/null; then
        sleep 1 && xdg-open "http://localhost:$PORT/$HTML_FILE" &
    fi
    
    python3 -m http.server $PORT
    
# Try Python 2 as fallback
elif command -v python &> /dev/null; then
    echo "✅ Using Python 2"
    echo "🌐 Server: http://localhost:$PORT/$HTML_FILE"
    echo ""
    echo "💡 Press Ctrl+C to stop the server"
    echo "========================================================"
    echo ""
    
    if command -v xdg-open &> /dev/null; then
        sleep 1 && xdg-open "http://localhost:$PORT/$HTML_FILE" &
    fi
    
    python -m SimpleHTTPServer $PORT
    
# No Python found
else
    echo "❌ Error: Python not found!"
    echo ""
    echo "Please install Python 3:"
    echo "  Ubuntu/Debian: sudo apt install python3"
    echo "  Fedora:        sudo dnf install python3"
    echo "  Arch:          sudo pacman -S python"
    echo ""
    exit 1
fi
