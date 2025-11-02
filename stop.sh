#!/bin/bash
# Stop Tides & Tomes dashboard

echo "🛑 Stopping Tides & Tomes dashboard..."

# Find and kill streamlit processes
pkill -f "streamlit run presentation/app.py"

if [ $? -eq 0 ]; then
    echo "✅ Dashboard stopped successfully"
else
    echo "⚠️  No running dashboard found"
fi
