#!/bin/bash
# Tides & Tomes Presentation Launcher
# Bash script to run the Streamlit dashboard on Linux/openEuler

echo -e "\033[0;36m🌊 Tides & Tomes - Starting Presentation Dashboard...\033[0m"
echo ""

# Check if streamlit is installed
if ! python3 -m streamlit --version &> /dev/null; then
    echo -e "\033[0;33m⚠️  Streamlit not found. Installing dependencies...\033[0m"
    python3 -m pip install -r presentation/requirements.txt
    echo ""
fi

echo -e "\033[0;32m✅ Launching dashboard...\033[0m"
echo ""
echo -e "\033[0;37m📱 The presentation will open in your browser at http://localhost:8501\033[0m"
echo ""
echo -e "\033[0;37m🎯 Challenge Pages:\033[0m"
echo -e "\033[0;90m   • Overview - Complete system visualization\033[0m"
echo -e "\033[0;90m   • CompSoc Challenge - Interactive sensitivity analysis\033[0m"
echo -e "\033[0;90m   • G-Research Challenge - Real-time data monitoring\033[0m"
echo -e "\033[0;90m   • Hoppers Challenge - Edinburgh impact stories\033[0m"
echo ""
echo -e "\033[0;33mPress Ctrl+C to stop the server\033[0m"
echo -e "\033[0;36m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\033[0m"
echo ""

# Run streamlit
python3 -m streamlit run presentation/app.py
