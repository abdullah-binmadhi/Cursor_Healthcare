#!/bin/bash

# Healthcare Website Launcher
# This script starts a local web server for the healthcare analytics website

echo "🏥 Healthcare Analytics Website"
echo "================================"
echo ""
echo "Starting web server on port 8080..."
echo ""
echo "🌐 Open your browser and go to:"
echo "   http://localhost:8080"
echo ""
echo "⚠️  Press Ctrl+C to stop the server"
echo ""
echo "================================"
echo ""

# Start Python HTTP server
cd "$(dirname "$0")"
python3 -m http.server 8080
