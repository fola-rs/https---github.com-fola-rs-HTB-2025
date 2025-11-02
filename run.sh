#!/bin/bash
# Quick launcher for openEuler/Linux
# Make this file executable with: chmod +x run.sh

cd "$(dirname "$0")"
python3 -m streamlit run presentation/app.py --server.headless=true
